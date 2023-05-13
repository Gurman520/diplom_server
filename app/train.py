import os
import uuid as u
import subprocess
from app.parser import write_to_file, read_from_file
from dal.dal import add_new_train_task, set_train_status, get_train_task
from cm.main import PYTHON_PATH, NAME_FILE_TRAIN, status_subprocess_train, connection


def start(request):
    uuid = u.uuid1()
    write_to_file(request.file, uuid, 0)
    sp = subprocess.Popen(
        [PYTHON_PATH, os.path.join('.\\', NAME_FILE_TRAIN), '-uuid', str(uuid)])
    if sp.stderr is not None:
        return 0, sp.stderr
    status_subprocess_train.update({uuid: sp})
    add_new_train_task(str(uuid), request.userID, connection)
    return uuid, None


def status(request):
    uuid = request.uuid
    subpr = status_subprocess_train.get(u.UUID(uuid))
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


def result(request):
    uuid = request.uuid
    subpr = status_subprocess_train.get(u.UUID(uuid))
    if subpr is None:
        return None, []
    stat = get_train_task(str(uuid), connection)
    if stat == 1:
        return stat, []
    elif stat == 0:
        if os.path.isfile('./Files/Train/result/' + str(uuid) + '.csv'):
            ls = read_from_file(uuid, 0)
            return stat, ls
        return stat, []
    else:
        return stat, []
