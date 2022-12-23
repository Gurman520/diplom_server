from typing import Union
import logging as log
from fastapi import FastAPI, Body
from logic import start, status, result

app = FastAPI()
log.basicConfig(level=log.INFO, filename="log.log",filemode="w", format="%(asctime)s %(levelname)s %(message)s")
log.info("Start server")

@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


@app.get("Health-Check")
def ping():
    log.info("Get Health-Check")
    return {"succses": "OK"}


@app.post("Start-Analysis")
def start_analysis(data = Body()):
    log.info("Get start analysis")
    rezult = start()
    if rezult == None:
        return {"succuss": "OK"}
    else:
        return {"Error": rezult}


@app.get("Status-Analysis")
def status_analysis():
    log.info("Get status analysis")
    result = status()
    if result == 0:
        return {"Status": "Finish"}
    elif result == 1:
        return {"Status": "processing"}
    else:
        return {"Status": "error processing analysis"}

@app.get("Get-result")
def get_result():
    log.info("Get Get-result analysis")
    return result()
