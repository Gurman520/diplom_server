from fastapi import File
from pydantic import BaseModel


class Status(BaseModel):
    uuid: str


class Start(BaseModel):
    userID: int
    nameFile: str
    file: bytes = File()


class Result(BaseModel):
    uuid: str
