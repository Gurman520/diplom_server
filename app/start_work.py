import os
import subprocess
import logging as log
import dal.dal as dal
from dal.models import get_model
from cm.config import Config

pathModel = "./Files/Models/"


def restoring_work(connection):
    tasks = dal.get_work_predict(connection)
    for task in tasks:
        model = get_model(task[1], connection)
        sp = subprocess.Popen(
            [Config.PYTHON_PATH, os.path.join('./', Config.NAME_FILE_PREDICT), '-path_to_file', str(task[0]), '-path_to_model',
             pathModel + model[1] + ".joblib"])
        if sp.stderr is not None:
            continue
        status_subprocess_predict.update({task[0]: sp})

    tasks = dal.get_work_train(connection)
    for task in tasks:
        model = get_model(task[1], connection)
        sp = subprocess.Popen(
            [PYTHON_PATH, os.path.join('./', NAME_FILE_TRAIN), '-path_to_file', str(task[0]),
             '-path_to_model', pathModel + model[1] + ".joblib", '-uuid', str(task[0])])
        if sp.stderr is not None:
            continue
        status_subprocess_train.update({task[0]: sp})

    log.info("Task is all start")
