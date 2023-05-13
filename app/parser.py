import pandas as pd


def write_to_file(ls: list, uuid, status: int):
    """
        write_to_file(ls: list, uuid, status: int)
        Функция отвечающая за запись данных в файл, который потом будет использоваться для анализа или обучения
        status - int число, которое определяет, какой файл необходимо записать.
        1 - Файл для анализа (predict)
        0 - Файл для обучения (train)
        ls - список, содержащий комментарии
        В случаии status == 1 будет содержать список списков ["commentary", "Predict"]
    """
    if status == 1:
        name_file = "./Files/Predict file/" + str(uuid) + '.csv'
        list_in_dict = {"Comments": ls}
        my_df = pd.DataFrame(list_in_dict)
        my_df.to_csv(name_file, index=False)
    elif status == 0:
        name_file = "./Files/Train file/" + str(uuid) + '.csv'
        list_in_dict = {"Comments": [], "Predict": []}
        for i in ls:
            list_in_dict["Comments"].append(i[0])
            list_in_dict["Predict"].append(i[1])
        my_df = pd.DataFrame(list_in_dict)
        my_df.to_csv(name_file, index=False)


def read_from_file(uuid, status: int):
    """
        Функция отвечает за получение информации из файла и последующей передачи в виде списка
        read_to_file(ls: list, uuid, status: int)
        status - int число, которое определяет, какой тип файла необходимо прочитать.
        1 - Файл с результатами анализа (predict)
        0 - Файл с результатами обучения (train)
        ls - список, содержащий комментарии
        В случаии status == 1 будет содержать список списков ["commentary", "Result Predict"]
    """
    if status == 1:
        name_file = "./Files/FinishPredict/" + str(uuid) + '.csv'
        my_df = pd.read_csv(name_file)
        ls = my_df.values.tolist()
        return ls
    if status == 0:
        name_file = "./Train/result/" + str(uuid) + '.csv'
        my_df = pd.read_csv(name_file)
        ls = [my_df["Comments"], my_df["Result Predict"]]
        print(ls)
        return ls
