from pydantic import BaseModel


class ResponseTrainStatus(BaseModel):
    Message: str


class ResponseTrain(BaseModel):
    UUID: str


class ResponseTrainResult(BaseModel):
    Model: list
    Score: str
