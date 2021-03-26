import re
import json
from mdutils.mdutils import MdUtils

mdFile = MdUtils(file_name="README")
index_re = re.compile(r"<!\-\- table starts \-\->.*<!\-\- table ends \-\->", re.DOTALL)


def table_datasets():
    with open("src/sources.json") as json_file:
        datasets = json.load(json_file)

    dataset_table = ["Data", "Source", "Last updated", "Download", "Preview"]

    datafiles = [
        "confirmed.csv",
        "dead.csv",
        "hospitalized.csv",
        "tested.csv",
        "tested_lab.csv",
        "transport.csv",
        "vaccine_doses.csv",
        "smittestopp.csv",
    ]

    columns = len(dataset_table)
    link = mdFile.new_inline_link

    for datafile in datafiles:
        dataset_table.extend(
            [
                link(
                    link=datasets[datafile]["dataset_detail"],
                    text=datasets[datafile]["name"],
                ),
                datasets[datafile]["data_source"],
                datasets[datafile]["last_updated"],
                link(link=datasets[datafile]["link_csv"], text="csv", align="center"),
                link(
                    link=datasets[datafile]["link_preview"],
                    text="preview",
                    align="center",
                ),
            ]
        )

    mdFile.new_table(
        columns=columns, rows=len(datasets) + 1, text=dataset_table, text_align="left"
    )


def update_readme():
    table_datasets()

    table = mdFile.file_data_text

    readme = "README.md"
    readme_current = open(readme).read()

    index = ["<!-- table starts -->"]
    index.append(table)
    index.append("<!-- table ends -->")
    index_txt = "".join(index).strip()

    rewritten = index_re.sub(index_txt, readme_current)

    readme_new = open(readme, "w")
    readme_new.write(rewritten)
