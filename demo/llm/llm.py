from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chat_models import BedrockChat, ChatOpenAI

from demo.constants.settings import SETTINGS
from demo.llm.retriever import configure_retriever
from demo.prompts.system_prompt import build_prompt

"""
Configure your LLM Chain to use for this personal assistant.
"""

# Configure a LLM to use
llm = ChatOpenAI(
        openai_api_key=SETTINGS.openai_api_key.get_secret_value(),
        model=SETTINGS.model,  # type: ignore
        temperature=SETTINGS.temperature,
        streaming=True,
    )

# llm = BedrockChat(
#     region_name="us-east-1",
#     model_id="anthropic.claude-v2",
#     streaming=True,
# ) # type: ignore

def get_llm_chain():
    # Build prompt template
    prompt = build_prompt()

    #Define basic LLM chain
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    return llm_chain

def get_qa_chain(uploaded_files, memory):
    # Configure the retriever
    retriever = configure_retriever(uploaded_files)

    # ConversationalRetrievalChain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm, retriever=retriever, memory=memory, verbose=True,
    )

    return qa_chain
