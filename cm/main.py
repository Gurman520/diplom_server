import configparser
import uvicorn
import logging as log
from cm.info import description, tags_metadata
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

config = configparser.ConfigParser()
config.read('settings.ini', encoding="utf-8")
PYTHON_PATH = config["Settings"]["PYTHON_PATH"]
NAME_FILE_PREDICT = config["Settings"]["NAME_FILE_PREDICT"]
NAME_FILE_TRAIN = config["Settings"]["NAME_FILE_TRAIN"]
BD_HOST = config["Settings"]["BD_HOST"]
BD_PORT = config["Settings"]["BD_PORT"]

from dal.dal import create_connection
connection = create_connection(BD_HOST, BD_PORT)

status_subprocess_predict = dict()  # Словарь, которй хранит оинформацию о всех запущенных процессах.
status_subprocess_train = dict()  # Словарь, которй хранит оинформацию о всех запущенных процессах.

# Востановление задачь после неудачной останвоки сервера
from app.start_work import restoring_work
restoring_work(connection)

app = FastAPI(
    title="Machine Learning Server",
    description=description,
    version="0.1.0",
    openapi_tags=tags_metadata
)
log.info("Start main server")

from api import models, train, analysis

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
