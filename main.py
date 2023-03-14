import os

from typing import Union
import asyncio
import logging as log
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from routers import analysis, models, train


app = FastAPI()
log.basicConfig(level=log.INFO, filename="log.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s")
log.info("Start server")

app.include_router(analysis.router)
app.include_router(train.router)
app.include_router(models.router)


@app.get("/api/v1/Health-Check")
def ping():
    log.info("Get Health-Check")
    return {"Message": "OK"}
