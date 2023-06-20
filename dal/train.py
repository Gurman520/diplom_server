import psycopg2
import logging as log


def add_new_train_task(uuid, user_id, modelID, conn):
    """
    Добавление новой задачи обучения
    :param uuid: Уникальный идентификатор задачи
    :param user_id: Уникальный идентификатор пользователя
    :param conn: Соединение с БД
    :return: None
    """
    cur = conn.cursor()
    add_query = "INSERT INTO train (uuid, userid, status, modelID) VALUES(%s, %s, %s, %s);"
    cur.execute(add_query, (uuid, user_id, int(1), modelID))
    conn.commit()
    cur.close()


def set_train_status(uuid, status, conn):
    """
    Установить новый статус задачи обучения
    :param uuid: Уникалььный идентификатор задачи
    :param status: Статус задачи
    :param conn: Соединение с БД
    :return: None
    """
    cur = conn.cursor()
    set_query = "Update train set status = %s where uuid = %s"
    cur.execute(set_query, (status, uuid))
    conn.commit()
    cur.close()


def get_train_task(uuid: str, conn):
    """
    Получение статуса задачи
    :param uuid: Уникальный идентификатор задачи
    :param conn: Соединение с БД
    :return: Статус
    """
    cur = conn.cursor()
    select_query = "SELECT status FROM train WHERE uuid = %s"
    cur.execute(select_query, (uuid,))
    train_task = cur.fetchall()
    result = train_task[0][0]
    conn.commit()
    cur.close()
    return result