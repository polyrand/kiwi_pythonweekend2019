"""Get list of buses for a day"""

from requests_html import HTMLSession
from redis_funcs import get_location_from_redis, add_location_to_redis
import json


def get_id(city: str) -> int:

    result = get_location_from_redis(city=city)

    payload = None

    if result:
        print("GOT id FROM REDIS")
        # print(result)
        return result
    else:
        session = HTMLSession()
        data = session.get(
            "https://d11mb9zho2u7hy.cloudfront.net/api/v1/cities?locale=en"
        )
        data_json = data.json()
        cities = data_json["cities"]
        all_cities = (cities[i] for i in cities)
        for c in all_cities:
            if c["name"] == city:
                payload = c["id"]

        if payload:
            add_location_to_redis(city=city, payload=payload)

            print("Had to re-fetch id")
            return payload
        else:
            return


# a = itertools.takewhile(lambda x: x["name"] == "Brno", all_cities)
# print(list(a))
