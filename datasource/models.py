from pydantic import BaseModel

class CreateDataModel(BaseModel):
    file: str = "model"
    filename: str = "filename"
    format: str = "format"


class Inqury(BaseModel):
    text: str = "This text"

