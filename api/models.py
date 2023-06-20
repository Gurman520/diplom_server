import logging as log
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import api.request.request_model_class as request
import api.response.response_model_class as response
import app.models as app
import api.Converter as conv
import cm.info as info

router = APIRouter(
    prefix="/api/v1",
    tags=["models"],
    responses={404: {"description": "Not found"}},
)


@router.put("/models", response_model=response.ResponseModel,
            responses={404: {"model": response.ResponseModelNotFound}},
            description=info.des_model_put)
def set_models(req_result: request.RequestModelSet):
    log.info("PUT current model")
    model_id = req_result.ModelID
    model = app.set_model(model_id)
    if model is None:
        return JSONResponse(content={"Message": "Такой модели не существует."}, status_code=404)
    return conv.converter_model_to_api(model)


@router.delete("/models/{model_id}", response_model=response.ResponseModel,
               responses={404: {"model": response.ResponseModelNotFound}}, description=info.des_model_delete)
def delete_models(model_id: int):
    model, message = app.delete_model(model_id)
    if message == "Current model":
        return JSONResponse(content={"Message": "Модель является основной"}, status_code=400)
    elif message == "OK":
        return conv.converter_model_to_api(model)
    else:
        return JSONResponse(content={"Message": "Такой модели не существует."}, status_code=404)


@router.get("/models", response_model=response.ResponseModel)
def current_models():
    log.info("Get work model")
    model = app.get_current_model()
    return conv.converter_model_to_api(model)


@router.get("/models/list", response_model=response.ResponseListModels)
def list_models():
    log.info("Get List Models")
    ls = app.list_model()
    return conv.converter_model_list_to_api(ls)


@router.put("/models/{model_id}", response_model=response.ResponseModel,
            responses={404: {"model": response.ResponseModelNotFound}},
            description=info.des_model_rename)
def model_rename(model_id: int, req_rename: request.RequestModelRename):
    log.info("PUT name Model")
    model = app.rename_model(req_rename.NameModel, model_id)
    if model is None:
        return response.ResponseModelNotFound()
    return conv.converter_model_to_api(model)
