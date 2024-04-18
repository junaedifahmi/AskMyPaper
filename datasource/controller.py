from typing import List

from langchain_core.documents import Document

from .datasource import sources
from .fileloader import loader


async def create_item(data: bytes, filename: str) -> List[str]:
    result = await loader(data, filename)
    print(filename)
    docs = []
    for doc in result.elements:
        print(doc)
        page_content = doc["text"]
        metadata = doc["metadata"]
        del metadata["languages"]
        
        docs.append(Document(page_content=page_content, metadata=metadata))
        
    try:
        ids = await sources.add_item_to_db(docs)
        return ids
    except Exception as e:
        return e

def get_all() -> List[str]:
    all = sources.db.docstore._dict
    print(all)
    return all

def get_item(id: str) -> str:
    try:
        item = sources.db.docstore._dict[id]
        return item
    except Exception as e:
        return e

def delete_item(id: str):
    try:
        sources.delete_item_from_db(id)
        return id
    except Exception as e:
        return e