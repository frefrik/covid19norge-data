import pandas as pd
from utils import (
    get_timestr,
    load_sources,
    write_sources,
    load_datafile,
    write_datafile,
    get_fhi_datafile,
)


def update():
    now = get_timestr()

    datafile = get_fhi_datafile("data_covid19_msis_by_time_location")
    df_new = pd.read_csv(
        datafile, usecols=["date", "n", "location_name"], parse_dates=["date"]
    )

    df_new = df_new.loc[(df_new["location_name"] == "Norge")]
    df_new = df_new.filter(items=["date", "n"])
    df_new = df_new[df_new.date >= "2020-02-21"]
    df_new = df_new.rename(columns={"n": "new"})

    df_new["total"] = df_new["new"].cumsum()
    df_new["source"] = "fhi:git"
    df_new = df_new.reset_index(drop=True)

    df = load_datafile("confirmed", parse_dates=["date"])
    df = df[df.date >= "2020-02-21"]
    df_filter = df.loc[df["source"] == "fhi:git"]
    df_filter = df_filter.reset_index(drop=True)

    if not df_new.equals(df_filter):
        print(now, "fhi_git.confirmed: New update")

        df_new = df_new.merge(df, how="outer")
        df_new = df_new.drop_duplicates(subset=["date"], keep="first")

        second_last = df_new.iloc[-2:]
        second_last_total = second_last.total.values[0]
        last_total = second_last.total.values[1]
        last_new = second_last.new.values[1]

        if second_last_total > last_total:
            newToday = last_new + (second_last_total - last_total)

            df_new.iloc[-1:]["total"] = second_last_total
            df_new.iloc[-1:]["new"] = newToday

        sourcefile = load_sources()
        sourcefile["confirmed.csv"]["last_updated"] = now
        sourcefile["confirmed.csv"]["pending_update"] = 1

        write_sources(sourcefile)
        write_datafile("confirmed", df_new)
