import os
import subprocess
from typing import Union
import threading
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
    log.info("Get start analysis")
    sp = subprocess.Popen(
        [PYTHON_PATH, os.path.join('.', 'logic.py')])
    print("Основной поток")
    return {"succuss": "OKK"}


@app.get("/api/v1/analysis/status")
def status_analysis():
    log.info("Get status analysis")
    result = status()
    if result == 0:
        return {"Status": "Finish"}
    elif result == 1:
        return {"Status": "processing"}
    else:
        return {"Status": "error processing analysis"}


@app.get("api/v1/analysis/get-result")
def get_result():
    log.info("Get Get-result analysis")
    return result()


async def d():
    await start()
