from pydantic import BaseModel
from fastapi import File


class ResponseModelSet(BaseModel):
    NameModel: str


class ResponseModelDelete(BaseModel):
    Message: str


class ResponseModelCurrent(BaseModel):
    NameModel: str


class ResponseModelList(BaseModel):
    Models: list
