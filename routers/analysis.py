import os
import subprocess
import uuid as u
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from request_class import Status, Start, Result
from response_class import ResponseStatus, ResponseStart, ResponseResult

PYTHON_PATH = 'C:/Users/Роман/PycharmProjects/Server_D/venv/Scripts/python.exe'
status_subprocess = dict()  # Словарь, которй хранит оинформацию о всех запущенных процессах.

router = APIRouter(
    prefix="/api/v1",
    tags=["predict"],
    responses={404: {"description": "Not found"}},
)


@router.post("/predict", response_model=ResponseStart)
def start_analysis(req_start: Start):
    # log.info("Post start analysis")
    print(req_start.userID, req_start.nameFile, req_start.file, sep=" ")
    uuid = u.uuid1()
    print(uuid)
    sp = subprocess.Popen(
        [PYTHON_PATH, os.path.join('.', 'logic.py '), '-uuid', str(uuid)])
    if sp.stderr is not None:
        return HTTPException(status_code=400, detail="Ошибка запуска анализа: " + str(sp.stderr))
    status_subprocess.update({uuid: sp})
    return ResponseStart(UUID=str(uuid))


@router.get("/predict/status/{uuid}", response_model=ResponseStatus)
def status_analysis(req_status: Status):
    # log.info("Get status analysis")
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
    # log.info("Get Get-result analysis")
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
