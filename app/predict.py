import os
import uuid as u
import subprocess
from app.models import current_models
from app.parser import write_to_file, read_from_file
from dal.dal import add_new_predict_task, set_predict_status, get_predict_task
from cm.main import PYTHON_PATH, NAME_FILE_PREDICT, status_subprocess_predict, connection


def start(request):
    uuid = u.uuid1()
    write_to_file(request.comments, uuid, 1)
    sp = subprocess.Popen(
        [PYTHON_PATH, os.path.join('.\\', NAME_FILE_PREDICT), '-uuid', str(uuid), '-model', str(current_models)])
    if sp.stderr is not None:
        return 0, sp.stderr
    status_subprocess_predict.update({uuid: sp})
    add_new_predict_task(str(uuid), request.userID, 1, connection)
    return uuid, None


def status(request):
    uuid = request.uuid
    subpr = status_subprocess_predict.get(u.UUID(uuid))
    if subpr is None:
        return subpr, 0
    return_code = subpr.poll()  # Получение информации о статусе подпроцесса. Завершен, в процессе, прерван.
    if return_code is None:
        set_predict_status(str(uuid), 1, connection)
    elif return_code == 0:
        set_predict_status(str(uuid), 0, connection)
    else:
        set_predict_status(str(uuid), -1, connection)
    return subpr, return_code


def result(request):
    uuid = request.uuid
    subpr = status_subprocess_predict.get(u.UUID(uuid))
    if subpr is None:
        return None, []
    stat = get_predict_task(str(uuid), connection)
    if stat == 1:
        return stat, []
    elif stat == 0:
        if os.path.isfile('./Files/Predict/Finish/' + str(uuid) + '.csv'):
            ls = read_from_file(uuid, 1)
            return stat, ls
        return stat, []
    else:
        return stat, []
