from pydantic import BaseModel


class PredictResultComments(BaseModel):
    number: int
    comment: str
    class_comment: int


class ResponseStatus(BaseModel):
    Message: str


class ResponseStart(BaseModel):
    UUID: str


class ResponseResult(BaseModel):
    comments: list[PredictResultComments]


class ResponseError(BaseModel):
    Message: str
