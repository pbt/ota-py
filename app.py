from flask import Flask, render_template
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
    arrivals = [[train.route_id, train.headsign_text if train.headsign_text else train.shape_id, [update.arrival for update in train.stop_time_updates if any([update.stop_id == stop for stop in stops])][0]] for train in trains]
    return arrivals

@app.route('/')
def hello_world():
    arrivals = get_arrivals()
    relative_arrivals = [[route, dest, arrival_time, (arrival_time - datetime.now()).seconds // 60] for [route, dest, arrival_time] in arrivals]
    # (update.arrival - datetime.now()).seconds // 60
    return render_template('arrivals.html', arrivals=sorted([arr for arr in relative_arrivals if arr[3] < 30], key=lambda arr: arr[3]))
