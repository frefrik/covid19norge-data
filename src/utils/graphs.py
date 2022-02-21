import os
from datetime import date
import altair as alt
import pandas as pd


def tested_lab():
    data = "data/tested_lab.csv"
    filename = "graphs/tested_lab.png"
    if os.path.exists(filename):
        os.remove(filename)

    df = pd.read_csv(data)

    mapping = {
        "new_neg": "New (Negative)",
        "new_pos": "New (Positive)",
        "new_total": "New",
        "pr100_pos": "Share Positive",
        "total": "Cumulative",
    }

    df = df.rename(columns=mapping)
    df["date"] = pd.to_datetime(df["date"])
    df["Share Negative"] = 100 - df["Share Positive"]
    df = df.melt(
        id_vars=["date", "Share Positive"], var_name="category", value_name="value"
    )

    base = alt.Chart(
        df,
        title="Number of tested persons per specimen collection date and number of positive results (Source: FHI)",
    ).encode(alt.X("yearmonthdate(date):O", axis=alt.Axis(title=None, labelAngle=-40)))

    andel = base.mark_line(color="red", opacity=0.8).encode(
        y=alt.Y("Share Positive:Q", title="% Positive", axis=alt.Axis(grid=True))
    )

    bar = (
        base.transform_filter(
            (alt.datum.category == "New (Negative)")
            | (alt.datum.category == "New (Positive)")
        )
        .mark_bar()
        .encode(
            y=alt.Y("value:Q", title="Number of persons"),
            color=alt.Color(
                "category:N",
                scale=alt.Scale(
                    domain=["New (Positive)", "New (Negative)", "% Positive"],
                    range=["#FF9622", "#6DA9FF", "red"],
                ),
                legend=alt.Legend(title=None),
            ),
        )
    )

    chart = (
        alt.layer(bar, andel)
        .resolve_scale(y="independent")
        .properties(width=1200, height=600)
        .configure_legend(
            strokeColor="gray",
            fillColor="#FFFFFF",
            labelFontSize=12,
            symbolStrokeWidth=2,
            symbolSize=160,
            padding=6,
            cornerRadius=5,
            direction="horizontal",
            orient="none",
            legendX=480,
            legendY=655,
        )
    )

    chart.save(filename)


def confirmed():
    data = "data/confirmed.csv"
    filename = "graphs/confirmed.png"
    if os.path.exists(filename):
        os.remove(filename)

    df = pd.read_csv(data)
    df["date"] = pd.to_datetime(df["date"])
    df = df.loc[df["source"] == "fhi:git"]
    df["new_sma7"] = df.new.rolling(window=7).mean().shift()

    df = df.melt(
        id_vars=["date"],
        value_vars=["new", "new_sma7", "total"],
        var_name="category",
        value_name="value",
    ).dropna()

    rename = {"new": "New cases", "new_sma7": "Avg 7 d.", "total": "Cumulative"}

    df["category"] = df["category"].replace(rename)

    base = alt.Chart(
        df,
        title="Number of reported COVID-19 cases by specimen collection date (Source: FHI)",
    ).encode(alt.X("yearmonthdate(date):O", axis=alt.Axis(title=None, labelAngle=-40)))

    bar = (
        base.transform_filter(alt.datum.category == "New cases")
        .mark_bar(color="#FFD1D1")
        .encode(y=alt.Y("value:Q", axis=alt.Axis(title="New per day", grid=True)))
    )

    line = (
        base.transform_filter(alt.datum.category == "Cumulative")
        .mark_line(color="#2E507B", strokeWidth=3)
        .encode(
            y=alt.Y("value:Q", axis=alt.Axis(title="Cumulative")),
            color=alt.Color(
                "category:N",
                scale=alt.Scale(
                    domain=["New cases", "Avg 7 d.", "Cumulative"],
                    range=["#FFD1D1", "red", "#2E507B"],
                ),
                legend=alt.Legend(title=None),
            ),
        )
    )

    ma7 = (
        base.transform_filter(alt.datum.category == "Avg 7 d.")
        .mark_line(opacity=0.8)
        .encode(y=alt.Y("value:Q"), color=alt.Color("category:N"))
    )

    chart = (
        alt.layer(bar + ma7, line)
        .resolve_scale(y="independent")
        .properties(width=1200, height=600)
        .configure_legend(
            strokeColor="gray",
            fillColor="#FFFFFF",
            labelFontSize=12,
            symbolStrokeWidth=2,
            symbolSize=160,
            padding=6,
            cornerRadius=5,
            direction="horizontal",
            orient="none",
            legendX=480,
            legendY=655,
        )
    )

    chart.save(filename)


