from typing import Tuple

import requests


def get_all_districts():
    response = requests.get("https://rki-covid-api.now.sh/api/districts").json()
    return response["lastUpdate"], {d["name"]: d for d in response["districts"]}


def get_district(district: str) -> Tuple[str, dict]:
    last_update, districts = get_all_districts()
    return last_update, districts[district]
