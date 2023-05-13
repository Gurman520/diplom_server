import logging as log
from fastapi import APIRouter, HTTPException
from api.request.request_train_class import RequestTrain, RequestTrainStatus, RequestTrainResult
from api.response.response_train_class import ResponseTrain, ResponseTrainStatus, ResponseTrainResult


router = APIRouter(
    prefix="/api/v1",
    tags=["teach"],
    responses={404: {"description": "Not found"}},
)


@router.post("/teach", response_model=ResponseTrain)
def start_teach(req_result: RequestTrain):
    log.info("Post start teach")
    uuid, err = start(req_start)
    if err is not None:
        return HTTPException(status_code=400, detail="Ошибка запуска анализа: " + str(err))
    return ResponseTrain(UUID=str(uuid))


@router.get("/teach/status/{uuid}", response_model=ResponseTrainStatus)
def get_status(req_result: RequestTrainStatus):
    pass


@router.get("/teach/result/{uuid}", response_model=ResponseTrainResult)
def get_result(req_result: RequestTrainResult):
    pass
