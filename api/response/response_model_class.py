from pydantic import BaseModel
from fastapi import File


class ResponseModelSet(BaseModel):
    NameModel: str


class ResponseModelDelete(BaseModel):
    Message: str


class ResponseModelRun(BaseModel):
    NameModel: str


class ResponseModelList(BaseModel):
    NameModel: list
