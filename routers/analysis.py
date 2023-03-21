import os
import subprocess
import uuid as u
import logging as log
import configparser
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from request.request_class import Status, Start, Result
from response.response_class import ResponseStatus, ResponseStart, ResponseResult
from parser import write_to_file

config = configparser.ConfigParser()
config.read('settings.ini', encoding="utf-8")
PYTHON_PATH = config["Settings"]["PYTHON_PATH"]
print(PYTHON_PATH)
# PYTHON_PATH = 'C:/Users/Роман/PycharmProjects/Server_D/venv/Scripts/python.exe'
log.basicConfig(level=log.INFO, filename="./log file/predict.log", filemode="a",
                format="%(asctime)s %(levelname)s %(message)s")
status_subprocess = dict()  # Словарь, которй хранит оинформацию о всех запущенных процессах.

router = APIRouter(
    prefix="/api/v1",
    tags=["predict"],
    responses={404: {"description": "Not found"}},
)


@router.post("/predict", response_model=ResponseStart)
def start_analysis(req_start: Start):
    log.info("Post start predict")
    uuid = u.uuid1()
    write_to_file(req_start.comments, uuid, 1)
    sp = subprocess.Popen(
        [PYTHON_PATH, os.path.join('.', 'logic.py '), '-uuid', str(uuid)])
    if sp.stderr is not None:
        return HTTPException(status_code=400, detail="Ошибка запуска анализа: " + str(sp.stderr))
    status_subprocess.update({uuid: sp})
    return ResponseStart(UUID=str(uuid))


@router.get("/predict/status/{uuid}", response_model=ResponseStatus)
def status_analysis(req_status: Status):
    log.info("Get status predict")
    uui = req_status.uuid
    s = status_subprocess.get(u.UUID(uui))
    if s is None:
        return JSONResponse(
            content={"Message": "Не верный uuid. Задачи с таким uuid не сущетсвует."},
            status_code=404)
    return_code = s.poll()  # Получение информации о статусе подпроцесса. Завершен, в процессе, прерван.
    if return_code == 0:
        return ResponseStatus(Message="Finish")
    elif return_code is None:
        return ResponseStatus(Message="Processing")
    else:
        return JSONResponse(content={"Message": "Ошибка в работе алгоритма анализа. Returncode: " + str(s.returncode)},
                            status_code=400)


@router.get("/predict/result/{uuid}", response_model=ResponseResult)
def get_result(req_result: Result):
    log.info("Get result predict")
    uuid = req_result.uuid
    s = status_subprocess.get(u.UUID(uuid))
    if s is None:
        return JSONResponse(
            content={"Message": "Не верный uuid. Задачи с таким uuid не сущетсвует."},
            status_code=404)
    if os.path.isfile('./' + str(uuid) + '.csv'):
        fp = open('ss.scv', 'rb')
        return FileResponse(path='data.xlsx', filename='Статистика покупок.xlsx', media_type='multipart/form-data')
        # return ResponseResult(file=fp)
    return JSONResponse(
        content={"Message": "Нет такого файла"},
        status_code=404)
