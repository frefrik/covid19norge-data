from datetime import datetime
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

    # get from fhi api
    url = "https://www.fhi.no/api/chartdata/api/91672"
    res = requests.get(url).json()

    tests = res["figures"][4]
    fhi_tests = tests["number"]
    fhi_date = str(datetime.strptime(tests["updated"], "%d/%m/%Y").date())

    # get current data
    df = load_datafile("tested")

    # update new data
    if fhi_date not in df.date.values:
        print(now, "tested: New update")

        last_data = df["total"].max()
        tested_diff = fhi_tests - last_data

        df = df.append(
            {
                "date": fhi_date,
                "new": tested_diff,
                "total": fhi_tests,
                "source": "fhi:web",
            },
            ignore_index=True,
        )

        sourcefile = load_sources()
        sourcefile["tested.csv"]["last_updated"] = now
        sourcefile["tested.csv"]["pending_update"] = 1

        write_sources(sourcefile)
        write_datafile("tested", df)
