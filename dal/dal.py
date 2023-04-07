# from main import conn
import sqlite3


# TODO: Добавить реализацию работы с БД

def create_connection(name_bd):
    """
    Создание коннекшина с базой дагнных
    Если файл БД небыл обнаружен, то будет произведено создание файла и создание всех необходимых таблиц.
    :return: connection к БД
    """
    conn = sqlite3.connect(r'./dal/bd/' + name_bd)
    cursor = conn.cursor()
    create_table(cursor)
    conn.commit()
    return cursor


def create_table(cur):
    cur.execute("""CREATE TABLE IF NOT EXISTS predict(
       orderID INT PRIMARY KEY,
       uuid TEXT,
       userid TEXT,
       status INT,
       modelID INT);
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS models(
           ID INT PRIMARY KEY,
           nameFile TEXT,
           nameModel TEXT,
           score REAL);
        """)

    cur.execute("""CREATE TABLE IF NOT EXISTS train(
           trainID INT PRIMARY KEY,
           uuid TEXT,
           userid TEXT,
           status INT,
           nameFile TEXT);
        """)


def add_new_predict_task(uuid):
    pass


def delete_predict_task(uuid):
    pass


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
