import sys
from datetime import datetime, date, timedelta
import requests
from utils import (
    get_timestr,
    load_sources,
    write_sources,
    load_datafile,
    write_datafile,
)


def update():
    now = get_timestr()
    today = date.today()
    yesterday = today - timedelta(days=1)

    url = "https://statistikk.fhi.no/api/msis/antallKoronaTotalt"

    df = load_datafile("confirmed")
    last_total = df["total"].max()

    try:
        confirmed_total = requests.get(url).json()
    except Exception:
        confirmed_total = 0
        error = sys.exc_info()[1]
        print(now, "- ERROR:", str(error))

    if confirmed_total > last_total:
        print(now, "msis_api.confirmed: New update")

        confirmed_diff = confirmed_total - last_total

        if datetime.now().hour in range(0, 2):
            n_yesterday = df.new.loc[df["date"] == str(yesterday)].values[0]

            diff_yesterday = n_yesterday + confirmed_diff

            df.loc[df["date"] == str(yesterday), "new"] = diff_yesterday
            df.loc[df["date"] == str(yesterday), "total"] = confirmed_total
            df.loc[df["date"] == str(today), "total"] = confirmed_total
            df.loc[df["date"] == str(yesterday), "source"] = "msis:api"
            df.loc[df["date"] == str(today), "source"] = "msis:api"

        else:
            n_today = df.new.loc[df["date"] == str(today)].values[0]
            diff_today = n_today + confirmed_diff

            df.loc[df["date"] == str(today), "new"] = diff_today
            df.loc[df["date"] == str(today), "total"] = confirmed_total
            df.loc[df["date"] == str(today), "source"] = "msis:api"

        sourcefile = load_sources()
        sourcefile["confirmed.csv"]["last_updated"] = now
        sourcefile["confirmed.csv"]["pending_update"] = 1

        write_sources(sourcefile)
        write_datafile("confirmed", df)
