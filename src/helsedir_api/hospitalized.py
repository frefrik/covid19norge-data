import os
import requests
import pandas as pd
from utils import (
    get_timestr,
    load_sources,
    write_sources,
    load_datafile,
    write_datafile,
    graphs,
)


def update():
    now = get_timestr()

    url = "https://api.helsedirektoratet.no/ProduktCovid19/Covid19Statistikk/"

    headers = {
        "Ocp-Apim-Subscription-Key": os.getenv("HELSEDIR_API_KEY"),
    }

    res = requests.get(url + "helseregion", headers=headers).json()
    df_new = pd.DataFrame()

    for r in res:
        df_new = df_new.append(r["registreringer"])

    df_new = df_new.rename(
        columns={
            "dato": "date",
            "antInnlagte": "admissions",
            "antCovidIntensiv": "icu",
            "antRespirator": "respiratory",
        }
    )

    df_new = df_new[["date", "admissions", "icu", "respiratory"]]
    df_new["date"] = pd.to_datetime(df_new["date"], format="%Y-%m-%d")

    df_new = df_new.groupby("date").sum()
    df_new = df_new.reset_index().sort_values(["date"], ascending=True)
    df_new["source"] = "helsedir:api"

    df = load_datafile("hospitalized", parse_dates=["date"])

    if not df_new.equals(df):
        print(now, "hospitalized: New update")

        sourcefile = load_sources()
        sourcefile["hospitalized.csv"]["last_updated"] = now
        sourcefile["hospitalized.csv"]["pending_update"] = 1

        write_sources(sourcefile)
        write_datafile("hospitalized", df_new)

        # Generate graph
        graphs.hospitalized()
