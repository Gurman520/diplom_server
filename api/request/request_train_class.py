from fastapi import File
from pydantic import BaseModel


class TrainComments(BaseModel):
    number: int
    comment: str
    class_comment: int


class RequestTrainStatus(BaseModel):
    uuid: str


class RequestTrain(BaseModel):
    userID: int
    comments: list[TrainComments]


class RequestTrainResult(BaseModel):
    uuid: str
