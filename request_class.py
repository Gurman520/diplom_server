import io

from pydantic import BaseModel


class Status(BaseModel):
    uuid: str


class Start(BaseModel):
    userID: int
    nameFile: str
    file: bytes


class Result(BaseModel):
    uuid: str
