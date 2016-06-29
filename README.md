Webapp to find the nearest and cheapest gas station based on the [Tankerkoenig API](https://creativecommons.tankerkoenig.de/) inspired by the IT-Talents' [monthly competition](https://www.it-talents.de/cms/aktionen/code-competition/code-competition-05-2016).
The website also uses [OpenLayers3](http://openlayers.org/en/latest/doc/quickstart.html).

# Requirements
* python>=3
* flask
* sqlalchemy
* bokeh
* geocoder


# Install
1. Clone the repository:
   ```bash
   $ git clone https://github.com/libeanim/refuelking.git
   ```

2. Create a virtual environment and activate it:
   ```bash
   $ virtualenv -p python3 my_environment
   $ source my_environment/bin/activate
   ```

3. Use pip to install required packages in the virtual environment:
   ```bash
   $ pip install -r requirements.txt
   ```

# Run
This is a simple explanation to run this website on a local flask test server.

1. After you finished the installation procedure, execute the `init_all.py` script in the activated virtual environment:
   ```bash
   python3 init_all.py
   ```
   This will generate the configuration file and requires your [Tankerkoenig api key](https://creativecommons.tankerkoenig.de/#register). It also initialises a `sqlite` database in the module directory called `sample.db`

2. Start now the `run_debug.py` script to start the server:
   ```bash
   python3 run_debug.py
   ```

3. That's it! You should now be able to access the website on [127.0.0.1:5000](http://127.0.0.1:5000/).


# Deployment
There are many ways to deploy a Flask website. Choose the one which is your favour or mandatory in the webspace you are using.

Then before you start the application set the following two environment variables:
* Set the app configuration to production mode:
  ```bash
  $ export APP_CONFIG="config.ProductionConfig"
  ```
* Set the url to your database:
  ```bash
  $ export DATABASE_URL="your_database_server.com/"
  ```

**Before the first run** make sure the configuration and database has been created. You can do that by executing the `init_all.py` script with the correct values for the environment variable `DATABASE_URL`.

# Future plans
* Predict future price developement according to last prices changes, similar to a [server load prediction](http://cs229.stanford.edu/proj2009/ChaidaroonKimSeo.pdf).
