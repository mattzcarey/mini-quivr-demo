"""Streamlit app.

Please read the README.md in the root to set up the project. 

Start from project root with :
```bash
PYTHONPATH=. streamlit run demo/main.py
```
Don't forget to set .env variables before running the app.
"""

import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory

from demo.constants.paths import ROOT_FOLDER
from demo.llm.handlers import PrintRetrievalHandler, StreamHandler
from demo.llm.llm import get_llm_chain, get_qa_chain
from demo.prompts.welcome_message import build_welcome_message

st.set_page_config(
    "Mini Quivr 🤖",
    initial_sidebar_state="expanded",
    page_icon=str(ROOT_FOLDER / "demo/logo.png"),
)

st.title("Mini Quivr 🤖")

# uploaded_files = st.sidebar.file_uploader(
#     label="Upload PDF files", type=["pdf"], accept_multiple_files=True
# )
# if not uploaded_files:
#     st.info("Please upload PDF documents to continue.")
#     st.stop()

# Setup memory for contextual conversation
msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=msgs, return_messages=True)

# Get LLM chain
chain = get_llm_chain()
# chain = get_qa_chain(uploaded_files, memory)

# Clear History
if len(msgs.messages) == 0 or st.sidebar.button("Clear message history"):
    msgs.clear()
    #Set welcome message..
    msgs.add_ai_message(build_welcome_message())

# Fix avatars for Streamlit
avatars = {"human": "user", "ai": "assistant", "system": "system"}
for msg in msgs.messages:
    st.chat_message(avatars[msg.type]).write(msg.content)

# Query LLM
if user_query := st.chat_input(placeholder="Ask me anything!"):
    #comment this for the weird memory thing
    msgs.add_user_message(user_query)
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        # Define callback handlers
        # retrieval_handler = PrintRetrievalHandler(st.container())
        stream_handler = StreamHandler(st.empty())

        response = chain.run(question=user_query)
        msgs.add_ai_message(response)
        st.write(response)

        # response = chain.run(user_query, callbacks=[retrieval_handler, stream_handler])
