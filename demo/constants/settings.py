from pydantic import SecretStr
from pydantic_settings import BaseSettings

from demo.constants.paths import ROOT_FOLDER


class Settings(BaseSettings):
    """Settings for the demo app.

    Reads from demo/.env file or environment variables.
    You can create the .env file from the .env_example file.

    !!! SecretStr is a pydantic type that hides the value in logs.
    If you want to use the real value, you should do:
    SETTINGS.<variable>.get_secret_value()
    """

    class Config:
        env_file = ROOT_FOLDER / "demo" / ".env"

    model: str = "gpt-4" # if you have access to GPT4, you can use "gpt-4"
    temperature: float = 0
    openai_api_key: SecretStr
    huggingfacehub_api_token: SecretStr
    custom_hf_endpoint_url: str


SETTINGS = Settings()  # type: ignore
