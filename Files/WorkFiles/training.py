import pandas as pd
import argparse
import os
import re
from bs4 import BeautifulSoup
import joblib


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-path_to_file')
    parser.add_argument('-path_to_model')
    parser.add_argument('-uuid')
    return parser


def clean_str(string):
    """
    Tokenization/string cleaning for dataset
    Every dataset is lower cased except
    """
    string = re.sub(r"\\", "", string)
    string = re.sub(r"\'", "", string)
    string = re.sub(r"\"", "", string)
    return string.strip().lower()


def clear_data(data):
    texts = []
    labels = []
    for idx in range(data.content.shape[0]):
        try:
            text = BeautifulSoup(data.content[idx])
            texts.append(clean_str(text.get_text()))
            labels.append(data.label[idx])
        except:
            print(idx)
    return texts, labels


def training(X, y, model, uuid):
    '''
    :X: content
    :y: labels
    :model: path to model
    :return: vector with classes
    '''
    loaded_rf = joblib.load(model)
    loaded_rf.fit(X, y)
    joblib.dump(loaded_rf, "./Files/Models/" + uuid + ".joblib")
    print(f"The new version of the model is saved in {uuid + '.joblib'}")


if __name__ == '__main__':
    # get args
    parser = createParser()
    namespace = parser.parse_args()
    file = namespace.path_to_file
    model = namespace.path_to_model
    uuid = namespace.uuid

    # read file
    if '.xlsx' in file or '.xls' in file:
        df = pd.read_excel(file)
        df.to_csv(f'./Files/Train/{os.path.splitext(os.path.basename(file))[0]}.csv')
    data_for_predict = pd.read_csv(f'server/Files/Train/{os.path.splitext(os.path.basename(file))[0]}.csv')

    # preproccessing data
    data = pd.DataFrame()
    data['content'] = data_for_predict['Comments']
    data['label'] = data_for_predict['Predict']
    data.dropna()
    X, y = clear_data(data)

    # training
    training(X, y, model, uuid)
