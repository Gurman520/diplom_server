from fastapi import APIRouter
from api.request.request_train_class import RequestTrain, RequestTrainStatus, RequestTrainResult
from api.response.response_train_class import ResponseTrain, ResponseTrainStatus, ResponseTrainResult

# PYTHON_PATH = 'C:/Users/Роман/PycharmProjects/Server_D/venv/Scripts/python.exe'


router = APIRouter(
    prefix="/api/v1",
    tags=["teach"],
    responses={404: {"description": "Not found"}},
)


@router.post("/teach", response_model=ResponseTrain)
def get_result(req_result: RequestTrain):
    pass


@router.get("/teach/status/{uuid}", response_model=ResponseTrainStatus)
def get_result(req_result: RequestTrainStatus):
    pass


@router.get("/teach/result/{uuid}", response_model=ResponseTrainResult)
def get_result(req_result: RequestTrainResult):
    pass