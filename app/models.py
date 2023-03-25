import os


def list_models():
    return [["Model 1", 87], ["Model 2", 67]]


def current_model():
    # TODO: продумать логику получения текущей модели
    return "model1"


def set_models(name_models):
    global current_models
    current_models = name_models
    return "OK"


def delete_model(model_id):
    name_model = "TEST"
    # TODO: Добавить получение имени файла по ID модели.
    if os.path.isfile('./Files/Models/' + name_model + '.h5'):
        os.remove('./Files/Models/' + name_model + '.h5')
    return 0


current_models = current_model()
