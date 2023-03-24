from fastapi import APIRouter
from api.request.request_model_class import RequestModelDelete, RequestModelSet
from api.response.response_model_class import ResponseModelSet, ResponseModelDelete, ResponseModelRun, ResponseModelList

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


@router.get("/models/list", response_model=ResponseModelList)
def get_result():
    return ResponseModelRun(NameModel=["Tata", "Hata"])
