import os
import uuid as u
import subprocess
import logging as log
from app.parser import write_to_file
from dal.dal import add_new_train_task, set_train_status, get_train_task, get_model_for_name, get_model, add_new_model
from cm.main import PYTHON_PATH, NAME_FILE_TRAIN, status_subprocess_train, connection

pathModel = "./Files/Models/"


def start(request):
    uuid = u.uuid4()
    write_to_file(request.comments, uuid, 0)
    model = get_model(request.modelID, connection)
    print(os.path.join('./', NAME_FILE_TRAIN))
    sp = subprocess.Popen(
        [PYTHON_PATH, os.path.join('./', NAME_FILE_TRAIN), '-path_to_file', str(uuid),
         '-path_to_model', pathModel + model[1] + ".joblib", '-uuid', str(uuid)])
    if sp.stderr is not None:
        return 0, sp.stderr
    status_subprocess_train.update({uuid: sp})
    add_new_train_task(str(uuid), request.userID, model[0], connection)
    return uuid, None


def status(req_uuid):
    uuid = u.UUID(req_uuid)
    subpr = status_subprocess_train.get(uuid)
    if subpr is None:
        return subpr, 0
    return_code = subpr.poll()  # Получение информации о статусе подпроцесса. Завершен, в процессе, прерван.
    if return_code is None:
        set_train_status(str(uuid), 1, connection)
    elif return_code == 0:
        set_train_status(str(uuid), 0, connection)
        if not exists_model(str(uuid)):
            # Вызвать метод оценки модели.
            score = 89
            model = add_new_model(str(uuid), score, connection)
    else:
        set_train_status(str(uuid), -1, connection)
    return subpr, return_code


def result(req_uuid):
    uuid = u.UUID(req_uuid)
    subpr = status_subprocess_train.get(uuid)
    if subpr is None:
        return None, "", 0
    stat = get_train_task(str(uuid), connection)
    if stat == 1:
        return stat, "", 0
    elif stat == 0:
        model = get_model_for_name(str(uuid), connection)
        return stat, model
    else:
        return stat, "", 0


def exists_model(model_name):
    try:
        get_model_for_name(model_name, connection)
    except Exception as e:
        log.error(f"Model with name %s not exists", model_name)
        return False
    return True
