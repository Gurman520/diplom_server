import os
import subprocess
from typing import Union
import asyncio
import logging as log
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse

app = FastAPI()
log.basicConfig(level=log.INFO, filename="log.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s")
log.info("Start server")
PYTHON_PATH = 'C:/Users/Роман/PycharmProjects/Server_D/venv/Scripts/python.exe'
status = dict()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/Health-Check")
def ping():
    log.info("Get Health-Check")
    return {"succses": "OK"}


@app.post("/api/v1/analysis/start")
def start_analysis():
    log.info("Post start analysis")
    s = status.get('1')
    if s is None:
        return {"Message": "На данный момент у данного пользователя уже запущен процесс обучения."}
    sp = subprocess.Popen(
        [PYTHON_PATH, os.path.join('.', 'logic.py')])
    status.update({'1': sp})
    print("Основной поток")
    if sp.stderr is not None:
        return {"Error": sp.stderr}
    return {"success": "OK"}


@app.get("/api/v1/analysis/status")
def status_analysis():
    log.info("Get status analysis")
    s = status.get('1')
    if s is None:
        return JSONResponse(
            content={"Message": "На данный момент у данного пользователя нет запущенных процессов анализа."},
            status_code=404)
    return_code = s.poll()  # Получение информации о статусе подпроцесса. Завершен, в процессе, прерван.
    print("Status: ", return_code)
    # if os.path.isfile('./ss.csv'):
    if return_code == 0:
        status.pop('1')
        return {"Status": "Finish"}
    elif return_code is None:
        return {"Status": "processing"}
    else:
        return {"Error": s.stderr, "Message": "Error analysis alg"}


@app.get("/api/v1/analysis/get-result")
def get_result():
    log.info("Get Get-result analysis")
    return {"message": "Скоро будет, нужно подождать"}
