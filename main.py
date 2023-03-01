import os
import subprocess
from typing import Union
import asyncio
import logging as log
from fastapi import FastAPI, Body

app = FastAPI()
log.basicConfig(level=log.INFO, filename="log.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s")
log.info("Start server")
flag = 0
PYTHON_PATH = 'C:/Users/Роман/PycharmProjects/Server_D/venv/Scripts/python.exe'


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
    sp = subprocess.Popen(
        [PYTHON_PATH, os.path.join('.', 'logic.py')])
    print("Основной поток")
    if sp.stderr is not None:
        return {"Error": sp.stderr}
    return {"success": "OK"}


@app.get("/api/v1/analysis/status")
def status_analysis():
    log.info("Get status analysis")
    if os.path.isfile('./ss.csv'):
        return {"Status": "Finish"}
    else:
        return {"Status": "processing"}


@app.get("/api/v1/analysis/get-result")
def get_result():
    log.info("Get Get-result analysis")
    return {"message": "Скоро будет, нужно подождать"}
