import os
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


def get_data():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.2; rv:86.0) Gecko/20100101 Firefox/86.0",
        "X-Requested-With": "XMLHttpRequest",
    }

    base_url = "https://www.fhi.no"
    url = f"{base_url}/sv/smittsomme-sykdommer/corona/meldte-tilfeller-av-ny-virusvariant/"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "lxml")

    for i in soup.find_all("div", class_="fhi-dynamic-table__download"):
        a = i.find("a")
        href = a.get("href")
        filename = os.path.basename(href)

        if "uke-week" in filename:
            res = requests.get(
                f"{base_url}{href}", allow_redirects=True, headers=headers
            )
            return res

    return None


def update():
    now = get_timestr()

    cols = {
        "År": "year",
        "Uke/week": "week",
        "Tilfeller/ cases": "new_confirmed",
    }
    data = get_data()

    if data:
        df_new = pd.read_excel(data.content, usecols=cols)
        df_new = df_new.rename(columns=cols)

        df_new = df_new[df_new["year"] != "Total"]
        df_new = df_new[["year", "week", "new_confirmed"]].astype(int)
        df_new = df_new.sort_values(by="week").reset_index(drop=True)

        df_new["total_confirmed"] = df_new["new_confirmed"].cumsum()

        df_new["source"] = "fhi:web"

        df = load_datafile("omicron")

        if not df_new.equals(df):
            print(now, "omicron: New update")

            sourcefile = load_sources()
            sourcefile["omicron.csv"]["last_updated"] = now
            sourcefile["omicron.csv"]["pending_update"] = 1

            write_sources(sourcefile)
            write_datafile("omicron", df_new)
