import os
from datetime import datetime, timedelta
import numpy as np
import geocoder
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from bokeh.embed import components
from bokeh.resources import CDN

from config import API_KEYS
from refuelking.api import Tankerkoenig
from refuelking.plots import get_price_plot

# Instantiating main app object
app = Flask(__name__)
# Instantiating configuration from class in config.py loaded from a environment
# variable.
app.config.from_object(os.environ['APP_SETTINGS'])
# Instantiating database
db = SQLAlchemy(app)
# Instantiating Tankerkoenig api wrapper
tk = Tankerkoenig(api_key=API_KEYS.TANKERKOENIG)

from refuelking.models import Price


def update_price(station):
    """
    Update station information in the database of the given station.

    * Parameters:

        :station:
            ``dict``;
            station object provided by the Tankerkoenig api.
    """
    # Find a price entry of the given station within the last 60 minutes.
    pr = Price.query.filter(Price.station_id == station['id'],
                            Price.date > datetime.now() -
                            timedelta(seconds=60**2)).order_by(
                                Price.date.desc()).first()
    # If there is no entry add the new one otherwise if an entry exists
    # only add the provided information when the prices have changed.
    if not pr or not (pr.diesel == int(station['diesel'] * 1000) and
                      pr.e10 == int(station['e10'] * 1000) and
                      pr.e5 == int(station['e5'] * 1000)):
        # import pdb; pdb.set_trace()
        db.session.add(Price(station_id=station['id'],
                             diesel=station['diesel'],
                             e10=station['e10'],
                             e5=station['e5'],
                             date=datetime.now()))


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
        for station in res['stations']:
            update_price(station)
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
                # Divide it by 1000 to convert to correct float
                pr_out[pr.date.hour][0].append(pr.e10 / 1000)
                pr_out[pr.date.hour][1].append(pr.e5 / 1000)
                pr_out[pr.date.hour][2].append(pr.diesel / 1000)

            # Create list for all fuel types (for later processing).
            e10.append(station['e10'])
            e5.append(station['e5'])
            diesel.append(station['diesel'])
            lats.append(station['lat'])
            lons.append(station['lng'])
        # Average all prices for each hour to get the average price per hour
        # for all fuel types.
        pr_out = np.array([(np.average(vals[0]) if vals[0] else 0,
                            np.average(vals[1] if vals[1] else 0),
                            np.average(vals[2]) if vals[2] else 0
                            ) for vals in pr_out.values()])

        # Identify best prices and store the information in the stations list.
        for station in stations:
            station['top_prices'] = (station['e10'] == min(e10),
                                     station['e5'] == min(e5),
                                     station['diesel'] == min(diesel))
        if np.all(pr_out == 0):
            best_time = ('?', '?', '?')
        else:
            # Make sure that a price of 0 does not count.
            pr_out[pr_out == 0] = np.nan
            best_time = np.nanargmin(pr_out, axis=0)

        return render_template('search.html', stations=stations,
                               rad=request.args.get('rad', 3),
                               average_prices=(np.average(e10),
                                               np.average(e5),
                                               np.average(diesel)),
                               pos=(geo.lat, geo.lng),
                               best_time=best_time)
    # Redirect to index page if it's not a GET request.
    return redirect(url_for('/'))


# Define station detail page.
@app.route('/station/<string:id>')
def get_station(id):
    # Tankerkoenig api call to get detailed station information
    station = tk.detail(id=id)['station']
    data = {'dates': [], 'diesel': [], 'e10': [], 'e5': []}
    time_diff = datetime.now() - timedelta(days=7)
    # Generate price plot, but only if there are more than 2 results
    # in database.
    if Price.query.filter(Price.station_id == id,
                          Price.date > time_diff).count() > 2:
        # Generate a list of fuel prices over the last 7 days.
        for price in Price.query.filter(Price.station_id == id,
                                        Price.date > time_diff).all():
            data['dates'].append(price.date)
            data['diesel'].append(price.diesel / 1000)
            data['e10'].append(price.e10 / 1000)
            data['e5'].append(price.e5 / 1000)

        # Generate a price plot and dismantle it to it's components
        # (script, div) element.
        price_plot = components(get_price_plot(data), CDN)
    else:
        price_plot = ('', '<p>Preisentwicklung kann nicht dargestellt werden, '
                      'da nicht genügend Daten vorhanden sind.</p>')
    return render_template('station.html', price_plot=price_plot,
                           station=station)
