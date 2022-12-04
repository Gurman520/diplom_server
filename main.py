from typing import Union

from fastapi import FastAPI, Body
from logic import start

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


@app.get("ping")
def ping():
    return {"succses": "OK"}


@app.get("start-analysis")
def start_analysis(data = Body()):
    rezult = start()
    if rezult == None:
        return {"succuss": "OK"}
    else:
        return {"Error": rezult}


@app.get("status-analysis")
def status_analysis():
    return {"succuss": "OK"}