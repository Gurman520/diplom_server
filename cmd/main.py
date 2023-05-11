import configparser
import logging as log
from fastapi import FastAPI
from dal.dal import create_connection, add_new_model
from fastapi.responses import JSONResponse

log.basicConfig(level=log.INFO, filename="./Files/log file/main.log", filemode="a",
                format="%(asctime)s %(levelname)s %(message)s")
log.info("---------------------")
connection = create_connection()
if connection is None:
    log.info("Error connection BD. Server run with out BD.")
else:
    log.info("Connection BD successful")
config = configparser.ConfigParser()
config.read('./settings.ini', encoding="utf-8")
PYTHON_PATH = config["Settings"]["PYTHON_PATH"]
NAME_FILE_PREDICT = config["Settings"]["NAME_FILE_PREDICT"]
print(PYTHON_PATH)
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


@app.post("/api/v1/add_new_model")
def add():
    add_new_model("SecondModel.h5", "SecondModel", 90, connection)
    return JSONResponse(
        content={"Message": "Запись успешно добавлена"},
        status_code=200)
