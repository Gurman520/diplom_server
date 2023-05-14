from pydantic import BaseModel
from fastapi import File


class ResponseTrainStatus(BaseModel):
    Message: str


class ResponseTrain(BaseModel):
    UUID: str


class ResponseTrainResult(BaseModel):
    Model_name: list
    Score: str
