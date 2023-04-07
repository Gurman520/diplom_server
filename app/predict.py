import os
import uuid as u
import subprocess
from app.parser import write_to_file, read_from_file
from main import PYTHON_PATH, status_subprocess_predict


def start(request):
    uuid = u.uuid1()
    write_to_file(request.comments, uuid, 1)
    sp = subprocess.Popen(
        [PYTHON_PATH, os.path.join('..', 'logic.py '), '-uuid', str(uuid)])
    if sp.stderr is not None:
        return 0, sp.stderr
    status_subprocess_predict.update({uuid: sp})
    return uuid, None


def status(request):
    uuid = request.uuid
    subpr = status_subprocess_predict.get(u.UUID(uuid))
    if subpr is None:
        return subpr, 0
    return_code = subpr.poll()  # Получение информации о статусе подпроцесса. Завершен, в процессе, прерван.
    return subpr, return_code


def result(request):
    uuid = request.uuid
    s = status_subprocess_predict.get(u.UUID(uuid))
    if s is None:
        return s, []
    if os.path.isfile('./FinishPredict/' + str(uuid) + '.csv'):
        ls = read_from_file(uuid, 1)
        print(ls)
        return s, ls
    return s, []
