import os
import uuid as u
import subprocess
import logging as log
from app.parser import write_to_file, read_from_file
import dal.predict as dal
from dal.models import get_basic_model
from cm.main import connection
from cm.config import Config

status_subprocess_predict = dict()  # Словарь, который хранит информацию о всех запущенных процессах.
pathModel = "./Files/Models/"


def start(request):
    uuid = u.uuid4()
    write_to_file(request.comments, uuid, 1)
    model = get_basic_model(connection)
    print(os.path.join('./', Config.NAME_FILE_PREDICT))
    sp = subprocess.Popen(
        [Config.PYTHON_PATH, os.path.join('./', Config.NAME_FILE_PREDICT), '-path_to_file', str(uuid),
         '-path_to_model', pathModel + model[1] + ".joblib"])
    if sp.stderr is not None:
        log.error(f"APP - predict - error start %s", sp.stderr)
        return 0, sp.stderr
    status_subprocess_predict.update({uuid: sp})
    dal.add_new_predict_task(str(uuid), request.userID, model[0], connection)
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
        dal.set_predict_status(str(uuid), 1, connection)
    elif return_code == 0:
        log.info("APP - predict status - finish")
        dal.set_predict_status(str(uuid), 0, connection)
    else:
        log.info("APP - predict status - error")
        dal.set_predict_status(str(uuid), -1, connection)
    return subpr, return_code


def result(req_uuid):
    uuid = u.UUID(req_uuid)
    subpr = status_subprocess_predict.get(uuid)
    if subpr is None:
        log.error("APP - predict result - task not found")
        return None, []
    stat = dal.get_predict_task(str(uuid), connection)
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
