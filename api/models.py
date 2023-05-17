import logging as log
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.request.request_model_class import RequestModelSet
from api.response.response_model_class import ResponseModelSet, ResponseModelDelete, ResponseModelCurrent, \
    ResponseModelList
from app.models import list_model, delete_model, get_current_model, set_model
from cm.info import des_model_put, des_model_delete


router = APIRouter(
    prefix="/api/v1",
    tags=["models"],
    responses={404: {"description": "Not found"}},
)


@router.put("/models", response_model=ResponseModelSet, description=des_model_put)
def set_models(req_result: RequestModelSet):
    log.info("PUT current model")
    model_id = req_result.ModelID
    model = set_model(model_id)
    if model is None:
        return JSONResponse(content={"Message": "Такой модели не существует."}, status_code=404)
    return ResponseModelSet(Model=model)


@router.delete("/models/{model_id}", response_model=ResponseModelDelete, description=des_model_delete)
def delete_models(model_id: int):
    model, message = delete_model(model_id)
    if message == "Current model":
        return JSONResponse(content={"Message": "Модель является основной"}, status_code=400)
    elif message == "OK":
        return ResponseModelDelete(Model=model)
    else:
        return JSONResponse(content={"Message": "Такой модели не существует."}, status_code=404)


@router.get("/models", response_model=ResponseModelCurrent)
def current_models():
    log.info("Get work model")
    model = get_current_model()
    return ResponseModelCurrent(Model=model)


@router.get("/models/list", response_model=ResponseModelList)
def list_models():
    log.info("Get List Models")
    ls = list_model()
    return ResponseModelList(Models=ls)
