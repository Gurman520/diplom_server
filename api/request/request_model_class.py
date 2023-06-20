from pydantic import BaseModel


class RequestModelSet(BaseModel):
    ModelID: int


class RequestModelRename(BaseModel):
    NameModel: str
