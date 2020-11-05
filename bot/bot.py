import time
from os import environ

import requests
from redis import Redis

from covid_api import get_district

TOKEN = environ["TOKEN"]
REDIS_HOST = environ["REDIS_HOST"]
CHANNEL = environ["CHANNEL"]
DISTRICT = environ["DISTRICT"]

redis = Redis(host=REDIS_HOST)


def send_message(text: str):
    requests.get(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        params={"chat_id": CHANNEL, "text": text, "parse_mode": "Markdown"},
    )


def update(ts: str) -> bool:
    if redis.get("last_update") == ts.encode():
        return False
    redis.set("last_update", ts)
    return True


def update_value(district: dict, key: str, precision: int = 0):
    last = redis.get("last_val_" + key)
    if last:
        last = round(float(last.decode()), precision or None)

    value = district[key]
    redis.set("last_val_" + key, value)
    value = round(value, precision or None)

    if last is not None and last != value:
        diff = round(value - last, precision or None)
        return f"{value} ({'+' * (value > last)}{diff})"

    return str(value)


def callback():
    last_update, district = get_district(DISTRICT)
    if not update(last_update):
        return

    text = [
        f"*{district['name']}*\n",
        f"Fälle: {update_value(district, 'count')}",
        f"Fälle/100k EW: {update_value(district, 'casesPer100k', 2)}",
        f"Fälle letzte 7d/100k EW: {update_value(district, 'weekIncidence', 2)}",
        f"Todesfälle: {update_value(district, 'deaths')}",
        f"\nStand: {last_update}",
    ]
    send_message(text="\n".join(text))


while True:
    callback()
    time.sleep(60)
