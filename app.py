from flask import Flask, render_template, request

app = Flask(__name__)

import os

from nyct_gtfs import NYCTFeed
from nyct_gtfs.gtfs_static_types import Stations

from datetime import datetime, date, time, timezone, tzinfo, timedelta
from itertools import groupby

import cachetools.func

ApiKey = os.environ["API_KEY"]


@cachetools.func.ttl_cache(maxsize=2, ttl=60)
def get_arrivals():
    print(str(datetime.now()), "getting arrivals")
    feedACE = NYCTFeed("A", api_key=ApiKey)
    feedF = NYCTFeed("F", api_key=ApiKey)
    feedR = NYCTFeed("R", api_key=ApiKey)
    stations = Stations()

    trains = []

    # Stop IDs for Jay St-MetroTech
    stops = ["A41N", "A41S", "R29N", "R29S"]

    for stop in stops:
        for feed in [feedACE, feedF, feedR]:
            trains += feed.filter_trips(headed_for_stop_id=stop, underway=True)
    arrivals = [
        (
            train.route_id,
            train.headsign_text if train.headsign_text else train.shape_id,
            [
                update.arrival
                for update in train.stop_time_updates
                if any([update.stop_id == stop for stop in stops])
            ][0],
            train.direction,
            train.trip_id,
        )
        for train in trains
    ]
    return (arrivals, datetime.now())


@app.route("/")
def countdown():
    arrivals, last_updated = get_arrivals()
    relative_arrivals = [
        {
            "route": route,
            "dest": dest,
            "arrival_time": arrival_time,
            "relative": (arrival_time - datetime.now()).seconds // 60,
            "direction": direction,
            "trip_id": trip_id,
        }
        for (route, dest, arrival_time, direction, trip_id) in arrivals
    ]
    return render_template(
        "arrivals.html",
        mode=request.args.get("mode", "simple"),
        last_updated=str(last_updated),
        arrivals=sorted(
            [arr for arr in relative_arrivals if arr["relative"] < 30],
            key=lambda arr: arr["arrival_time"],
        ),
    )
