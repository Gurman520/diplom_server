import os
import subprocess
import uuid as u
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from request_model_class import RequestModelDelete, RequestModelSet
from response_model_class import ResponseModelSet, ResponseModelDelete, ResponseModelRun

# PYTHON_PATH = 'C:/Users/Роман/PycharmProjects/Server_D/venv/Scripts/python.exe'
# status_subprocess = dict()  # Словарь, которй хранит оинформацию о всех запущенных процессах.

router = APIRouter(
    prefix="/api/v1",
    tags=["models"],
    responses={404: {"description": "Not found"}},
)


@router.put("/models", response_model=ResponseModelSet)
def get_result(req_result: RequestModelSet):
    return ResponseModelSet(NameModel="static")


@router.delete("/models/{uuid}", response_model=ResponseModelDelete)
def get_result(uuid: int, req_result: RequestModelDelete):
    return ResponseModelDelete(Message="OK")


@router.get("/models", response_model=ResponseModelRun)
def get_result():
    return ResponseModelRun(NameModel="static")


@router.get("/models/list", response_model=ResponseModelRun)
def get_result():
    return ResponseModelRun(NameModel="static")
