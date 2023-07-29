from os import getenv


class Config(object):
    DB_PORT = int(getenv('DB_PORT', default=5432))
    DB_HOST = getenv('DB_HOST', default='localhost')
    DB_NAME = getenv('DB_NAME', default='server')
    DB_USER = getenv('DB_USER', default='admin')
    DB_PASSWORD = getenv('DB_PASSWORD', default='pgpwd4habr')
    PYTHON_PATH = getenv('PYTHON_PATH', default='usr/bin/python3')
    NAME_FILE_PREDICT = getenv('FILE_PREDICT', default='Files/WorkFiles/get_predict.py')
    NAME_FILE_TRAIN = getenv('FILE_TRAIN', default='Files/WorkFiles/training.py')
