# Refuelking

This is a simple webapp to find the nearest and cheapest gas station based on the [Tankerkoenig API](https://creativecommons.tankerkoenig.de/) and the [CC by 4.0](https://creativecommons.org/licenses/by/4.0/legalcode) license for the IT-Talents' [monthly competition](https://www.it-talents.de/cms/aktionen/code-competition/code-competition-05-2016).
All maps in this webapp are rendered through the [OpenLayers](http://openlayers.org/) library and the frontend of this app is in german.

**Click [here](http://libeanim.shaula.uberspace.de/projects/refuelking/) for a working demo.**

## Requirements

* python3
* virtualenv
* pip

### Python dependencies
*These packages can be installed via pip, see installation instructions below.*
* flask
* flask-sqlalchemy
* bokeh
* geocoder


## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/libeanim/refuelking.git
   ```

2. Create a virtual environment and activate it:
   ```bash
   virtualenv -p python3 my_environment
   source my_environment/bin/activate
   ```

3. Use pip to install required packages in the virtual environment:
   ```bash
   cd refuelking
   pip install -r requirements.txt
   ```

## Run Test Server
This is a simple explanation to run this website on a local flask test server.

1. After you finished the installation procedure, execute the `init_all.py` script in the activated virtual environment:
   ```bash
   python3 init_all.py
   ```
   This will generate the configuration file and requires your Tankerkoenig [api key](https://creativecommons.tankerkoenig.de/#register). It also initialises a `sqlite` database in the module directory called `sample.db`

2. Execute now the `run_debug.py` script to start the server:
   ```bash
   python3 run_debug.py
   ```

3. That's it! You should now be able to access the website on [http://127.0.0.1:5000/](http://127.0.0.1:5000/).


## Deployment
There are many ways to deploy a Flask application. Choose your favorite or mandatory way according to your webspace provider.

Then before you start the application set the following two environment variables:
* Set the app configuration to production mode:
   ```bash
   export APP_CONFIG="config.ProductionConfig"
   ```

* Set the url to your database:
   ```bash
   export DATABASE_URL="mysql+oursql://username:password@server/database"
   ```
   More information on the sqlalchemy database url format can be found [here](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls).

   *Hint: A working engine for mysql and python3 is `oursql`*

**Before the first run** make sure the configuration and database has been created. You can do that by executing the `init_all.py` script with the correct value for the environment variable `DATABASE_URL`.
