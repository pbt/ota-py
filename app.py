from flask import Flask, render_template, request

app = Flask(__name__)

import os

from nyct_gtfs import NYCTFeed

from nyct_gtfs.gtfs_static_types import Stations

from datetime import datetime, date, time, timezone, tzinfo, timedelta
import arrow
from itertools import groupby, chain

from tzlocal import get_localzone

import cachetools.func

ApiKey = os.environ["API_KEY"]

# TODO: instantiate all the feeds, and manually refresh them.
# or use a queue


@cachetools.func.ttl_cache(maxsize=2, ttl=60)
def get_arrivals(stations):
    print(str(arrow.utcnow()), "getting arrivals")

    feeds = (
        NYCTFeed("1", api_key=ApiKey),
        NYCTFeed("A", api_key=ApiKey),
        NYCTFeed("G", api_key=ApiKey),
        NYCTFeed("F", api_key=ApiKey),
        NYCTFeed("R", api_key=ApiKey),
    )

    trains = []

    directional_stations = [(f"{station}N", f"{station}S") for station in stations]
    stops = list(chain.from_iterable(directional_stations))

    for stop in stops:
        for feed in feeds:
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

    return (arrivals, arrow.utcnow())


@app.route("/")
def countdown():
    stop_ids = tuple(request.args.get("stop_ids", "A41,R29").split(","))
    arrivals, last_updated = get_arrivals(stop_ids)
    station_name = Stations().get_station_name(stop_ids[0])

    relative_arrivals = [
        {
            "route": route,
            "dest": dest,
            "arrival_time": arrow.get(arrival_time, get_localzone()).isoformat(),
            "relative": (arrival_time - datetime.now()).seconds // 60,
            "direction": direction,
            "trip_id": trip_id,
        }
        for (route, dest, arrival_time, direction, trip_id) in arrivals
    ]
    return render_template(
        "arrivals.html",
        stop_ids=stop_ids,
        station_name=station_name,
        mode=request.args.get("mode", "detailed"),
        last_updated=(last_updated, last_updated.humanize(arrow.utcnow())),
        arrivals=sorted(
            [arr for arr in relative_arrivals if arr["relative"] < 30],
            key=lambda arr: arr["arrival_time"],
        ),
    )
