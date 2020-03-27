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
        dfs[canton] = (
            pd.read_csv(parser["cantonal"][canton.lower()]).groupby(["date"]).max()
        )

    # Append empty dates to all
    dates = get_date_range(dfs)

    df_cases = pd.DataFrame(float("nan"), index=dates, columns=cantons)
    df_fatalities = pd.DataFrame(float("nan"), index=dates, columns=cantons)
    df_hospitalized = pd.DataFrame(float("nan"), index=dates, columns=cantons)

    for canton, df in dfs.items():
        for d in dates:
            if d in df.index:
                df_cases[canton][d] = df["ncumul_conf"][d]
                df_fatalities[canton][d] = df["ncumul_deceased"][d]
                df_hospitalized[canton][d] = df["ncumul_hosp"][d]

    # Fill to calculate the correct totals for CH
    df_cases_total = df_cases.fillna(method="ffill")
    df_fatalities_total = df_fatalities.fillna(method="ffill")
    df_hospitalized_total = df_hospitalized.fillna(method="ffill")

    df_cases["CH"] = df_cases_total.sum(axis=1)
    df_fatalities["CH"] = df_fatalities_total.sum(axis=1)
    df_hospitalized["CH"] = df_hospitalized_total.sum(axis=1)

    df_cases.to_csv("covid19_cases_switzerland_openzh.csv", index_label="Date")
    df_fatalities.to_csv(
        "covid19_fatalities_switzerland_openzh.csv", index_label="Date"
    )
    df_hospitalized.to_csv(
        "covid19_hospitalized_switzerland_openzh.csv", index_label="Date"
    )


if __name__ == "__main__":
    main()
