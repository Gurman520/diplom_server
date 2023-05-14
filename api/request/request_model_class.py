from fastapi import File
from pydantic import BaseModel


class RequestModelSet(BaseModel):
    ModelID: int
