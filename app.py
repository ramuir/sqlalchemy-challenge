import pandas as pd 
import numpy as np 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_, or_ 

from flask import Flask, jsonify
import datetime as dt


# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():

# Create our session (link) from Python to the DB
    session = Session(engine)
   
    """Return a dictionary for date and precipitation"""

    # Query all dates and prcp
    dates_prcp = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

 # Convert the query results to a dictionary using date as the key and prcp as the value.

    precipitation_dates = []
    for date, prcp in dates_prcp:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_dates.append(precipitation_dict)

    return jsonify(precipitation_dates)



@app.route("/api/v1.0/stations")
def stations():

# Create our session (link) from Python to the DB
    session = Session(engine)
   
    """Return a dictionary for stations"""

    # Query all stations
    results = session.query(Station.station).all()

    session.close()

 # Convert the query results to json list.

    stations = list(np.ravel(results)) 

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    """quering most active stations and temps obeserved over last 12 months"""
#Query the dates and temperature observations of the most active station for the last year of data.
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)

    lastyear_temps = session.query(Measurement.tobs, Measurement.date).\
                 filter(and_(Measurement.station == 'USC00519281',\
                      Measurement.date >= query_date)).all()


#Return a JSON list of temperature observations (TOBS) for the previous year.

    return jsonify(lastyear_temps)

if __name__ == '__main__':
    app.run(debug=True)

