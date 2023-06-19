import api.response.response_model_class as response


def converter_model_to_api(model: list):
    """
    Конвертирует модель в представление для слоя API
    :param model: список содержащий параметры модели
    :return: Response.ResponseModel
    """
    return response.ResponseModel(ID=model[0], NameModel=model[1], score=model[3], Active=model[4])


def converter_model_list_to_api(models: list):
    """
    Конвертирует список моделей в представление для слоя API
    :param models: Список моделей
    :return: Response.ResponseListModels
    """
    final_models = list()
    for model in models:
        mod = response.ResponseModel(ID=model[0], NameModel=model[1], score=model[3], Active=model[4])
        final_models.append(mod)
    return response.ResponseListModels(models=final_models)
