from pydantic import BaseModel
from fastapi import File


class ResponseStatus(BaseModel):
    Message: str


class ResponseStart(BaseModel):
    UUID: str


class ResponseResult(BaseModel):
    file: bytes = File()


class ResponseError(BaseModel):
    Message: str
