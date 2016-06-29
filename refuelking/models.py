from refuelking import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta


class Price(db.Model):
    """
    Simple table model which stores the station id and the available prices.

    * Parameters:

        :station_id:

            ``str``;
            station id which is provided by the Tankerkoenig api.

        :diesel:
            ``float``;
            price of diesel fuel.

        :e10:
            ``float``;
            price of e10 fuel.

        :e5:
            ``float``;
            price of e5 fuel.

        :date:
            ``datetime.datetime``, default: ``datetime.now()``;
            datetime whe the prices were gathered.
    """

    __tablename__ = 'prices'

    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String(36), nullable=False, index=True)
    diesel = db.Column(db.Float(precision='2,3'), nullable=False)
    e10 = db.Column(db.Float(precision='2,3'), nullable=False)
    e5 = db.Column(db.Float(precision='2,3'), nullable=False)
    date = db.Column(db.DateTime)

    def __init__(self, station_id, diesel, e10, e5, date=datetime.now()):
        self.station_id = station_id
        self.diesel = diesel
        self.e10 = e10
        self.e5 = e5
        self.date = date

    @staticmethod
    def update_price(station):
        """
        Update station information in the database of the given station.

        * Parameters:

            :station:
                ``dict``;
                station object provided by the Tankerkoenig api.
        """
        # Find a price entry of the given station within the last 15 minutes.
        pr = Price.query.filter(Price.station_id == station['id'],
                                Price.date > datetime.now() -
                                timedelta(seconds=15 * 60)).order_by(
                                    Price.date).first()
        # If there is no entry add the new one otherwise if an entry exists
        # only add the provided information when the prices have changed.
        if not pr or not (pr.diesel == station['diesel'] and
                          pr.e10 == station['e10'] and
                          pr.e5 == station['e5']):
            db.session.add(Price(station_id=station['id'],
                                 diesel=station['diesel'],
                                 e10=station['e10'],
                                 e5=station['e5']))
