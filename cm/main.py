import sys
import os

import uvicorn
import logging as log
from cm.info import description, tags_metadata
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from cm.config import Config

from dal.dal import create_connection

connection = create_connection(Config)

# Востановление задачь после неудачной остановки сервера
from app.start_work import restoring_work

restoring_work()

app = FastAPI(
    title="Machine Learning Server",
    description=description,
    version="0.2.0",
    openapi_tags=tags_metadata
)

from api import models, train, analysis

app.include_router(analysis.router)
app.include_router(train.router)
app.include_router(models.router)

log.info("Start main server")


@app.get("/api/v1/Health-Check")
def ping():
    log.info("Get Health-Check")
    return {"Message": "OK"}


@app.get("/")
def doc():
    log.info("Get Home page - redirect /docs#/")
    return RedirectResponse("/docs#/")


if __name__ == "__main__":
    uvicorn.run(app)
