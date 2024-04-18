from typing import Text

from pydantic import BaseModel, Field

class Inquery(BaseModel):
    text: str = Field(examples=["What the meaning of transformers layer?"])
    