def dead():
    data = "data/dead.csv"
    filename = "graphs/dead.png"
    if os.path.exists(filename):
        os.remove(filename)

    df = pd.read_csv(data)

    today = date.today()
    idx = pd.date_range("2020-03-07", df["date"].max())
    df.index = pd.DatetimeIndex(df["date"])
    df = df.reindex(idx)
    df["date"] = df.index
    df = df.reset_index(drop=True)
    df = df[df.date <= str(today)]

    df["new"] = df["new"].fillna(0).astype(int)
    df["total"] = df["total"].fillna(method="bfill").astype(int)
    df["new_sma7"] = df.new.rolling(window=7).mean()

    df = df.melt(
        id_vars=["date"],
        value_vars=["new", "new_sma7", "total"],
        var_name="category",
        value_name="value",
    ).dropna()

    rename = {"new": "New", "new_sma7": "Avg 7 d.", "total": "Cumulative"}
    df["category"] = df["category"].replace(rename)

    base = alt.Chart(df, title="COVID-19 related deaths (Source: FHI)").encode(
        alt.X("yearmonthdate(date):O", axis=alt.Axis(title=None, labelAngle=-40))
    )

    bar = (
        base.transform_filter(alt.datum.category == "New")
        .mark_bar(color="#FFD1D1")
        .encode(y=alt.Y("value:Q", axis=alt.Axis(title="New per day", grid=True)))
    )

    line = (
        base.transform_filter(alt.datum.category == "Cumulative")
        .mark_line(color="#2E507B", strokeWidth=3)
        .encode(
            y=alt.Y("value:Q", axis=alt.Axis(title="Cumulative")),
            color=alt.Color(
                "category:N",
                scale=alt.Scale(
                    domain=["New", "Avg 7 d.", "Cumulative"],
                    range=["#FFD1D1", "red", "#2E507B"],
                ),
                legend=alt.Legend(title=None),
            ),
        )
    )

    ma7 = (
        base.transform_filter(alt.datum.category == "Avg 7 d.")
        .mark_line(opacity=0.8)
        .encode(y=alt.Y("value:Q"), color=alt.Color("category:N"))
    )

    chart = (
        alt.layer(bar + ma7, line)
        .resolve_scale(y="independent")
        .properties(width=1200, height=600)
        .configure_legend(
            strokeColor="gray",
            fillColor="#FFFFFF",
            labelFontSize=12,
            symbolStrokeWidth=2,
            symbolSize=160,
            padding=6,
            cornerRadius=5,
            direction="horizontal",
            orient="none",
            legendX=480,
            legendY=655,
        )
    )

    chart.save(filename)


def hospitalized():
    data = "data/hospitalized.csv"
    filename = "graphs/hospitalized.png"
    if os.path.exists(filename):
        os.remove(filename)

    df = pd.read_csv(data)

    today = date.today()
    idx = pd.date_range("2020-03-08", today)
    df.index = pd.DatetimeIndex(df["date"])
    df = df.reindex(idx)
    df["date"] = df.index
    df = df.reset_index(drop=True)

    df["admissions"] = df["admissions"].fillna(method="ffill").astype(int)
    df["icu"] = df["icu"].fillna(method="ffill").astype(int)
    df["respiratory"] = df["respiratory"].fillna(method="ffill").astype(int)

    df_melt = pd.melt(
        df,
        id_vars=["date"],
        value_vars=["admissions", "icu", "respiratory"],
        value_name="value",
    ).replace(
        {
            "admissions": "Hospitalized",
            "icu": "Intensive Care",
            "respiratory": "Respiratory",
        }
    )

    chart = (
        alt.Chart(
            df_melt,
            title="Number of patients admitted to hospital with COVID-19 (Source: Helsedirektoratet)",
        )
        .mark_area(line={}, opacity=0.3)
        .encode(
            x=alt.X("yearmonthdate(date):O", axis=alt.Axis(title=None, labelAngle=-40)),
            y=alt.Y(
                "value:Q",
                stack=None,
                title="Number of patients",
            ),
            color=alt.Color(
                "variable:N",
                scale=alt.Scale(
                    domain=["Hospitalized", "Intensive Care", "Respiratory"],
                    range=["#5A9DFF", "#FF8B1B", "#FF642B"],
                ),
                legend=alt.Legend(title=None),
            ),
        )
        .properties(width=1200, height=600)
        .configure_legend(
            strokeColor="gray",
            fillColor="#FFFFFF",
            labelFontSize=12,
            symbolStrokeWidth=2,
            symbolSize=160,
            padding=6,
            cornerRadius=5,
            direction="horizontal",
            orient="none",
            legendX=480,
            legendY=655,
        )
    )

    chart.save(filename)


