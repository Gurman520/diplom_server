from pydantic import BaseModel


class ResponseModel(BaseModel):
    ID: int
    NameModel: str
    score: float
    Active: bool


class ResponseListModels(BaseModel):
    Models: list[ResponseModel]


class ResponseModelNotFound(BaseModel):
    Message: str = "Такой модели не существует"
