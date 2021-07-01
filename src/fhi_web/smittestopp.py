import sys
import time
import dateparser
import pandas as pd
from utils import (
    get_timestr,
    load_sources,
    write_sources,
    load_datafile,
    write_datafile,
    get_browser,
    graphs,
)

def fmt_num(num):
    if isinstance(num, str):
        num = int(num.replace(".", ""))

    return num


def update():
    now = get_timestr()
    url = "https://www.fhi.no/om/smittestopp/nokkeltall-fra-smittestopp/"

    browser = get_browser()

    try:
        browser.get(url)
        time.sleep(1)
        new_downloads = browser.execute_script(
            "return Highcharts.charts[0].series[0].options.data"
        )
        total_downloads = browser.execute_script(
            "return Highcharts.charts[0].series[1].options.data"
        )
        new_reported = browser.execute_script(
            "return Highcharts.charts[1].series[0].options.data"
        )
        total_reported = browser.execute_script(
            "return Highcharts.charts[1].series[1].options.data"
        )

        browser.close()
        browser.quit()

    except Exception:
        error = sys.exc_info()[1]
        print("- ERROR:", str(error))

    new_lst = []

    for n in new_downloads:
        date_parsed = dateparser.parse(str(n[0]), settings={'DATE_ORDER': 'DMY'})
        datestr = date_parsed.strftime("%Y-%m-%d")
        d = {"date": datestr, "new_downloads": fmt_num(n[1])}

        new_lst.append(d)

    df_new = pd.DataFrame(new_lst)

    for n in total_downloads:
        date_parsed = dateparser.parse(str(n[0]), settings={'DATE_ORDER': 'DMY'})
        datestr = date_parsed.strftime("%Y-%m-%d")
        df_new.loc[df_new["date"] == datestr, "total_downloads"] = fmt_num(n[1])

    for n in new_reported:
        date_parsed = dateparser.parse(str(n[0]), settings={'DATE_ORDER': 'DMY'})
        datestr = date_parsed.strftime("%Y-%m-%d")
        df_new.loc[df_new["date"] == datestr, "new_reported"] = fmt_num(n[1])

    for n in total_reported:
        date_parsed = dateparser.parse(str(n[0]), settings={'DATE_ORDER': 'DMY'})
        datestr = date_parsed.strftime("%Y-%m-%d")
        df_new.loc[df_new["date"] == datestr, "total_reported"] = fmt_num(n[1])

    df_new = df_new.fillna(0)
    intcolumns = [
        "new_downloads",
        "total_downloads",
        "new_reported",
        "total_reported",
    ]

    df_new[intcolumns] = df_new[intcolumns].astype(int)

    df_new["source"] = "fhi:web"
    df_new["date"] = pd.to_datetime(df_new["date"])

    columns = [
        "date",
        "new_downloads",
        "total_downloads",
        "new_reported",
        "total_reported",
    ]

    # Compare dfs
    df = load_datafile("smittestopp", parse_dates=["date"])
    df_new = df_new.sort_values(by=["date"])

    merged = pd.merge(df_new, df, how="outer", indicator=True)
    new_data = merged.loc[merged._merge == "left_only", columns]

    if not new_data.empty:
        print(now, "smittestopp: New update")

        sourcefile = load_sources()
        sourcefile["smittestopp.csv"]["last_updated"] = now
        sourcefile["smittestopp.csv"]["pending_update"] = 1

        write_sources(sourcefile)
        write_datafile("smittestopp", df_new)

        # Generate graph
        graphs.smittestopp()
