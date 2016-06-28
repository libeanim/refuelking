from datetime import datetime, timedelta
import numpy as np
import geocoder
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from bokeh.embed import components

from config import API_KEYS
from refuelking.api import Tankerkoenig
from refuelking.plots import get_price_plot

# Instantiating main app object
app = Flask(__name__)
# Instantiating configuration from class in config.py
app.config.from_object('config.DevelopmentConfig')
# Instantiating database
db = SQLAlchemy(app)
# Instantiating Tankerkoenig api wrapper
tk = Tankerkoenig(api_key=API_KEYS.TANKERKOENIG)

from refuelking.models import Price


# Define main page.
@app.route('/')
def index():
    return render_template('index.html')


# Define search page.
@app.route('/search')
def get_data():
    # Only accept get requests.
    if request.method == 'GET':
        # Get geo location via google maps api.
        geo = geocoder.google(
            '{}, Germany'.format(request.args.get('address')),
            region='DE', language='de')

        # Call Tankerkoenig api to get gas stations close to location.
        res = tk.list(lat=geo.lat, lng=geo.lng, rad=request.args.get('rad', 3))
        # Redirect to index page if there is an error in the request.
        if res['status'] != 'ok':
            return redirect(url_for('index'))

        # Update database with the station info received in the previous
        # Tankerkoenig api call.
        print("Start db update.")
        map(Price.update_price, res['stations'])
        db.session.commit()
        print("Update finished.")

        # Generate a list of all e10, e5 and diesel prices of the nearby
        # stations, as well as their coordinates.
        e10, e5, diesel, lats, lons = [], [], [], [], []
        stations = res['stations']
        time_diff = datetime.now() - timedelta(days=7)
        pr_out = {i: ([], [], []) for i in range(24)}

        # Iterate through all found stations.
        for station in stations:
            # Get Price data of the last 7 days of the currently iterated
            # station.
            prs = Price.query.filter(Price.station_id == station['id'],
                                     Price.date > time_diff).all()
            for pr in prs:
                # Group prices to the hour where they occured to identify the
                # hour where fuel was cheapest within the last week.
                pr_out[pr.date.hour][0].append(pr.e10)
                pr_out[pr.date.hour][1].append(pr.e5)
                pr_out[pr.date.hour][2].append(pr.diesel)

            # Create list for all fuel types (for later processing).
            e10.append(station['e10'])
            e5.append(station['e5'])
            diesel.append(station['diesel'])
            lats.append(station['lat'])
            lons.append(station['lng'])
        # Average all prices for each hour to get the average price per hour
        # for all fuel types.
        pr_out = np.array([(np.average(vals[0]),
                            np.average(vals[1]),
                            np.average(vals[2])) for vals in pr_out.values()])
        # Make sure that a price of 0 does not count.
        pr_out[pr_out == 0] = np.nan

        # Identify best prices and store the information in the stations list.
        for station in stations:
            station['top_prices'] = (station['e10'] == min(e10),
                                     station['e5'] == min(e5),
                                     station['diesel'] == min(diesel))

        return render_template('search.html', stations=stations,
                               rad=request.args.get('rad', 3),
                               average_prices=(np.average(e10),
                                               np.average(e5),
                                               np.average(diesel)),
                               pos=(geo.lat, geo.lng),
                               best_time=np.nanargmin(pr_out, axis=0))
    # Redirect to index page if it's not a GET request.
    return redirect(url_for('/'))


# Define station detail page.
@app.route('/station/<string:id>')
def get_station(id):
    # Tankerkoenig api call to get detailed station information
    station = tk.detail(id=id)['station']
    data = {'dates': [], 'diesel': [], 'e10': [], 'e5': []}
    time_diff = datetime.now() - timedelta(days=7)
    # Generate a list of fuel prices over the last 7 days.
    for price in Price.query.filter(Price.station_id == id,
                                    Price.date > time_diff).all():
        data['dates'].append(price.date)
        data['diesel'].append(price.diesel)
        data['e10'].append(price.e10)
        data['e5'].append(price.e5)
    # Generate a price plot and dismantle it to it's components (script, div)
    # element.
    price_plot = components(get_price_plot(data))
    return render_template('station.html', price_plot=price_plot,
                           station=station)
