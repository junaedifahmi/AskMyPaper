from pathlib import Path

from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    
    ## DataSource Setting
    DB_PATH: Path = "./db"
    DB_INDEX: str = "index"
    
    
    ## LLM Setting
    CHAT_MODEL: str = "mistral"
    LLM_BASE_URL: str = "http://localhost:11434"
    EMBEDDING_MODEL: str =  "mxbai-embed-large"
    
    ## Agent Setting
    SYSTEM_PROMPT: str = "./agent/prompt.txt"

    ## Document Loader
    UNSTRUCTURED_SERVICE_URL: str = "http://localhost:8000"
    UNSTRUCTURED_API_KEY: str = "duar:mewek"
        
    
    
    
def get_setting() -> Setting:
    s = Setting()
    try:
        p = Path(s.SYSTEM_PROMPT)
        assert p.exists(), "file prompt is not exist"
        s.SYSTEM_PROMPT = p.read_text()
    except Exception as e:
        pass
    return s