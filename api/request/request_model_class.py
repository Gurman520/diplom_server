from pydantic import BaseModel


class RequestModelSet(BaseModel):
    ModelID: int
