from fastapi import File
from pydantic import BaseModel


class RequestModelSet(BaseModel):
    NameModel: str


class RequestModelDelete(BaseModel):
    NameModel: str
