description = """
Данный сервер может производить анализ комментариев на предмет экстремизма
"""

tags_metadata = [
    {
        "name": "predict",
        "description": "Анализ комментариев на предмет экстремизма"
    },
    {
        "name": "models",
        "description": "Методы по работе с уже обученными моделями"
    },
    {
        "name": "teach",
        "description": "Методы по работе с обучением новых моделей"
    }
]

des_pred_info = "Если попытаться запросить Result раньше, чем получен Finish будет получено сообщение вида {'Message' " \
                ": 'Процесс анализа не завершен.'} \n В случае отправки запроса с несуществующим uuid будет получен " \
                "ответ {'Message': 'Задачи с таким uuid не сущетствует'}\n В слачае возникновения ошибки с " \
                "формированием ответа будет получено 'Message': 'Проблема с формированием файла с результами' "

des_pred_status = "При попытке обратится с неверным uuid, то будет отправлен ответ вида {'Message': 'Задачи с таким " \
                  "uuid не сущетствует'}\n" \
                  "В случае возникновения ошибки в работе алгоритма анализа, будет отправлено сообщение {'Message': " \
                  "'Ошибка в работе алгоритма анализа. Returncode: (код ошибки)'} " \
                  "Если задача выполняется, то будет сообщение Proccesing, если завершено, то Finish"

des_pred_start = "В случае ошибки запуска анализа, будет отправлено сообщение {'Message': 'Ошибка запуска аналиаз: (" \
                 "текст ошибки)'} "

des_model_put = "Если модель с таким ID не была найдена, то будет отправлено сообщение 'Message': 'Такой модели не существует.' с кодом ошибки 404"

des_model_delete = "Если модель является основной, которую сейчас используют, то удалить ее нельзя и будет отправлен ответ {'Message': 'Модель является основной'} с кодом 400" \
    "Если модель небыла найдена, то будет отправлен ответ {'Message': 'Такой модели не существует.'} с кодом 404"

des_train_result = "Если попытаться запросить Result раньше, чем получен Finish будет получено сообщение вида {'Message' " \
                ": 'Процесс обучения не завершен.'} \n В случае отправки запроса с несуществующим uuid будет получен " \
                "ответ {'Message': 'Задачи с таким uuid не сущетствует'}\n В слачае возникновения ошибки в " \
                "работе алгоритма обучения будет отправлен ответ 'Message': 'Ошибка в работе алгоритма обучения. Returncode: (код ошибки)' "

des_train_status = "При попытке обратится с неверным uuid, то будет отправлен ответ вида {'Message': 'Задачи с таким " \
                  "uuid не сущетствует'}\n" \
                  "В случае возникновения ошибки в работе алгоритма обучения, будет отправлено сообщение {'Message': " \
                  "'Ошибка в работе алгоритма обучения. Returncode: (код ошибки)'} " \
                  "Если задача выполняется, то будет сообщение Proccesing, если завершено, то Finish"

des_train_start = "В случае ошибки запуска обучения, будет отправлено сообщение {'Message': 'Ошибка запуска обучения: (" \
                 "текст ошибки)'} "