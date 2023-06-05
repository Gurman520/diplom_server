import logging as log
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.request.request_train_class import RequestTrain
from api.response.response_train_class import ResponseTrain, ResponseTrainStatus, ResponseTrainResult, \
    ResponseTrainError, ResponseTrainNotFound
from app.train import start, status, result
from cm.info import des_train_start, des_train_status

router = APIRouter(
    prefix="/api/v1",
    tags=["teach"],
    responses={404: {"description": "Not found"}},
)


@router.post("/teach", response_model=ResponseTrain, responses={400: {"model": ResponseTrainError}},
             description=des_train_start)
def start_teach(req_start: RequestTrain):
    log.info("Post start teach")
    uuid, err = start(req_start)
    if err is not None:
        return JSONResponse(content={"Message": f"Ошибка запуска обучения: {str(err)}"}, status_code=400)
    return ResponseTrain(UUID=str(uuid))


@router.get("/teach/status/{uuid}", response_model=ResponseTrainStatus,
            responses={400: {"model": ResponseTrainError}, 404: {"model": ResponseTrainNotFound}},
            description=des_train_status)
def get_status(uuid: str):
    log.info("Get status train")
    subpr, return_code = status(uuid)
    if subpr is None:
        return JSONResponse(
            content={"Message": "Не верный uuid. Задачи с таким uuid не сущетсвует."},
            status_code=404)
    if return_code == 0:
        return ResponseTrainStatus(Message="Finish")
    elif return_code is None:
        return ResponseTrainStatus(Message="Processing")
    else:
        return JSONResponse(
            content={"Message": "Ошибка в работе алгоритма обучения. Returncode: " + str(subpr.returncode)},
            status_code=400)


@router.get("/teach/result/{uuid}", response_model=ResponseTrainResult,
            responses={400: {"model": ResponseTrainError}, 404: {"model": ResponseTrainNotFound}},
            description=des_train_status)
def get_result(uuid: str):
    log.info("Get result train")
    stat, model = result(uuid)
    if stat is None:
        return JSONResponse(
            content={"Message": "Не верный uuid. Задачи с таким uuid не сущетсвует."},
            status_code=404)
    elif stat == 0:
        return ResponseTrainResult(Model=model)
    elif stat == 1:
        return JSONResponse(content={"Message": "Процесс обучения не завершён"}, status_code=200)
    else:
        return JSONResponse(
            content={"Message": "Ошибка в работе алгоритма обучения. Returncode: " + str(stat)},
            status_code=400)
