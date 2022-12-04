from typing import Union
import logging as log
from fastapi import FastAPI, Body
from logic import start

app = FastAPI()
log.basicConfig(level=log.INFO, filename="log.log",filemode="w", format="%(asctime)s %(levelname)s %(message)s")
log.info("Start server")

@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


@app.get("ping")
def ping():
    log.info("Get Ping")
    return {"succses": "OK"}


@app.get("start-analysis")
def start_analysis(data = Body()):
    log.info("Get start analysis")
    rezult = start()
    if rezult == None:
        return {"succuss": "OK"}
    else:
        return {"Error": rezult}


@app.get("status-analysis")
def status_analysis():
    log.info("Get status analysis")
    return {"succuss": "OK"}
