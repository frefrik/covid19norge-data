from datetime import datetime, date
from pytz import timezone
from .readme import update_readme
from .browser import get_browser
from .files import (
    load_sources,
    write_sources,
    get_fhi_datafile,
    load_datafile,
    write_datafile,
)


def get_timestr():
    tz = timezone("Europe/Oslo")
    timestr = datetime.now().replace(microsecond=0).astimezone(tz)

    return str(timestr)


def confirmed_new_day():
    now = get_timestr()
    today = date.today()

    df = load_datafile("confirmed")
    df_today = df[df["date"] == str(today)]
    last_total = df["total"].max()

    if df_today.empty:
        print(
            now,
            "confirmed: date missing, inserting new row",
        )
        df = df.append(
            {"date": today, "new": 0, "total": last_total, "source": "local:cron"},
            ignore_index=True,
        )

        sourcefile = load_sources()
        sourcefile["confirmed.csv"]["last_updated"] = now
        sourcefile["confirmed.csv"]["pending_update"] = 1

        write_sources(sourcefile)
        write_datafile("confirmed", df)
