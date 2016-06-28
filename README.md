Webapp to find the nearest and cheapest gas station based on the [Tankerkoenig API](https://creativecommons.tankerkoenig.de/) inspired by the IT-Talents' [monthly competition](https://www.it-talents.de/cms/aktionen/code-competition/code-competition-05-2016).
The website also uses [OpenLayers3](http://openlayers.org/en/latest/doc/quickstart.html).

# Requirements
* python>=3
* flask
* sqlalchemy
* bokeh


# Install
Create a virtual environment and activate it:
```bash
$ virtualenv -p python3 my_environment
$ source my_environment/bin/activate
```

Use pip to install required packages:
```bash
$ pip install -r requirements.txt
```


# Run
Export following variables your created environment my_environment:

* Set the configuration to developement configuration (optional)
```bash
$ export CONFIG="config.DevelopmentConfig"
```
* Set url for the database conncetion (not required in developement mode)
```bash
$ export DATABASE_URL="your_database_server.com/"
```

**Before the first run** start the ``init_all.py`` script: ``python init_all.py``.
 Then run the server ``python run.py``


# Future plans
* Predict future price developement according to last prices changes, similar to a [server load prediction](http://cs229.stanford.edu/proj2009/ChaidaroonKimSeo.pdf).
