import os
import uuid as u
import subprocess
import logging as log
from app.parser import write_to_file
import dal.models as mod_dal
import dal.train as dal
from dal.dal import get_work_train
from cm.main import connection
from cm.config import Config

status_subprocess_train = dict()  # Словарь, который хранит информацию о всех запущенных процессах.
pathModel = "./Files/Models/"


def start(request):
    uuid = u.uuid4()
    write_to_file(request.comments, uuid, 0)
    model = mod_dal.get_model(request.modelID, connection)
    print(os.path.join('./', Config.NAME_FILE_TRAIN))
    sp = subprocess.Popen(
        [Config.PYTHON_PATH, os.path.join('./', Config.NAME_FILE_TRAIN), '-path_to_file', str(uuid),
         '-path_to_model', pathModel + model[1] + ".joblib", '-uuid', str(uuid)])
    if sp.stderr is not None:
        return 0, sp.stderr
    status_subprocess_train.update({uuid: sp})
    dal.add_new_train_task(str(uuid), request.userID, model[0], connection)
    return uuid, None


def status(req_uuid):
    uuid = u.UUID(req_uuid)
    subpr = status_subprocess_train.get(uuid)
    if subpr is None:
        return subpr, 0
    return_code = subpr.poll()  # Получение информации о статусе подпроцесса. Завершен, в процессе, прерван.
    if return_code is None:
        dal.set_train_status(str(uuid), 1, connection)
    elif return_code == 0:
        dal.set_train_status(str(uuid), 0, connection)
        if not exists_model(str(uuid)):
            # Вызвать метод оценки модели.
            score = 89
            model = mod_dal.add_new_model(str(uuid), score, connection)
    else:
        dal.set_train_status(str(uuid), -1, connection)
    return subpr, return_code


def result(req_uuid):
    uuid = u.UUID(req_uuid)
    subpr = status_subprocess_train.get(uuid)
    if subpr is None:
        return None, "", 0
    stat = dal.get_train_task(str(uuid), connection)
    if stat == 1:
        return stat, "", 0
    elif stat == 0:
        model = mod_dal.get_model_for_name(str(uuid), connection)
        return stat, model
    else:
        return stat, "", 0


def exists_model(model_name):
    try:
        mod_dal.get_model_for_name(model_name, connection)
    except Exception as e:
        log.error(f"Model with name %s not exists", model_name)
        return False
    return True


def restart_train():
    tasks = get_work_train(connection)
    for task in tasks:
        model = mod_dal.get_model(task[1], connection)
        sp = subprocess.Popen(
            [Config.PYTHON_PATH, os.path.join('./', Config.NAME_FILE_TRAIN), '-path_to_file', str(task[0]),
             '-path_to_model', pathModel + model[1] + ".joblib", '-uuid', str(task[0])])
        if sp.stderr is not None:
            continue
        status_subprocess_train.update({task[0]: sp})
