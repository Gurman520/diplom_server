from pydantic import BaseModel


class PredictComments(BaseModel):
    number: int
    comment: str


class Start(BaseModel):
    userID: int
    comments: list[PredictComments]
