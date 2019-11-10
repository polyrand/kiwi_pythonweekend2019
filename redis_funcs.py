from redis import StrictRedis
from slugify import slugify
import json

from typing import Union


def sf(x: str) -> str:

    return slugify(x, separator="_")


redis_config = {
    "host": "34.77.218.145",
    "port": 80,
}

initials = "anderegg"
carrier = sf("Flixbus")

redis = StrictRedis(socket_connect_timeout=3, **redis_config)
# redis.set("x", 5)
# redis.get("x")
# "5"


def get_location_from_redis(city: str) -> Union[None, int]:
    key = f"bcn_{initials}:location:{city}_{carrier}"
    value = redis.get(key)
    if value:
        result = value.decode("utf-8")

        # print(result)
        # print(type(result))
        # print(int(result))
        return int(result)
    else:
        return None


def add_location_to_redis(city: str, payload: str) -> None:
    key = f"bcn_{initials}:location:{city}_{carrier}"
    # redis.expire("cached_data", 60 * 60)
    redis.setex(key, 3600, json.dumps(payload))
    return


def get_journey_from_redis(
    source: str, destination: str, dep_date: str
) -> Union[str, None]:
    key = f"bcn_{initials}:journey:{source}_{destination}_{dep_date}_{carrier}"
    value = redis.get(key)
    if value:
        return json.loads(value)
    else:
        return None


def add_journey_to_redis(
    source: str, destination: str, dep_date: str, payload: str
) -> None:
    key = f"bcn_{initials}:journey:{source}_{destination}_{dep_date}_{carrier}"
    redis.setex(key, 3600, json.dumps(payload))
    return


# payload = "[{'departure_datetime': '02:00', 'arrival_datetime': '13:15', 'source': 'Brno', 'destinations': 'Munich', 'price': 27.98, 'type': 'bus', 'source_id': 26323200, 'destination_id': 26383230, 'free_seats': None, 'carrier': 'Flixbus'}, {'departure_datetime': '03:35', 'arrival_datetime': '13:20', 'source': 'Brno', 'destinations': 'Munich', 'price': 28.89, 'type': 'bus', 'source_id': 26323200, 'destination_id': 26383230, 'free_seats': 2, 'carrier': 'Flixbus'}]"
