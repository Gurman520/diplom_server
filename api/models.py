import logging as log
from fastapi import APIRouter
from api.request.request_model_class import RequestModelDelete, RequestModelSet
from api.response.response_model_class import ResponseModelSet, ResponseModelDelete, ResponseModelCurrent, \
    ResponseModelList
from app.models import list_models, delete_model, current_model

log.basicConfig(level=log.INFO, filename="./Files/log file/models.log", filemode="a",
                format="%(asctime)s %(levelname)s %(message)s")

router = APIRouter(
    prefix="/api/v1",
    tags=["models"],
    responses={404: {"description": "Not found"}},
)


@router.put("/models", response_model=ResponseModelSet)
def set_models(req_result: RequestModelSet):
    return ResponseModelSet(NameModel="static")


@router.delete("/models/{model_id}", response_model=ResponseModelDelete)
def delete_models(model_id: int):
    delete_model(model_id)
    return ResponseModelDelete(Message="OK")


@router.get("/models", response_model=ResponseModelCurrent)
def current_models():
    name_model = current_model()
    return ResponseModelCurrent(NameModel=name_model)


@router.get("/models/list", response_model=ResponseModelList)
def list_models():
    log.info("Get List models")
    ls = list_models()
    return ResponseModelList(Model=ls)
