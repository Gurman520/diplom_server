from pydantic import BaseModel
from fastapi import File


class ResponseModelSet(BaseModel):
    Model: list


class ResponseModelDelete(BaseModel):
    Model: list


class ResponseModelCurrent(BaseModel):
    Model: list


class ResponseModelList(BaseModel):
    Models: list
