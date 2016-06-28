import requests
import json


class Tankerkoenig():
    """
    Wrapper for Tankerkönig-API calls.

    * Parameters:

        :api_key: ``str``; Tankerönik API key.
    """
    def __init__(self, api_key):
        self.api_key = api_key

    def __check(self, r):
        """
        Internal method to check wether request was successful.

        * Parameters:

            :r: ``request``; http response of api call.

        * Return:

            ``True`` if request was successful, ``Exception`` if not.
        """
        if r.status_code != 200 or \
                'application/json' not in r.headers['content-type']:
            raise Exception('Request failed.\n'
                            'Code: {}\nText: {}'.format(r.status_code, r.text))
        return True

    def list(self, lat, lng, rad, sort='dist', type='all'):
        """
        'List' request of tankerkoenig api. Returns a list of gas station close
        to a given location sorted by distance.

        * Parameters:

            :lat: ``float``; latitude of the chosen location.

            :lng: ``float``; longitude of the chosen location.

            :rad:
                ``float``;
                max radius around the given location in which gas stations
                should be searched.

            :sort:
                ``str``, default: ``'dist'``, options: ``('dist', 'price')``;
                sorts the results by either price ``('price')`` or distance
                ('dist').
                *Hint:* the sorting by price is only possible if the
                chosen fuel type is ``('diesel', 'e10', 'e5')`` and not
                ``all``.

            :type:
                ``str``, default: ``'all'``, options: ``('diesel', 'e10',
                'e5', 'all')``;
                can be set to return a specific fuel type ``('diesel', 'e10',
                'e5')``.
                *Hint:* the sorting by price is only possible if the
                chosen fuel type is ``('diesel', 'e10', 'e5')`` and not
                ``all``.


        * Return:

            ``dict``;
            returns a dictionary containing a list of stations
            (id: 'all_stations').

        """
        r = requests.get('https://creativecommons.tankerkoenig.de'
                         '/json/list.php',
                         params=dict(lat=lat, lng=lng, rad=rad, sort=sort,
                                     type=type, apikey=self.api_key))
        self.__check(r)
        return json.loads(r.text)

    def detail(self, id):
        """
        'Detail' request of tankerkoenig api. Returns detailed information of
        a specific gas station by id.

        * Parameters:

            :id: ``str``; gas station id provided by tankerkoenig.

        * Result:

            ``dict``;
            returns a dictionary with detailed information of the gas station
            corresponding to the given id.
        """
        r = requests.get('https://creativecommons.tankerkoenig.de/'
                         'json/detail.php',
                         params=dict(id=id, apikey=self.api_key))
        self.__check(r)
        return json.loads(r.text)
