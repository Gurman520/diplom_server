import psycopg2
import logging as log


def create_connection(BD_HOST, BD_PORT):
    """
    Создание соединения с БД, а так же добавление таблиц в БД, если они не найдены в БД
    :return: соединение с БД
    """
    try:
        conn = psycopg2.connect(
            host=BD_HOST,
            port=BD_PORT,
            database="server",
            user="admin",
            password="pgpwd4habr"
        )
    except:
        log.error("Error connection BD. Server run with out BD.")
        return None
    if not exists_table(conn):
        create_table(conn)
    else:
        log.info("Tables exist")
    log.info(f"Connection BD successful. Host = %s, Port = %s", BD_HOST, BD_PORT)
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
        nameModel TEXT,
        fileName TEXT,
        score REAL,
        toDoWork bool);
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS train(
        trainID SERIAL PRIMARY KEY,
        uuid TEXT,
        userid INTEGER,
        status INT,
        modelID INT);
    """)

    cur.execute(
        "INSERT INTO Models (nameModel, fileName, score ,toDoWork) VALUES ('startModel', 'startModel', 85, true);")
    conn.commit()
    cur.close()
    log.info("Create 3 tables successful")
    log.info("Start model create successful")


def get_work_train(conn):
    cur = conn.cursor()
    select_query = "SELECT uuid, modelID FROM train WHERE status = 1"
    cur.execute(select_query)
    pred_task = cur.fetchall()
    conn.commit()
    cur.close()
    return pred_task


def get_work_predict(conn):
    cur = conn.cursor()
    select_query = "SELECT uuid, modelID FROM predict WHERE status = 1"
    cur.execute(select_query)
    pred_task = cur.fetchall()
    conn.commit()
    cur.close()
    return pred_task
