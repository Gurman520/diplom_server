from app import init_log
import configparser
import uvicorn
import logging as log
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from dal.dal import create_connection, add_new_model

connection = create_connection()
config = configparser.ConfigParser()
config.read('settings.ini', encoding="utf-8")
PYTHON_PATH = config["Settings"]["PYTHON_PATH"]
NAME_FILE_PREDICT = config["Settings"]["NAME_FILE_PREDICT"]
NAME_FILE_TRAIN = config["Settings"]["NAME_FILE_TRAIN"]
status_subprocess_predict = dict()  # Словарь, которй хранит оинформацию о всех запущенных процессах.
status_subprocess_train = dict()  # Словарь, которй хранит оинформацию о всех запущенных процессах.

app = FastAPI()
log.info("Start main server")

from api import analysis, train, models

app.include_router(analysis.router)
app.include_router(train.router)
app.include_router(models.router)


@app.get("/api/v1/Health-Check")
def ping():
    log.info("Get Health-Check")
    return {"Message": "OK"}


@app.get("/")
def doc():
    return RedirectResponse("/docs#/")


if __name__ == "__main__":
    uvicorn.run(app)
