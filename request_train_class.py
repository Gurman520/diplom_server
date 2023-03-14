from fastapi import File
from pydantic import BaseModel


class RequestTrainStatus(BaseModel):
    uuid: str


class RequestTrain(BaseModel):
    userID: int
    nameFile: str
    file: bytes = File()


class RequestTrainResult(BaseModel):
    uuid: str
