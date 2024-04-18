import yaml
from typing import List, Annotated, Tuple, Dict

from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_community.llms.ollama import Ollama
from langchain_community.callbacks import get_openai_callback


from settings import get_setting
from datasource.datasource import DataSource


class RAG:
    def __init__(self) -> None:
        cfg = get_setting()
        
        prompt = ChatPromptTemplate.from_template( cfg.SYSTEM_PROMPT )
        model = Ollama(
            base_url=cfg.LLM_BASE_URL,
            model=cfg.CHAT_MODEL
        )

        inputs = {
            "question": RunnablePassthrough(),
            "sources": RunnablePassthrough(),
        }
        
        output = StrOutputParser()
        
        self.chain = inputs | prompt | model | output
        self.retriever = DataSource()
    
    def retrieve(self, query: str) -> List[Tuple[Document, float]]:
        data = self.retriever.get_similarity_with_score(query=query)
        return data
    
    def invoke(self, query: str) -> str:
        sources = self.retrieve(query)
        resp = self.chain.invoke({"question": query, "sources": sources})
        return resp
    
    def _format_source(self, src: List[Tuple[Document, float]]) -> List[Tuple[int, Dict]]:
        source = [ s for s in src ]
        return source
    
    def __call__(self, query: str) -> str:
        return self.invoke(query)
    
    
if __name__ == "__main__":
    setting = get_setting()
    agent = RAG(setting)
    
    while True:
        text = input("this input ")
        ans = agent(text)
        print(ans)