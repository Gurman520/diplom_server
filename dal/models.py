import psycopg2
import logging as log


def get_basic_model(conn):
    """
    Получение текущей основной модели (Та что используется для всех анализов текста)
    :param conn: Соединение с БД
    :return: Имя модели
    """
    cur = conn.cursor()
    get_query = "SELECT * from Models where toDoWork = true"
    cur.execute(get_query)
    model = cur.fetchall()
    conn.commit()
    cur.close()
    return model[0]


def get_list_models(conn):
    """
    Получение списка моделей
    :param conn: Соединение с БД
    :return: Список моделей
    """
    cur = conn.cursor()
    get_list_query = "SELECT * FROM Models"
    cur.execute(get_list_query)
    ls_models = cur.fetchall()
    conn.commit()
    cur.close()
    return ls_models


def set_basic_model(model_id, conn):
    """
    Установить новую основную модель
    :param model_id: Имя новой модели
    :param conn: Соединение с БД
    :return: Возвращает вызов имя основной модели
    """
    cur = conn.cursor()
    set_false_model = "Update Models set toDoWork = %s where toDoWork = %s"
    set_true_model = "Update Models set toDoWork = %s WHERE id = %s"
    cur.execute(set_false_model, (False, True))
    conn.commit()
    cur.execute(set_true_model, (True, model_id))
    conn.commit()
    cur.close()
    return get_basic_model(conn)


def add_new_model(name_model: str, score, conn):
    """
    Добавление новой модели в БД
    :param name_model: Имя модели
    :param score: Оценка модели
    :param conn: Соединение с БД
    :return:
    """
    cur = conn.cursor()
    add_model_query = "INSERT INTO Models (nameModel, fileName, score, toDoWork) VALUES(%s, %s, %s);"
    cur.execute(add_model_query, (name_model, name_model, score, False))
    conn.commit()
    cur.close()
    return get_model_for_name(name_model, conn)


def get_model(model_id, conn):
    """
    Получение модели по model_id
    :param model_id: Уникальный идентификатор модели
    :param conn: Соединение с БД
    :return: Модель
    """
    cur = conn.cursor()
    get_model_query = "SELECT * FROM models WHERE id = %s"
    cur.execute(get_model_query, (model_id,))
    conn.commit()
    model = cur.fetchall()
    cur.close()
    return model[0]


def get_model_for_name(model_name, conn):
    """
    Получение модели по model_name
    :param model_name: Имя модели
    :param conn: Соединение с БД
    :return: Модель
    """
    cur = conn.cursor()
    get_model_query = "SELECT * FROM models WHERE nameModel = %s"
    cur.execute(get_model_query, (model_name,))
    conn.commit()
    model = cur.fetchall()
    cur.close()
    return model[0]


def delete_model_sql(model_id, conn):
    """
    Удаление модели из БД
    :param model_id: Иникальный идентификатор модели
    :param conn: Соединение с БД
    :return: None
    """
    cur = conn.cursor()
    delete_query = "Delete from models where id = %s"
    cur.execute(delete_query, (model_id,))
    conn.commit()
    cur.close()


def rename_model(conn, name_model: str, model_id: int):
    """
    Добавление модели имени понятного пользователю
    :param conn: Соединение с БД
    :param name_model: Имя модели
    :param model_id: Уникальный идентификатор модели
    :return:
    """
    cur = conn.cursor()
    rename_query = "Update Models set nameModel = %s where ID = %s"
    cur.execute(rename_query, (name_model, model_id))
    conn.commit()
    cur.close()
    return get_model(model_id, conn)
