from pydantic import BaseModel
from fastapi import File


class ResponseTrainStatus(BaseModel):
    Message: str


class ResponseTrain(BaseModel):
    UUID: str


class ResponseTrainResult(BaseModel):
    file: bytes = File()
    score: str
