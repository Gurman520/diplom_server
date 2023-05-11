import os
from dal.dal import get_basic_model, get_list_models, set_basic_model, get_model, get_model_for_name, delete_model_sql
from cmd.main import connection
import logging as log

log.basicConfig(level=log.INFO, filename="./log file/app_models.log", filemode="a",
                format="%(asctime)s %(levelname)s %(message)s")


def list_model():
    ls = get_list_models(connection)
    return ls


def current_model():
    name_model = get_basic_model(connection)
    return name_model


def set_model(name_model):
    global current_models
    if exists_model(name_model):
        name = set_basic_model(name_model, connection)
        current_models = name
        return name
    return None


def delete_model(model_id):
    model = get_model(model_id, connection)
    # Так же можно добавить проаерку, что перед удалением, необходимо удостоверится, что модель не используется в каких либо задачах
    if model[4]:
        return None, "Current model"
    if os.path.isfile('./Files/Models/' + model[1]):
        os.remove('./Files/Models/' + model[1])
        delete_model_sql(model_id, connection)
        return model[2], "OK"
    return None, "File not Found"


def exists_model(name_model):
    try:
        get_model_for_name(name_model, connection)
    except Exception as e:
        log.error(f"Model %s not exists", name_model)
        return False
    return True


current_models = current_model()