def smittestopp():
    data = "data/smittestopp.csv"
    filename = "graphs/smittestopp.png"
    if os.path.exists(filename):
        os.remove(filename)

    df = pd.read_csv(data)
    df["date"] = pd.to_datetime(df["date"])

    df = df.melt(
        id_vars=["date"],
        value_vars=["new_reported", "total_downloads"],
        var_name="category",
        value_name="value",
    ).dropna()

    rename = {
        "new_reported": "Number of reported infections",
        "total_downloads": "Number of downloads",
    }

    df["category"] = df["category"].replace(rename)

    base = alt.Chart(
        df,
        title="Number of downloads of Smittestopp og number of reported infections through the app (Source: FHI)",
    ).encode(alt.X("yearmonthdate(date):O", axis=alt.Axis(title=None, labelAngle=-40)))

    downloads = (
        base.transform_filter(alt.datum.category == "Number of downloads")
        .mark_area(line={}, color="#5BC1FF", opacity=0.2)
        .encode(
            y=alt.Y(
                "value:Q",
                axis=alt.Axis(title="Number of downloads", grid=True),
            )
        )
    )

    reported = (
        base.transform_filter(alt.datum.category == "Number of reported infections")
        .mark_bar(color="#FFA57E")
        .encode(
            y=alt.Y("value:Q", axis=alt.Axis(title="Number of reported infections")),
            color=alt.Color(
                "category:N",
                scale=alt.Scale(
                    domain=[
                        "Number of downloads",
                        "Number of reported infections",
                    ],
                    range=["#5BC1FF", "#FFA57E"],
                ),
                legend=alt.Legend(title=None),
            ),
        )
    )

    chart = (
        alt.layer(reported, downloads)
        .resolve_scale(y="independent")
        .properties(width=1200, height=600)
        .configure_legend(
            strokeColor="gray",
            fillColor="#FFFFFF",
            labelFontSize=12,
            symbolStrokeWidth=2,
            symbolSize=160,
            labelLimit=200,
            padding=6,
            cornerRadius=5,
            direction="horizontal",
            orient="none",
            legendX=390,
            legendY=660,
        )
    )

    chart.save(filename)


def vaccine_doses():
    data = "data/vaccine_doses.csv"
    filename = "graphs/vaccine_doses.png"
    if os.path.exists(filename):
        os.remove(filename)

    df = pd.read_csv(data)
    df["date"] = pd.to_datetime(df["date"])
    df = df[df["granularity_geo"] == "nation"]
    df["new_sma7"] = df.new_doses.rolling(window=7).mean().shift()

    df = df.melt(
        id_vars=["date"],
        value_vars=["total_dose_1", "total_dose_2", "total_dose_3"],
        var_name="category",
        value_name="value",
    ).dropna()

    rename = {
        "total_dose_1": "Dose 1",
        "total_dose_2": "Dose 2",
        "total_dose_3": "Dose 3",
    }

    df["category"] = df["category"].replace(rename)

    chart = (
        alt.Chart(
            df,
            title="Number of people who received their first, second and third dose of a COVID-19 vaccine in Norway (Source: FHI)",
        )
        .mark_area(line={}, opacity=0.3)
        .encode(
            x=alt.X("yearmonthdate(date):O", axis=alt.Axis(title=None, labelAngle=-40)),
            y=alt.Y(
                "value:Q",
                stack=None,
                title="Number of people",
            ),
            color=alt.Color(
                "category:N",
                scale=alt.Scale(
                    domain=[
                        "Dose 1",
                        "Dose 2",
                        "Dose 3",
                    ],
                    range=["#5dade2", " #2ecc71", "#006600"],
                ),
                legend=alt.Legend(title=None),
            ),
        )
        .properties(width=1200, height=600)
        .configure_legend(
            strokeColor="gray",
            fillColor="#FFFFFF",
            labelFontSize=12,
            symbolStrokeWidth=2,
            symbolSize=160,
            padding=6,
            cornerRadius=5,
            direction="horizontal",
            orient="none",
            legendX=380,
            legendY=660,
        )
    )

    chart.save(filename)
