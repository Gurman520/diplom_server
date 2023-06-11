import os
import uuid as u
import subprocess
import logging as log
from app.models import current_models
from app.parser import write_to_file, read_from_file
from dal.dal import add_new_predict_task, set_predict_status, get_predict_task, get_basic_model
from cm.main import PYTHON_PATH, NAME_FILE_PREDICT, status_subprocess_predict, connection

pathModel = "./Files/Models/"


def start(request):
    uuid = u.uuid4()
    write_to_file(request.comments, uuid, 1)
    model = get_basic_model(connection)
    sp = subprocess.Popen(
        [PYTHON_PATH, os.path.join('.\\', NAME_FILE_PREDICT), '-path_to_file', str(uuid),
         '-path_to_model', pathModel + model[1] + ".joblib"])
    if sp.stderr is not None:
        log.error(f"APP - predict - error start %s", sp.stderr)
        return 0, sp.stderr
    status_subprocess_predict.update({uuid: sp})
    add_new_predict_task(str(uuid), request.userID, current_models, connection)
    log.info("APP - predict - success")
    return uuid, None


def status(req_uuid):
    uuid = u.UUID(req_uuid)
    subpr = status_subprocess_predict.get(uuid)
    if subpr is None:
        log.error("APP - predict status - task not found")
        return subpr, 0
    return_code = subpr.poll()  # Получение информации о статусе подпроцесса. Завершен, в процессе, прерван.
    if return_code is None:
        log.info("APP - predict status - processing")
        set_predict_status(str(uuid), 1, connection)
    elif return_code == 0:
        log.info("APP - predict status - finish")
        set_predict_status(str(uuid), 0, connection)
    else:
        log.info("APP - predict status - error")
        set_predict_status(str(uuid), -1, connection)
    return subpr, return_code


def result(req_uuid):
    uuid = u.UUID(req_uuid)
    subpr = status_subprocess_predict.get(uuid)
    if subpr is None:
        log.error("APP - predict result - task not found")
        return None, []
    stat = get_predict_task(str(uuid), connection)
    if stat == 1:
        return stat, []
    elif stat == 0:
        if os.path.isfile('./Files/Predict/Finish/' + str(uuid) + '.csv'):
            ls = read_from_file(uuid, 1)
            return stat, ls
        log.error(f"APP - predict result - file %s not found", uuid)
        return stat, []
    else:
        return stat, []
