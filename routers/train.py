from fastapi import APIRouter
from request.request_train_class import RequestTrain, RequestTrainStatus, RequestTrainResult
from response.response_train_class import ResponseTrain, ResponseTrainStatus, ResponseTrainResult

PYTHON_PATH = 'C:/Users/Роман/PycharmProjects/Server_D/venv/Scripts/python.exe'
status_subprocess = dict()  # Словарь, которй хранит оинформацию о всех запущенных процессах.

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
