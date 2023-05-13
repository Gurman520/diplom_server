import psycopg2
import logging as log


def create_connection():
    """
    Создание соединения с БД, а так же добавление таблиц в БД, если они не найдены в БД
    :return: соединение с БД
    """
    try:
        conn = psycopg2.connect(
            host="",
            port=5432,
            database="server",
            user="admin",
            password="pgpwd4habr"
        )
    except:
        log.error("Error connection BD. Server run with out BD.")
        return None
    if not exists_table(conn):
        create_table(conn)
    log.info("Connection BD successful")
    return conn


def exists_table(conn):
    """
    Проверка существования таблиц в БД
    :param conn: Соединение с БД
    :return: True or False
    """
    cur = conn.cursor()
    cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('predict',))
    return cur.fetchone()[0]


def create_table(conn):
    """
    Создание таблиц в БД
    :param conn: соединение с БД
    :return: None
    """
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS predict(
       predictID SERIAL PRIMARY KEY,
       uuid TEXT,
       userid INTEGER,
       status INT,
       modelID INT);
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS Models(
        ID SERIAL PRIMARY KEY,
        nameFile TEXT,
        nameModel TEXT,
        score REAL,
        toDoWork bool);
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS train(
        trainID SERIAL PRIMARY KEY,
        uuid TEXT,
        userid INTEGER,
        status INT);
    """)

    cur.execute(
        "INSERT INTO Models (nameFile, nameModel, score ,toDoWork) VALUES ('startModel.h5', 'startModel', 85, true);")
    conn.commit()
    cur.close()
    log.info("Create table successful")


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
    return model[0][2]


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


def set_basic_model(name_model, conn):
    """
    Установить новую основную модель
    :param name_model: Имя новой модели
    :param conn: Соединение с БД
    :return: Возвращает вызов имя основной модели
    """
    cur = conn.cursor()
    set_false_model = "Update Models set toDoWork = %s where toDoWork = %s"
    set_true_model = "Update Models set toDoWork = %s WHERE nameModel = %s"
    cur.execute(set_false_model, (False, True))
    conn.commit()
    cur.execute(set_true_model, (True, name_model))
    conn.commit()
    cur.close()
    return get_basic_model(conn)


def add_new_model(name_file, name_model, score, conn):
    """
    Добавление новой модели в БД
    :param name_file:
    :param name_model: Имя модели
    :param score: Оценка модели
    :param conn: Соединение с БД
    :return:
    """
    cur = conn.cursor()
    add_model_query = "INSERT INTO Models (nameFile, nameModel, score, toDoWork) VALUES(%s, %s, %s, %s);"
    cur.execute(add_model_query, (name_file, name_model, score, False))
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


def add_new_train_task(uuid, user_id, conn):
    """
    Добавление новой задачи обучения
    :param uuid: Уникальный идентификатор задачи
    :param user_id: Уникальный идентификатор пользователя
    :param conn: Соединение с БД
    :return: None
    """
    cur = conn.cursor()
    add_query = "INSERT INTO train (uuid, userid, status) VALUES(%s, %s, %s);"
    cur.execute(add_query, (uuid, user_id, int(1)))
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
