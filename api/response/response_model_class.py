from pydantic import BaseModel


class ResponseModelSet(BaseModel):
    Model: list


class ResponseModelDelete(BaseModel):
    Model: list


class ResponseModelCurrent(BaseModel):
    Model: list


class ResponseModelList(BaseModel):
    Models: list


class ResponseModelNotFound(BaseModel):
    Message: str = "Такой модели не существует"
