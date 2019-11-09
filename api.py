from flask import Flask, render_template, jsonify, request
from dateutil.parser import parse as date_parse
from get_rides import get_rides

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["GET"])
def search():

    searchForm = request.args

    parsedSearchForm = {
        "from": searchForm["from"],
        "to": searchForm["to"],
        # "date": searchForm["date"],
        "date": searchForm["date"].split("T")[0],
    }

    # search_results = get_rides(
    #     source_city=request.args.get("from"),
    #     dst_city=request.args.get("to"),
    #     date=request.args.get("date"),
    # )

    print(parsedSearchForm)

    search_results = get_rides(
        source_city=parsedSearchForm["from"],
        dst_city=parsedSearchForm["to"],
        date=parsedSearchForm["date"],
    )

    # print(date_parse(request.args.get("date")))
    # print(search_results)
    # search_results = [
    #     {
    #         "from": "BCN",
    #         "to": "PRG",
    #         "departure": "2019, 9, 16",
    #         "return": "2096, 9, 16",
    #         "price": 200.5,
    #     },
    #     {
    #         "from": "BCN",
    #         "to": "PRG",
    #         "departure": "2019, 9, 17",
    #         "return": "2096, 9, 18",
    #         "price": 200.5,
    #     },
    # ]
    return jsonify(results=search_results)


if __name__ == "__main__":
    app.run(port=8080)
