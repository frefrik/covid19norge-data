import os
import json
import pandas as pd


def load_sources():
    with open("src/sources.json", "r") as f:
        jsonfile = json.load(f)

    return jsonfile


def write_sources(datadict):
    with open("src/sources.json", "w") as f:
        json.dump(datadict, f, indent=2)


def get_fhi_datafile(filestr):
    file_path = "https://raw.githubusercontent.com/folkehelseinstituttet/surveillance_data/master/covid19/"
    filename = f"{filestr}_latest.csv"

    datafile = os.path.join(file_path, filename)

    return datafile


def load_datafile(filestr, parse_dates=False):
    filepath = f"data/{filestr}.csv"
    df = pd.read_csv(filepath, na_values="", parse_dates=parse_dates)

    return df


def write_datafile(filestr, df):
    filepath = f"data/{filestr}.csv"
    df.to_csv(filepath, index=False, encoding="utf-8")
