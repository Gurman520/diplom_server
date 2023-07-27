import logging as log
import app.predict as pr
import app.train as tr


pathModel = "./Files/Models/"


def restoring_work():
    pr.restart_predict()
    tr.restart_train()
    log.info("Task is all start")
