import os
import uvicorn
from typing import Union
import asyncio
import configparser
import logging as log
from fastapi import FastAPI
from dal.dal import create_connection


name_bd = "server.sqlite"
cursor = create_connection(name_bd=name_bd)
config = configparser.ConfigParser()
config.read('settings.ini', encoding="utf-8")
PYTHON_PATH = config["Settings"]["PYTHON_PATH"]
print(PYTHON_PATH)
status_subprocess_predict = dict()  # Словарь, которй хранит оинформацию о всех запущенных процессах.
status_subprocess_train = dict()  # Словарь, которй хранит оинформацию о всех запущенных процессах.

app = FastAPI()
log.basicConfig(level=log.INFO, filename="Files/log file/log.log", filemode="a",
                format="%(asctime)s %(levelname)s %(message)s")
log.info("Start server")

from api import analysis, train, models

app.include_router(analysis.router)
app.include_router(train.router)
app.include_router(models.router)


@app.get("/api/v1/Health-Check")
def ping():
    log.info("Get Health-Check")
    return {"Message": "OK"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
