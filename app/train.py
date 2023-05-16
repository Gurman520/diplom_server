import os
import uuid as u
import subprocess
from app.parser import write_to_file
from dal.dal import add_new_train_task, set_train_status, get_train_task, get_model_for_name
from cm.main import PYTHON_PATH, NAME_FILE_TRAIN, status_subprocess_train, connection


def start(request):
    uuid = u.uuid4()
    write_to_file(request.file, uuid, 0)
    sp = subprocess.Popen(
        [PYTHON_PATH, os.path.join('.\\', NAME_FILE_TRAIN), '-uuid', str(uuid)])
    if sp.stderr is not None:
        return 0, sp.stderr
    status_subprocess_train.update({uuid: sp})
    add_new_train_task(str(uuid), request.userID, connection)
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
        model = get_model_for_name(uuid, connection)
        return stat, model[1], model[3]
    else:
        return stat, "", 0
