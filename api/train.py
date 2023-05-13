import logging as log
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.request.request_train_class import RequestTrain, RequestTrainStatus, RequestTrainResult
from api.response.response_train_class import ResponseTrain, ResponseTrainStatus, ResponseTrainResult
from app.train import start, status, result


router = APIRouter(
    prefix="/api/v1",
    tags=["teach"],
    responses={404: {"description": "Not found"}},
)


@router.post("/teach", response_model=ResponseTrain)
def start_teach(req_start: RequestTrain):
    log.info("Post start teach")
    uuid, err = start(req_start)
    if err is not None:
        return JSONResponse(content={"Message": f"Ошибка запуска обучения: {str(err)}"}, status_code=404)
    return ResponseTrain(UUID=str(uuid))


@router.get("/teach/status/{uuid}", response_model=ResponseTrainStatus)
def get_status(req_status: RequestTrainStatus):
    log.info("Get status train")
    subpr, return_code = status(req_status)
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


@router.get("/teach/result/{uuid}", response_model=ResponseTrainResult)
def get_result(req_result: RequestTrainResult):
    log.info("Get result train")
    stat, name_model, score = result(req_result)
    if stat is None:
        return JSONResponse(
            content={"Message": "Не верный uuid. Задачи с таким uuid не сущетсвует."},
            status_code=404)
    elif stat == 0 and score != 0:
        return ResponseTrainResult(Model_name=name_model, Score=score)
    elif stat == 1:
        return JSONResponse(content={"Message": "Процесс обучения не завершён"}, status_code=200)
    else:
        return JSONResponse(
            content={"Message": "Ошибка в работе алгоритма обучения. Returncode: " + str(stat)},
            status_code=400)
