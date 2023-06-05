from pydantic import BaseModel


class ResponseTrainStatus(BaseModel):
    Message: str


class ResponseTrain(BaseModel):
    UUID: str


class ResponseTrainResult(BaseModel):
    Model: list


class ResponseTrainError(BaseModel):
    Message: str


class ResponseTrainNotFound(BaseModel):
    Message: str = "Не верный uuid. Задачи с таким uuid не сущетсвует."
