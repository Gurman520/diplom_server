from pydantic import BaseModel


class PredictResultComments(BaseModel):
    number: int
    comment: str
    class_comment: int


class ResponseStatus(BaseModel):
    Message: str = "Processing | Finish"


class ResponseStart(BaseModel):
    UUID: str


class ResponseResult(BaseModel):
    comments: list[PredictResultComments]


class ResponseErrorNotFound(BaseModel):
    Message: str = "Не верный uuid. Задачи с таким uuid не сущетсвует."


class ResponseError(BaseModel):
    Message: str
