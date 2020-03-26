import pandas as pd
from configparser import ConfigParser


def main():
    parser = ConfigParser()
    parser.read("sources.ini")

    cases = {}
    fatalities = {}

    for i in parser["cantonal"]:
        print(parser["cantonal"][i])


if __name__ == "__main__":
    main()
