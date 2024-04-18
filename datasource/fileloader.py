from typing import Any, List, Dict

from unstructured_client import UnstructuredClient, shared
from settings import get_setting, Setting


class DocumentLoader:
    def __init__(self) -> None:
        settings: Setting = get_setting()
        self.loader = UnstructuredClient(
            api_key_auth=settings.UNSTRUCTURED_API_KEY,
            server_url=settings.UNSTRUCTURED_SERVICE_URL
        )
        
    def _generate_request(self, file: bytes, filename: str, strategy: str, max_character: int):
        return shared.PartitionParameters(
            files=shared.Files(
                content=file,
                file_name=filename
            ),
            strategy=strategy,
            # chunking strategy
            chunking_strategy="basic",
            max_characters=max_character
        )
    
    def make_request(self, file: bytes, filename: str, strategy: str = "auto", max_character: int = 1500) -> List[Dict]:
        req = self._generate_request(file, filename, strategy, max_character)
        result = self.loader.general.partition(req)
        return result
    
    async def __call__(self, file: bytes, filename: str, strategy: str = "auto", max_character: int = 1500) -> List[Dict]:
        return self.make_request(file, filename, strategy=strategy, max_character=max_character)    
    
    def __repr__(self) -> str:
        return f"Unstructed"
    
    
loader = DocumentLoader()