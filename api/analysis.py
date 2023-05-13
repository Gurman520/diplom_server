import logging as log
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.request.request_class import Status, Start, Result
from api.response.response_class import ResponseStatus, ResponseStart, ResponseResult
from app.predict import start, status, result

router = APIRouter(
    prefix="/api/v1",
    tags=["predict"],
    responses={404: {"description": "Not found"}},
)


@router.post("/predict", response_model=ResponseStart)
def start_analysis(req_start: Start):
    log.info("Post start predict")
    uuid, err = start(req_start)
    if err is not None:
        return JSONResponse(content={"Message": f"Ошибка запуска анализа: {str(err)}"}, status_code=400)
    return ResponseStart(UUID=str(uuid))


@router.get("/predict/status/{uuid}", response_model=ResponseStatus)
def status_analysis(req_status: Status):
    log.info("Get status predict")
    subpr, return_code = status(req_status)
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


@router.get("/predict/result/{uuid}", response_model=ResponseResult)
def get_result(req_result: Result):
    log.info("Get result predict")
    stat, ls = result(req_result)
    if stat is None:
        return JSONResponse(
            content={"Message": "Не верный uuid. Задачи с таким uuid не сущетсвует."},
            status_code=404)
    elif stat == 0 and len(ls) == 0:
        return JSONResponse(
            content={"Message": "Проблема с формированием файла с результами"},
            status_code=404)
    elif stat == 0 and len(ls) > 0:
        return ResponseResult(file=ls)
    elif stat == 1:
        return JSONResponse(content={"Message": "Процесс анализа не завершён"}, status_code=200)
    else:
        return JSONResponse(
            content={"Message": "Ошибка в работе алгоритма анализа. Returncode: " + str(stat)},
            status_code=400)
