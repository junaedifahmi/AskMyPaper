import yaml
from typing import List, Dict

from langchain.agents import AgentExecutor
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


from langchain_community.llms.ollama import Ollama
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.vectorstores.faiss import FAISS


from utils import DotConfig, get_prompt


the_prompt = """
    you have feelings, now you are feeling sad. Answer all the question how much you are want to answer.
"""

class YourAssistant:
    def __init__(self, cfg: Dict) -> None:
        # self.db: FAISS = FAISS.load_local(
        #     cfg.db.local,
        #     OllamaEmbeddings(),
        #     allow_dangerous_deserialization=True,
        #     index_name=cfg.db.index_name,
        # )

        prompt = ChatPromptTemplate.from_template( the_prompt )
        model = Ollama(
            base_url=cfg.model.base_url,
            model=cfg.model.model
        )

        self.chain = (
            {
                "question": RunnablePassthrough(),
                "sources": RunnablePassthrough(),
            }
            | prompt
            | model
            | StrOutputParser()
        )

    
    def __call__(self, query: str) -> str:
        text = self.chain.invoke(query)
        return text
    
    
    
if __name__ == "__main__":
    with open('config.yml') as f:
        setting = DotConfig(yaml.load(f, Loader=yaml.SafeLoader))
    print(setting)
    
    agent = YourAssistant(setting)
    
    while True:
        text = input("this input ")
        ans = agent(text)
        print(ans)