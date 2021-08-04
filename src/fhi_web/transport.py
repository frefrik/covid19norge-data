import os
import dateparser
import requests
import pandas as pd
from bs4 import BeautifulSoup
from utils import (
    get_timestr,
    load_sources,
    write_sources,
    load_datafile,
    write_datafile,
)


def fmt_date(datestr):
    fmt = dateparser.parse(
        str(datestr),
        date_formats=[
            "%d.%m.%y",
            "%d.%m.%y - %H:%M",
            "%d.%m.%y - %H.%M",
            "%d.%m.%Y - %H:%M",
        ],
        settings={"DATE_ORDER": "DMY"},
    )

    if fmt:
        return str(fmt)
    else:
        return None


def update():
    now = get_timestr()

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.2; rv:86.0) Gecko/20100101 Firefox/86.0",
        "X-Requested-With": "XMLHttpRequest",
    }

    columns = [
        "tr_type",
        "route",
        "company",
        "tr_from",
        "tr_to",
        "departure",
        "arrival",
        "source",
    ]
    df_new = pd.DataFrame(columns=columns)

    base_url = "https://www.fhi.no"
    url = f"{base_url}/sv/smittsomme-sykdommer/corona/koronavirus-og-covid-19-pa-offentlig-kommunikasjon/"

    html = requests.get(url).text
    soup = BeautifulSoup(html, "lxml")

    for i in soup.find_all("div", class_="fhi-dynamic-table__download"):
        a = i.find("a")
        href = a.get("href")
        filename = os.path.basename(href)

        tr_types = {
            "båt": "Skip",
            "bat": "Skip",
            "buss": "Buss",
            "fly": "Fly",
            "fly2": "Fly",
            "tog": "Tog",
        }

        res = requests.get(f"{base_url}{href}", allow_redirects=True, headers=headers)

        df_tmp = pd.read_excel(res.content)
        df_tmp = df_tmp.dropna()

        for i, row in df_tmp.iterrows():
            route = row[0]
            company = row[1]
            from_to = row[2].replace("\xa0", "")
            departure = fmt_date(row[3])
            arrival = fmt_date(row[4])

            from_to_split = from_to.split("-")
            _from = from_to_split[0].strip()
            try:
                _to = from_to_split[1].strip()
            except IndexError:
                _to = ""

            tr_type = ""
            try:
                tr_type = filename.split("-")[1].split(".")[0]
            except Exception:
                raise Exception

            values = {
                "tr_type": tr_types[tr_type],
                "route": route,
                "company": company,
                "tr_from": _from,
                "tr_to": _to,
                "departure": departure,
                "arrival": arrival,
                "source": "fhi:web",
            }

            df_new = df_new.append(pd.DataFrame(values, index=[0]))

    df_new.loc[
        df_new.departure == "2021-12-27 16:05:00", ["departure"]
    ] = "2020-12-27 16:05:00"

    df_new["departure"] = pd.to_datetime(df_new["departure"])
    df_new["arrival"] = pd.to_datetime(df_new["arrival"])

    for column in columns:
        df_new[column] = df_new[column].astype(str)

    df_new = df_new.sort_values(by=["departure", "arrival", "route"], ascending=False)

    columns = [
        "tr_type",
        "route",
        "company",
        "tr_from",
        "tr_to",
        "departure",
        "arrival",
        "source",
    ]

    df = load_datafile("transport")

    for column in columns:
        df_new[column] = df_new[column].astype(str).replace("nan", "")
        df[column] = df[column].astype(str).replace("nan", "")

    merged = pd.merge(df_new, df, how="outer", indicator=True)
    new_data = merged.loc[merged._merge == "left_only", columns]

    if not new_data.empty:
        print(now, "transport: New update")
        df = pd.concat([df, new_data])
        df = df.sort_values(by=["departure", "arrival", "route"], ascending=False)

        sourcefile = load_sources()
        sourcefile["transport.csv"]["last_updated"] = now
        sourcefile["transport.csv"]["pending_update"] = 1

        write_sources(sourcefile)
        write_datafile("transport", df)
