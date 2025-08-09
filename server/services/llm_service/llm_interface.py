"""Interface for the LLM service"""

from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel

from services.llm_service.llm_config import MODEL, MODEL_PROVIDER

class LLMInterface:

    _llm: BaseChatModel = None

    def __init__(self):
        self._llm = init_chat_model(model=MODEL, model_provider=MODEL_PROVIDER)

    def generate_response(self, prompt: str) -> str:
        return self._llm.invoke(prompt)