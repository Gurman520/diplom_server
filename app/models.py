import os
from dal.dal import get_basic_model, get_list_models, set_basic_model, get_model, delete_model_sql
from cm.main import connection
import logging as log


def list_model():
    ls = get_list_models(connection)
    return ls


def get_current_model():
    model = get_basic_model(connection)
    return model


def current_model():
    model = get_basic_model(connection)
    return model[0]


def set_model(model_id):
    global current_models
    if exists_model(model_id):
        model = set_basic_model(model_id, connection)
        current_models = model[0]
        return model
    return None


def delete_model(model_id):
    model = get_model(model_id, connection)
    if model[3]:
        return None, "Current model"
    if os.path.isfile('./Files/Models/' + model[1]):
        os.remove('./Files/Models/' + model[1])
        delete_model_sql(model_id, connection)
        return model, "OK"
    return None, "File not Found"


def exists_model(model_id):
    try:
        get_model(model_id, connection)
    except Exception as e:
        log.error(f"Model with ID %s not exists", model_id)
        return False
    return True


current_models = current_model()
