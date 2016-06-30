import requests
import time

SLEEP = 15
RAD = 15
CITIES = ['Bremen', 'Berlin', 'Heidelberg', 'Köln', 'Düsseldorf', 'Essen',
          'Karlsruhe', 'Stuttgart', 'Frankfurt', 'Potsdam', 'Dortmund',
          'Hamburg', 'München', 'Bielefeld']

while True:
    print('Requesting...')
    for city in CITIES:
        requests.get('http://libeanim.shaula.uberspace.de/projects/refuelking/'
                     'search?address={}&rad={}'.format(city, RAD))
        print(city, 'OK.')
    print('Done.\nSleep for {} mins.\n'.format(SLEEP))
    time.sleep(SLEEP * 60)
