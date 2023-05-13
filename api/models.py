import logging as log
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.request.request_model_class import RequestModelSet
from api.response.response_model_class import ResponseModelSet, ResponseModelDelete, ResponseModelCurrent, \
    ResponseModelList
from app.models import list_model, delete_model, current_model, set_model


router = APIRouter(
    prefix="/api/v1",
    tags=["models"],
    responses={404: {"description": "Not found"}},
)


@router.put("/models", response_model=ResponseModelSet)
def set_models(req_result: RequestModelSet):
    log.info("PUT current model")
    name_model = req_result.NameModel
    model = set_model(name_model)
    if model is None:
        return JSONResponse(content={"Message": "Такой модели не существует."}, status_code=404)
    return ResponseModelSet(NameModel=model)


@router.delete("/models/{model_id}", response_model=ResponseModelDelete)
def delete_models(model_id: int):
    model, message = delete_model(model_id)
    if message == "Current model":
        return JSONResponse(content={"Message": "Модель является основной, по этому удалять нельзя."}, status_code=400)
    elif message == "OK":
        return ResponseModelDelete(NameModel=model)
    else:
        return JSONResponse(content={"Message": "Файл модели не найден."}, status_code=404)


@router.get("/models", response_model=ResponseModelCurrent)
def current_models():
    log.info("Get work model")
    name_model = current_model()
    return ResponseModelCurrent(NameModel=name_model)


@router.get("/models/list", response_model=ResponseModelList)
def list_models():
    log.info("Get List Models")
    ls = list_model()
    return ResponseModelList(Models=ls)
