import pandas as pd
from datetime import date, timedelta
from configparser import ConfigParser


def get_date_range(dfs):
    min_dates = []
    for _, df in dfs.items():
        min_dates.append(date.fromisoformat(df.index.values.min()))
    min_date = min(min_dates)

    dates = []
    for i in range((date.today() - min_date).days + 1):
        dates.append((min_date + timedelta(days=i)).isoformat())

    return dates


def main():
    parser = ConfigParser()
    parser.read("sources.ini")

    cantons = list(map(str.upper, parser["cantonal"]))

    dfs = {}
    for canton in cantons:
        dfs[canton] = pd.read_csv(parser["cantonal"][canton.lower()], index_col=[0])

    # Append empty dates to all
    dates = get_date_range(dfs)

    df_cases = pd.DataFrame(float("nan"), index=dates, columns=cantons)
    for canton, df in dfs.items():
        for d in dates:
            if d in df.index:
                df_cases[canton][d] = df["ncumul_conf"][d]

    df_fatalities = pd.DataFrame(float("nan"), index=dates, columns=cantons)
    for canton, df in dfs.items():
        for d in dates:
            if d in df.index:
                df_fatalities[canton][d] = df["ncumul_deceased"][d]

    print(df_cases)
    print(df_fatalities.fillna(method="ffill"))


if __name__ == "__main__":
    main()
