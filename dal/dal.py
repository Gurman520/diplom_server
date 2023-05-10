# from main import conn
# import sqlite3
import psycopg2


# TODO: Добавить реализацию работы с БД

def create_connection():
    """
    Создание коннекшина с базой дагнных
    Если файл БД небыл обнаружен, то будет произведено создание файла и создание всех необходимых таблиц.
    :return: connection к БД
    """
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="server",
        user="admin",
        password="pgpwd4habr"
    )
    create_table(conn)
    return conn
    # conn = sqlite3.connect(r'./dal/bd/' + name_bd)
    # cursor = conn.cursor()
    # create_table(cursor)
    # conn.commit()
    # conn.close()


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

    cur.execute("""CREATE TABLE IF NOT EXISTS models(
           ID SERIAL PRIMARY KEY,
           nameFile TEXT,
           nameModel TEXT,
           score REAL);
        """)

    cur.execute("""CREATE TABLE IF NOT EXISTS train(
           trainID SERIAL PRIMARY KEY,
           uuid TEXT,
           userid INTEGER,
           status INT,
           nameFile TEXT);
        """)
    conn.commit()
    cur.close()


def add_new_predict_task(uuid, user_id, model_id, conn):
    """
    Добавление новой записи об анализе текста
    :param uuid:
    :param user_id:
    :param model_id:
    :param conn:
    :return:
    """

    cur = conn.cursor()
    cur.execute(f"""INSERT INTO predict (uuid, userid, status, modelID) 
       VALUES(%s, %s, %s, %s);""", (uuid, user_id, int(1), model_id))
    conn.commit()
    cur.close()


def get_list_predict_task(conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM predict')
    for row in cur:
        print(row)
    conn.commit()
    cur.close()


def add_new_train_task(uuid):
    pass


def delete_train_task(uuid):
    pass


def add_new_model(name_model, accuracy):
    pass


def delete_model(name_model):
    pass


def get_list_models():
    pass
