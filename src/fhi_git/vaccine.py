import pandas as pd
from utils import (
    get_timestr,
    get_fhi_datafile,
    load_sources,
    write_sources,
    load_datafile,
    write_datafile,
    graphs,
)


def update():
    now = get_timestr()

    # load current data
    df = load_datafile("vaccine_doses")

    # get fhi datafile
    datafile = get_fhi_datafile("data_covid19_sysvak_by_time_location")

    df_new = pd.read_csv(
        datafile,
        usecols=[
            "date",
            "granularity_geo",
            "location_name",
            "n_dose_1",
            "n_dose_2",
            "cum_n_dose_1",
            "cum_n_dose_2",
            "cum_pr100_dose_1",
            "cum_pr100_dose_2",
        ],
    )

    mapping = {
        "n_dose_1": "new_dose_1",
        "n_dose_2": "new_dose_2",
        "cum_n_dose_1": "total_dose_1",
        "cum_n_dose_2": "total_dose_2",
        "cum_pr100_dose_1": "total_pr100_dose_1",
        "cum_pr100_dose_2": "total_pr100_dose_2",
    }

    columns = [
        "granularity_geo",
        "location_name",
        "date",
        "new_dose_1",
        "new_dose_2",
        "total_dose_1",
        "total_dose_2",
        "total_pr100_dose_1",
        "total_pr100_dose_2",
        "new_doses",
        "total_doses",
        "source",
    ]

    df_new = df_new.rename(columns=mapping)

    df_new["new_doses"] = df_new["new_dose_1"] + df_new["new_dose_2"]
    df_new["total_doses"] = df_new["total_dose_1"] + df_new["total_dose_2"]
    df_new["source"] = "fhi:git"

    df_new = df_new[columns]

    for column in columns:
        df_new[column] = df_new[column].astype(str).replace("nan", "")
        df[column] = df[column].astype(str)

    df_new = df_new.sort_values(
        by=["granularity_geo", "location_name", "date"]
    ).reset_index(drop=True)

    df = df.sort_values(by=["granularity_geo", "location_name", "date"]).reset_index(
        drop=True
    )

    if not df_new.index.equals(df.index):
        print(now, "vaccine_doses: New update")

        sourcefile = load_sources()
        sourcefile["vaccine_doses.csv"]["last_updated"] = now
        sourcefile["vaccine_doses.csv"]["pending_update"] = 1

        write_sources(sourcefile)
        write_datafile("vaccine_doses", df_new)

        # Generate graph
        graphs.vaccine_doses()
