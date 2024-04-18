from typing import Text, Optional

from langchain_community.chat_models.ollama import ChatOllama

from settings import get_setting
from .agent import RAG

agent = RAG()

def invoke_agent(text: str) -> Optional[Text]:
    return agent(text)


def one_time_prompt(prompt: str) -> Optional[Text]:
    setting = get_setting()
    model = ChatOllama(
        base_url=setting.LLM_BASE_URL,
        model=setting.CHAT_MODEL
    )
    output = model.invoke(prompt)
    return output.content