import psycopg2
import logging as log


def add_new_predict_task(uuid, user_id, model_id, conn):
    """
    Добавление новой записи об анализе текста
    :param uuid: Уникальный идентификатор задачи
    :param user_id: Идентификатор пользователя в основной системе
    :param model_id: Идентификатор модели
    :param conn: Соединение с БД
    :return: None
    """
    try:
        cur = conn.cursor()
        cur.execute(f"""INSERT INTO predict (uuid, userid, status, modelID) 
           VALUES(%s, %s, %s, %s);""", (uuid, user_id, int(1), model_id))
        conn.commit()
        cur.close()
    except Exception as e:
        log.error("Error add new predict task")
    else:
        log.info("New predict task add successful")


def get_predict_task(uuid: str, conn):
    """
    Получение статуса задачи анализа
    :param uuid: Уникальный идентификатор задачи
    :param conn: Соединение с БД
    :return: Возвращает статус выполнения задачи
    """
    cur = conn.cursor()
    select_query = "SELECT status FROM predict WHERE uuid = %s"
    cur.execute(select_query, (uuid,))
    pred_task = cur.fetchall()
    result = pred_task[0][0]
    conn.commit()
    cur.close()
    return result


def set_predict_status(uuid: str, status: int, conn):
    """
    Установить статус задачи анализа
    :param uuid: Уникальный идентификатор задачи
    :param status: Новый статус задачи
    :param conn: Соединение с БД
    :return: None
    """
    cur = conn.cursor()
    update_query = "Update predict set status = %s where uuid = %s"
    cur.execute(update_query, (status, uuid))
    conn.commit()
    cur.close()