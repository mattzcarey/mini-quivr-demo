import openai
from pydantic import BaseModel, SecretStr


class ModelConfig(BaseModel):
    display_name: str
    model_name: str
    api_key: SecretStr
    endpoint_url: str

    def configure_open_ai_module(self) -> None:
        openai.api_key = self.api_key.get_secret_value()
        openai.api_base = self.endpoint_url
