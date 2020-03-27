import pandas as pd
from configparser import ConfigParser


def get_min_date(dfs):
    for canton, df in dfs.items():
        df["date"].min


def main():
    parser = ConfigParser()
    parser.read("sources.ini")

    cases = {}
    fatalities = {}

    dfs = {}
    for i in parser["cantonal"]:
        dfs[i.upper()] = pd.read_csv(parser["cantonal"][i], index_col=[0])

    print(dfs)
    # get_min_date(dfs)


if __name__ == "__main__":
    main()
