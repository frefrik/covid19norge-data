import pandas as pd
from utils import (
    get_timestr,
    get_fhi_datafile,
    load_sources,
    write_sources,
    load_datafile,
    write_datafile,
    graphs
)


def update():
    now = get_timestr()

    # load current data
    df = load_datafile("dead")

    # get fhi datafile
    datafile = get_fhi_datafile("data_covid19_death_by_time")

    df_new = pd.read_csv(
        datafile, usecols=["date", "year", "week", "n"], parse_dates=["date"]
    )

    df_new = df_new.rename(columns={"n": "new"})
    df_new = df_new.sort_values(by=["date"], ascending=True)

    df_new["total"] = df_new["new"].cumsum()
    df_new["source"] = "fhi:git"

    df = load_datafile("dead", parse_dates=["date"])

    if not df_new.equals(df):
        print(now, "dead: New update")

        sourcefile = load_sources()
        sourcefile["dead.csv"]["last_updated"] = now
        sourcefile["dead.csv"]["pending_update"] = 1

        write_sources(sourcefile)
        write_datafile("dead", df_new)

        # Generate graph
        graphs.dead()
