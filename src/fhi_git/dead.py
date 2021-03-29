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
    datafile = get_fhi_datafile("data_covid19_demographics")
    df_new = pd.read_csv(datafile)

    date_of_publishing = df_new.date_of_publishing.max()

    if date_of_publishing not in df.date.values:
        print(now, "dead: New update")

        last_data = df["total"].max()
        fhi_dead = df_new["n"].sum()
        dead_diff = fhi_dead - last_data

        df = df.append(
            {
                "date": date_of_publishing,
                "new": dead_diff,
                "total": fhi_dead,
                "source": "fhi:git",
            },
            ignore_index=True,
        )

        sourcefile = load_sources()
        sourcefile["dead.csv"]["last_updated"] = now
        sourcefile["dead.csv"]["pending_update"] = 1

        write_sources(sourcefile)
        write_datafile("dead", df)

        # Generate graph
        graphs.dead()
