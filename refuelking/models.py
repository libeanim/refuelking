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
    diesel = db.Column(db.Integer, nullable=False)
    e10 = db.Column(db.Integer, nullable=False)
    e5 = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime)

    def __init__(self, station_id, diesel, e10, e5, date=datetime.now()):
        self.station_id = station_id
        # all prices are multiplied by 1000 to preseve 3 float digits and
        # then stored as int for easier handling
        self.diesel = (int(diesel * 1000) if not isinstance(diesel, int)
                       else diesel)
        self.e10 = int(e10 * 1000) if not isinstance(e10, int) else e10
        self.e5 = int(e5 * 1000) if not isinstance(e5, int) else e5
        self.date = date
