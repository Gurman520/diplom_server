import logging as log
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.request.request_class import Start
from api.response.response_class import ResponseStatus, ResponseStart, ResponseResult
from app.predict import start, status, result
from cm.info import des_pred_info, des_pred_status, des_pred_start

router = APIRouter(
    prefix="/api/v1",
    tags=["predict"],
    responses={404: {"description": "Not found"}},
)


@router.post("/predict", response_model=ResponseStart, description=des_pred_start)
def start_analysis(req_start: Start):
    log.info("Post start predict")
    uuid, err = start(req_start)
    if err is not None:
        return JSONResponse(content={"Message": f"Ошибка запуска анализа: {str(err)}"}, status_code=400)
    return ResponseStart(UUID=str(uuid))


@router.get("/predict/status/{uuid}", response_model=ResponseStatus, description=des_pred_status)
def status_analysis(uuid: str):
    log.info("Get status predict")
    subpr, return_code = status(uuid)
    if subpr is None:
        return JSONResponse(
            content={"Message": "Не верный uuid. Задачи с таким uuid не сущетсвует."},
            status_code=404)
    if return_code == 0:
        return ResponseStatus(Message="Finish")
    elif return_code is None:
        return ResponseStatus(Message="Processing")
    else:
        return JSONResponse(
            content={"Message": f"Ошибка в работе алгоритма анализа. Returncode: {str(subpr.returncode)}"},
            status_code=400)


@router.get("/predict/result/{uuid}", response_model=ResponseResult, description=des_pred_info)
def get_result(uuid: str):
    log.info("Get result predict")
    stat, ls = result(uuid)
    if stat is None:
        return JSONResponse(
            content={"Message": "Не верный uuid. Задачи с таким uuid не сущетсвует."},
            status_code=404)
    elif stat == 0 and len(ls) == 0:
        return JSONResponse(
            content={"Message": "Проблема с формированием файла с результами"},
            status_code=400)
    elif stat == 0 and len(ls) > 0:
        return ResponseResult(comments=ls)
    elif stat == 1:
        return JSONResponse(content={"Message": "Процесс анализа не завершён"}, status_code=200)
    else:
        return JSONResponse(
            content={"Message": "Ошибка в работе алгоритма анализа. Returncode: " + str(stat)},
            status_code=400)
