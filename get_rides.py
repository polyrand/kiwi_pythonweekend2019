from get_id import get_id
from redis_funcs import get_journey_from_redis, add_journey_to_redis


from requests_html import HTMLSession, Element

import datetime
from functools import partial
import re


def parse_date(date_string: str) -> str:
    format = r"%Y-%m-%d"
    date = datetime.datetime.strptime(date_string, format)
    return date.strftime(r"%d.%m.%Y")


def get_ride_info(ride: Element) -> dict:
    price = float(ride.find("span.num.currency-small-cents")[0].text.split("\xa0")[0])
    departure_time = ride.find("div.ride-times")[0].text.split()[0]
    arrival_time = ride.find("div.ride-times")[0].text.split()[1]
    seats_str = ride.find("div.seats-notice")
    source = ride.find("div.departure-station-name")[0].text
    destination = ride.find("div.arrival-station-name")[0].text

    # duration = ride.find("div.duration")

    # departure = date + departure_time
    # arrival = departure + trip_length

    if seats_str and len(seats_str) > 0:
        seats_str = ride.find("div.seats-notice")[0].text

        matcher = re.match("(\d+)\s+\w+", seats_str)
        if matcher:
            seats_available = int(matcher.groups()[0])
    else:
        seats_available = None

    return {
        "departure_datetime": departure_time,
        "arrival_datetime": arrival_time,  # "2018-06-20 15:00:00",
        "source": source,
        "destinations": destination,
        "price": price,  # in EUR - you can use https://api.skypicker.com/rates
        "type": "bus",  # optional (bus/train)
        "source_id": 26323200,  # optional (carrier’s id)
        "destination_id": 26383230,  # optional (carrier’s id)
        "free_seats": seats_available,  # optional
        "carrier": "Flixbus",  # optional
    }


def get_rides(source_city: str, dst_city: str, date: str) -> str:
    # source_city = source_city
    # dst_city = dst_city
    source = get_id(source_city)
    destination = get_id(dst_city)
    date = parse_date(date)
    # print(date)

    result = get_journey_from_redis(
        source=source_city, destination=dst_city, dep_date=date
    )

    if result:
        print("GOT RESULT FROM REDIS")
        print(result)
        return result

    else:
        session = HTMLSession()
        r = session.get(
            f"https://shop.global.flixbus.com/search?departureCity={source}&arrivalCity={destination}&route={source_city}-{dst_city}&rideDate={date}&adult=1&_locale=en&currency=EUR"
        )

        container = r.html.find("#results-group-container-direct")

        if len(container) > 0:
            container = container[0]

            rides = container.find("div.ride-item-pair")
            # mapper = partial(get_ride_info, source_city=source_city, dst_city=dst_city)
            # print(list(map(mapper, rides)))
            payload = list(map(get_ride_info, rides))

            add_journey_to_redis(
                source=source_city,
                destination=dst_city,
                dep_date=date,
                payload=str(payload),
            )

            print(payload)
            return str(payload)
        else:
            return ""


# get_rides(source_city="Brno", dst_city="Munich", date="2019-11-20")

