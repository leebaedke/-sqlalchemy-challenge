# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"Static:<br/>"
        f"/api/v1.0/date_and_precipitation<br/>"
        f"/api/v1.0/last_year_precipitation_data<br/>"
        f"/api/v1.0/all_stations<br/>"
        f"/api/v1.0/tobs_most_active<br/>"
        f"/api/v1.0/last_year_of_tobs<br/>"
        f"Dynamic:<br/>"
        f"/api/v1.0/2016-08-24<br/>"
        f"/api/v1.0/2016-08-24/2017-08-24"
    )

# A precipitation route that Returns json with the date as the key and the value as the precipitation
@app.route('/api/v1.0/date_and_precipitation')
def date_and_precipitation():
   
    precipitation_scores = session.query(Measurement.date, Measurement.prcp).\
        order_by(Measurement.date).all()

    rain_dict = dict(precipitation_scores)
    return jsonify(rain_dict)

# A precipitation route that Only returns the jsonified precipitation data for the last year in the database
@app.route('/api/v1.0/last_year_precipitation_data')
def last_year_precipitation_data():
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    year_ago_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago_date).\
        order_by(Measurement.date).all()

    precipitation_dict = {date: prcp for date, prcp in precipitation_data}

    return jsonify(precipitation_dict)



# A Station route that Returns jsonified data of all of the stations in the database
@app.route('/api/v1.0/all_stations')
def all_stations():
    station_list = session.query(Station.station).\
    order_by(Station.station).all()

    station_data = []
    for station in station_list:
        station_data.append({'station': station[0]})
    
    return jsonify(station_data)

# A tobs route that Returns jsonified data for the most active station (USC00519281)
@app.route('/api/v1.0/tobs_most_active')
def tobs_most_active():
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    year_ago_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)

    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= year_ago_date).\
        order_by(Measurement.date).all()    

    active_list = [{'date': date, 'tobs': tobs} for date, tobs in tobs_data]

    return jsonify(active_list)
# A tobs route that Only returns the jsonified data for the last year of data
@app.route('/api/v1.0/last_year_of_tobs')
def last_year_of_tobs():
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    year_ago_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    
    year_of_tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= year_ago_date).\
        order_by(Measurement.date).all()


    tobs_list = [{'date': date, 'tobs': tobs} for date, tobs in year_of_tobs_data]

    return jsonify(tobs_list)

# A start route that Accepts the start and end dates as parameters from the URL 
#@app.route('


# A start/end route that Returns the min, max, and average temperatures calculated from the given start date to the given end date         
#@app.route('


           
if __name__ == "__main__":
    app.run(debug=True)




















