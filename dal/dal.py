import psycopg2
import logging as log

log.basicConfig(level=log.INFO, filename="./Files/log file/dal.log", filemode="a",
                format="%(asctime)s %(levelname)s %(message)s")


def create_connection():
    """
    Создание коннекшина с базой дагнных
    Если файл БД небыл обнаружен, то будет произведено создание файла и создание всех необходимых таблиц.
    :return: connection к БД
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
    cur = conn.cursor()
    cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('predict',))
    return cur.fetchone()[0]


def create_table(conn):
    """
    Функция создает таблицы, необходимые для работы проекта
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
           status INT,
           nameFile TEXT);
        """)

    cur.execute(
        "INSERT INTO Models (nameFile, nameModel, score ,toDoWork) VALUES ('startModel.h5', 'startModel', 85, true);")
    conn.commit()
    cur.close()
    log.info("Create table successful")


def add_new_predict_task(uuid, user_id, model_id, conn):
    """
    Добавление новой записи об анализе текста
    :param uuid:
    :param user_id:
    :param model_id:
    :param conn:
    :return:
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


def get_list_predict_task(conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM predict')
    for row in cur:
        print(row)
    conn.commit()
    cur.close()


def get_predict_task(uuid: str, conn):
    cur = conn.cursor()
    select_query = "SELECT status FROM predict WHERE uuid = %s"
    cur.execute(select_query, (uuid,))
    pred_task = cur.fetchall()
    result = pred_task[0][0]
    conn.commit()
    cur.close()
    return result


def set_predict_status(uuid: str, status: int, conn):
    cur = conn.cursor()
    update_query = "Update predict set status = %s where uuid = %s"
    cur.execute(update_query, (status, uuid))
    conn.commit()
    cur.close()


def get_basic_model(conn):
    cur = conn.cursor()
    get_query = "SELECT * from Models where toDoWork = true"
    cur.execute(get_query)
    model = cur.fetchall()
    conn.commit()
    cur.close()
    return model[0][2]


def get_list_models(conn):
    cur = conn.cursor()
    get_list_query = "SELECT * FROM Models"
    cur.execute(get_list_query)
    ls_models = cur.fetchall()
    conn.commit()
    cur.close()
    return ls_models


def set_basic_model(name_model, conn):
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
    cur = conn.cursor()
    add_model_query = "INSERT INTO Models (nameFile, nameModel, score, toDoWork) VALUES(%s, %s, %s, %s);"
    cur.execute(add_model_query, (name_file, name_model, score, False))
    conn.commit()
    cur.close()


def get_model(model_id, conn):
    cur = conn.cursor()
    get_model_query = "SELECT * FROM models WHERE id = %s"
    cur.execute(get_model_query, (model_id,))
    conn.commit()
    model = cur.fetchall()
    cur.close()
    return model[0]


def get_model_for_name(model_name, conn):
    cur = conn.cursor()
    get_model_query = "SELECT * FROM models WHERE nameModel = %s"
    cur.execute(get_model_query, (model_name,))
    conn.commit()
    model = cur.fetchall()
    cur.close()
    return model[0]


def delete_model_sql(model_id, conn):
    cur = conn.cursor()
    delete_query = "Delete from models where id = %s"
    cur.execute(delete_query, (model_id, ))
    conn.commit()
    cur.close()



def add_new_train_task(uuid):
    pass


def delete_train_task(uuid):
    pass
