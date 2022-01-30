from datetime import datetime
from dateutil import parser
from typing import Tuple

import requests


def get_all_districts():
    response = requests.get("https://api.corona-zahlen.org/districts").json()
    return parser.parse(response["meta"]["lastUpdate"]), {
        d["name"]: d | {"count": d["cases"]} for d in response["data"].values()
    }


def get_district(district: str) -> Tuple[datetime, dict]:
    last_update, districts = get_all_districts()
    return last_update, districts[district]
