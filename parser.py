import pandas as pd


def parse_out(ls: list, uuid):
    my_df = pd.DataFrame(ls)
    my_df.to_csv(uuid + '.csv', index=False, header=False)


def parse_in():
    pass
