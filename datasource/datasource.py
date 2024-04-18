from typing import Text, Dict, List, Tuple
from datetime import datetime

from langchain_community.vectorstores.faiss import FAISS
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_core.documents import Document


from settings import get_setting, Setting


class DataSource:
    def __init__(self) -> None:
        cfg: Setting = get_setting()
        self.local_path = cfg.DB_PATH
        self.embedding = OllamaEmbeddings(
            base_url=cfg.LLM_BASE_URL,
            model=cfg.EMBEDDING_MODEL
        )
        self.index_name = cfg.DB_INDEX
        self._retrive_from_local()
        
    def _retrive_from_local(self):
        if self.local_path.exists():
            try:
                self.db: FAISS = FAISS.load_local(
                    folder_path=self.local_path,
                    embeddings=self.embedding,
                    index_name=self.index_name,
                    allow_dangerous_deserialization=True
                )
            except Exception as e:
                print(type(e).__name__ , str(e) )
        else:
            init_text = [f"DB initialized at { datetime.now().isoformat(sep=' ')}"]
            self.db: FAISS = FAISS.from_texts(texts=init_text, embedding=self.embedding)
            
    async def _save_to_local(self):
        try:
            self.db.save_local(
                folder_path=self.local_path,
                index_name=self.index_name
            )
        except Exception as e:
            print( type(e).__name__, str(e) )
        
    async def _refresh(self):
        await self._save_to_local()
        self._retrive_from_local()
    
    async def get_vectorstore(self, config: Dict):
        return self.db.as_retriever(config)
    
    async def get_similarity_with_score(self, query: Text, k: int = 4) -> List[Tuple[Document, float]]:
        result = self.db.similarity_search_with_relevance_scores(query, k=k)
        return result

    async def delete_item_from_db(self, item_id: str):
        if self.db.delete([item_id]):
            self._refresh()
        else:
            return False
            
    async def add_item_to_db(self, docs: List[Document]):
        try: 
            ids = await self.db.aadd_documents(docs)
            self._refresh()
            return ids
        except Exception as e:
            return e
        
        
        
sources = DataSource()