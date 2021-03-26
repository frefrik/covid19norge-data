import pandas as pd
from utils import (
    get_timestr,
    get_fhi_datafile,
    load_sources,
    write_sources,
    load_datafile,
    write_datafile,
)


def update():
    now = get_timestr()

    # get fhi datafile
    datafile = get_fhi_datafile("data_covid19_lab_by_time")
    df_new = pd.read_csv(
        datafile, usecols=["date", "n_neg", "n_pos", "pr100_pos"], parse_dates=["date"]
    )

    mapping = {"n_neg": "new_neg", "n_pos": "new_pos"}

    df_new = df_new.rename(columns=mapping)

    df_new["new_total"] = df_new["new_neg"] + df_new["new_pos"]
    df_new["total_neg"] = df_new["new_neg"].cumsum()
    df_new["total_pos"] = df_new["new_pos"].cumsum()
    df_new["total"] = df_new["new_total"].cumsum()
    df_new["source"] = "fhi:git"

    df_new = df_new.sort_values(by=["date"], ascending=True)
    df = load_datafile("tested_lab", parse_dates=["date"])

    if not df_new.equals(df):
        print(now, "tested_lab: New update")

        sourcefile = load_sources()
        sourcefile["tested_lab.csv"]["last_updated"] = now
        sourcefile["tested_lab.csv"]["pending_update"] = 1

        write_sources(sourcefile)
        write_datafile("tested_lab", df_new)
