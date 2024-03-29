# Import necessary libraries
import numpy as np
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Create engine
engine = create_engine("sqlite:///sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")

# Reflect database into ORM classes
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session
session = Session(engine)

# Create Flask app
app = Flask(__name__)

# Define function to calculate one year ago date
def get_one_year_ago():
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    return dt.datetime.strptime(most_recent_date, '%Y-%m-%d').date() - dt.timedelta(days=365)

# Define function to parse date
def parse_date(date_string):
    return dt.datetime.strptime(date_string, "%Y-%m-%d")

# Define routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        "Welcome to the Hawaii Climate Analysis API!<br/>"
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/&lt;start_date&gt;<br/>"
        "/api/v1.0/&lt;start_date&gt;/&lt;end_date&gt;<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last 12 months."""
    one_year_ago = get_one_year_ago()
    results = session.query(Measurement.date, Measurement.prcp).\
              filter(Measurement.date >= one_year_ago).all()
    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature observations for the last 12 months."""
    one_year_ago = get_one_year_ago()
    most_active_station = session.query(Measurement.station).\
                          group_by(Measurement.station).\
                          order_by(func.count(Measurement.station).desc()).first()[0]
    results = session.query(Measurement.date, Measurement.tobs).\
              filter(Measurement.station == most_active_station).\
              filter(Measurement.date >= one_year_ago).all()
    temperature_data = [{date: tobs} for date, tobs in results]
    return jsonify(temperature_data)

@app.route("/api/v1.0/<start_date>")
def temp_start(start_date):
    """Return TMIN, TAVG, and TMAX for all dates greater than or equal to the start date."""
    start_date = parse_date(start_date)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= start_date).all()
    temp_stats = list(np.ravel(results))
    return jsonify(temp_stats)

@app.route("/api/v1.0/<start_date>/<end_date>")
def temp_range(start_date, end_date):
    """Return TMIN, TAVG, and TMAX for dates between the start and end date inclusive."""
    start_date = parse_date(start_date)
    end_date = parse_date(end_date)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= start_date).\
              filter(Measurement.date <= end_date).all()
    temp_stats = list(np.ravel(results))
    return jsonify(temp_stats)

if __name__ == '__main__':
    app.run(debug=True)