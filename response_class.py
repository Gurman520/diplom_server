from pydantic import BaseModel


class ResponseStatus(BaseModel):
    Message: str


class ResponseStart(BaseModel):
    UUID: str


class ResponseResult(BaseModel):
    file: str


class ResponseError(BaseModel):
    Message: str
