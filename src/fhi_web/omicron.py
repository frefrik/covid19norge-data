import requests
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
from utils import (
    get_timestr,
    load_sources,
    write_sources,
    load_datafile,
    write_datafile,
)


def update():
    now = get_timestr()
    year = datetime.now().year

    cols = {
        "Uke": "week",
        "Sannsynlige Omikron": "new_probable",
        "Bekreftede Omikron": "new_confirmed",
    }

    url = "https://www.fhi.no/sv/smittsomme-sykdommer/corona/meldte-tilfeller-av-ny-virusvariant/"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "lxml")

    table = soup.find(
        text="Antall nye tilfeller siste døgn og totalt antall tilfeller"
    ).find_parent("table")

    df_new = pd.read_html(str(table))[0]
    df_new = df_new[df_new["Uke"] != "Total"]

    df_new = df_new.rename(columns=cols)
    df_new = df_new[["week", "new_probable", "new_confirmed"]].astype(int)
    df_new = df_new.sort_values(by="week").reset_index(drop=True)

    df_new["total_probable"] = df_new["new_probable"].cumsum()
    df_new["total_confirmed"] = df_new["new_confirmed"].cumsum()

    df_new.insert(
        loc=0, column="year", value=[2021 if x >= 47 else year for x in df_new["week"]]
    )
    df_new["source"] = "fhi:web"

    df = load_datafile("omicron")

    if not df_new.equals(df):
        print(now, "omicron: New update")

        sourcefile = load_sources()
        sourcefile["omicron.csv"]["last_updated"] = now
        sourcefile["omicron.csv"]["pending_update"] = 1

        write_sources(sourcefile)
        write_datafile("omicron", df_new)
