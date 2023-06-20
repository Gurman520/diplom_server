import os
from dal.models import get_basic_model, get_list_models, set_basic_model, get_model, delete_model_sql, \
    rename_model as rename
from cm.main import connection
import logging as log


def rename_model(name_model, model_id):
    if exists_model(model_id):
        model = rename(connection, name_model, model_id)
        return model
    return None


def list_model():
    log.info("APP list models")
    ls = get_list_models(connection)
    return ls


def get_current_model():
    log.info("APP get current model")
    model = get_basic_model(connection)
    return model


def current_model():
    model = get_basic_model(connection)
    return model[0]


def set_model(model_id):
    log.info("APP Set new model for current")
    if exists_model(model_id):
        model = set_basic_model(model_id, connection)
        return model
    return None


def delete_model(model_id):
    # Добавить проверку существования
    model = get_model(model_id, connection)
    if model[3]:
        log.error("APP - Delete model - current model")
        return None, "Current model"
    if os.path.isfile('./Files/Models/' + model[1]):
        os.remove('./Files/Models/' + model[1])
        delete_model_sql(model_id, connection)
        log.info("APP - Delete model")
        return model, "OK"
    log.error("APP - Delete model - Not found model")
    return None, "File not Found"


def exists_model(model_id):
    try:
        get_model(model_id, connection)
    except Exception as e:
        log.error(f"Model with ID %s not exists", model_id)
        return False
    log.info("APP - model is exists")
    return True
