from pydantic import BaseModel
from fastapi import File


class ResponseModelSet(BaseModel):
    NameModel: str


class ResponseModelDelete(BaseModel):
    NameModel: str


class ResponseModelCurrent(BaseModel):
    NameModel: str


class ResponseModelList(BaseModel):
    Models: list
