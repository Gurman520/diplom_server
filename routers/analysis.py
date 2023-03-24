import logging as log
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from request.request_class import Status, Start, Result
from response.response_class import ResponseStatus, ResponseStart, ResponseResult
from app.predict import start, status, result

# PYTHON_PATH = 'C:/Users/Роман/PycharmProjects/Server_D/venv/Scripts/python.exe'
log.basicConfig(level=log.INFO, filename="./log file/predict.log", filemode="a",
                format="%(asctime)s %(levelname)s %(message)s")

router = APIRouter(
    prefix="/api/v1",
    tags=["predict"],
    responses={404: {"description": "Not found"}},
)


@router.post("/predict", response_model=ResponseStart)
def start_analysis(req_start: Start):
    log.info("Post start predict")
    uuid, err = start(req_start)
    if err is not None:
        return HTTPException(status_code=400, detail="Ошибка запуска анализа: " + str(err))
    return ResponseStart(UUID=str(uuid))


@router.get("/predict/status/{uuid}", response_model=ResponseStatus)
def status_analysis(req_status: Status):
    log.info("Get status predict")
    subpr, return_code = status(req_status)
    if subpr is None:
        return JSONResponse(
            content={"Message": "Не верный uuid. Задачи с таким uuid не сущетсвует."},
            status_code=404)
    if return_code == 0:
        return ResponseStatus(Message="Finish")
    elif return_code is None:
        return ResponseStatus(Message="Processing")
    else:
        return JSONResponse(content={"Message": "Ошибка в работе алгоритма анализа. Returncode: " + str(subpr.returncode)},
                            status_code=400)


@router.get("/predict/result/{uuid}", response_model=ResponseResult)
def get_result(req_result: Result):
    log.info("Get result predict")
    s, ls = result(req_result)
    if s is None:
        return JSONResponse(
            content={"Message": "Не верный uuid. Задачи с таким uuid не сущетсвует."},
            status_code=404)
    if len(ls) == 0:
        return JSONResponse(
            content={"Message": "Нет такого файла"},
            status_code=404)
    return ResponseResult(file=ls)
