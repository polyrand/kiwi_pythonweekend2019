#!/usr/bin/env python3
"""
Get array of trips
"""


__author__ = "Ricardo"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
from get_rides import get_rides

if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # # Required positional argument
    # parser.add_argument("arg", help="Required positional argument")

    # # Optional argument flag which defaults to False
    # parser.add_argument("-f", "--flag", action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-s", "--source", action="store", dest="source", required=True)

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument(
        "-d", "--destination", action="store", dest="destination", required=True
    )

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument(
        "-dd", "--departure_date", action="store", dest="departure_date", required=True
    )

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Verbosity (-v, -vv, etc)"
    )

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    args = parser.parse_args()

    get_rides(
        source_city=args.source, dst_city=args.destination, date=args.departure_date
    )

