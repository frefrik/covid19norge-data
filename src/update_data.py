from fhi_git import vaccine, dead, tested_lab
from fhi_git import confirmed as confirmed_fhi
from fhi_web import tested, smittestopp, transport, omicron
from helsedir_api import hospitalized
from msis_api import confirmed as confirmed_msis
from utils import (
    confirmed_new_day,
    update_readme,
    load_sources,
    write_sources,
    pushover_message,
)


def reset_pending():
    for category in sources:
        sources[category]["pending_update"] = 0

    write_sources(sources)


if __name__ == "__main__":
    print("Checking for update: tested.csv")
    try:
        tested.update()
    except Exception as e:
        error_msg = f"tested.csv: {e.__class__.__name__}: {e}"
        print(error_msg)
        pushover_message("covid19norge-data: tested.csv", error_msg)

    print("Checking for update: tested_lab.csv")
    try:
        tested_lab.update()
    except Exception as e:
        error_msg = f"tested_lab.csv: {e.__class__.__name__}: {e}"
        print(error_msg)
        pushover_message("covid19norge-data: tested_lab.csv", error_msg)

    print("Checking for update: confirmed.csv")
    try:
        confirmed_new_day()
        confirmed_msis.update()
        confirmed_fhi.update()
    except Exception as e:
        error_msg = f"confirmed.csv: {e.__class__.__name__}: {e}"
        print(error_msg)
        pushover_message("covid19norge-data: confirmed.csv", error_msg)

    print("Checking for update: hospitalized.csv")
    try:
        hospitalized.update()
    except Exception as e:
        error_msg = f"hospitalized.csv: {e.__class__.__name__}: {e}"
        print(error_msg)
        pushover_message("covid19norge-data: hospitalized.csv", error_msg)

    print("Checking for update: dead.csv")
    try:
        dead.update()
    except Exception as e:
        error_msg = f"dead.csv: {e.__class__.__name__}: {e}"
        print(error_msg)
        pushover_message("covid19norge-data: dead.csv", error_msg)

    print("Checking for update: vaccine_doses.csv")
    try:
        vaccine.update()
    except Exception as e:
        error_msg = f"vaccine_doses.csv: {e.__class__.__name__}: {e}"
        print(error_msg)
        pushover_message("covid19norge-data: vaccine_doses.csv", error_msg)

    print("Checking for update: transport.csv")
    try:
        transport.update()
    except Exception as e:
        error_msg = f"transport.csv: {e.__class__.__name__}: {e}"
        print(error_msg)
        pushover_message("covid19norge-data: transport.csv", error_msg)

    print("Checking for update: smittestopp.csv")
    try:
        smittestopp.update()
    except Exception as e:
        error_msg = f"smittestopp.csv: {e.__class__.__name__}: {e}"
        print(error_msg)
        pushover_message("covid19norge-data: smittestopp.csv", error_msg)

    print("Checking for update: omicron.csv")
    try:
        omicron.update()
    except Exception as e:
        error_msg = f"omicron.csv: {e.__class__.__name__}: {e}"
        print(error_msg)
        pushover_message("covid19norge-data: omicron.csv", error_msg)

    sources = load_sources()
    pending_update = [sources[category]["pending_update"] for category in sources]

    if 1 in pending_update:
        print("Updating README.md")

        reset_pending()
        update_readme()
