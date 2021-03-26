from fhi_git import vaccine, dead, tested_lab
from fhi_git import confirmed as confirmed_fhi
from fhi_web import tested, smittestopp, transport
from helsedir_api import hospitalized
from msis_api import confirmed as confirmed_msis
from utils import confirmed_new_day, update_readme, load_sources, write_sources


def reset_pending():
    for category in sources:
        sources[category]["pending_update"] = 0

    write_sources(sources)


if __name__ == "__main__":
    print("Checking for update: tested.csv")
    tested.update()

    print("Checking for update: tested_lab.csv")
    tested_lab.update()

    print("Checking for update: confirmed.csv")
    confirmed_new_day()
    confirmed_msis.update()
    confirmed_fhi.update()

    print("Checking for update: hospitalized.csv")
    hospitalized.update()

    print("Checking for update: dead.csv")
    dead.update()

    print("Checking for update: vaccine_doses.csv")
    vaccine.update()

    print("Checking for update: transport.csv")
    transport.update()

    print("Checking for update: smittestopp.csv")
    smittestopp.update()

    sources = load_sources()
    pending_update = [sources[category]["pending_update"] for category in sources]

    if 1 in pending_update:
        print("Updating README.md")

        reset_pending()
        update_readme()
