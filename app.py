import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    return (

        f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/temperatures<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation/")
def precipitation():

    session = Session(engine)
 
    # Query results to a dictionary using `date` as the key and `prcp` as the value.
    date = dt.datetime(2016, 8, 23)
    results = session.query(Measurement.prcp, Measurement.date).filter(Measurement.date > date).order_by(Measurement.date).all()

    session.close()

    # Create a list of dictionaries
    precip_results = []
    for prcp, date in results:
        precip_dict = {}
        precip_dict["precip"] = prcp
        precip_dict["date"] = date
        
        precip_results.append(precip_dict)

    return jsonify(precip_results)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_resulst = session.query(Station.name).distinct().all()
    session.close()
    return jsonify(station_resulst)
    

@app.route("/api/v1.0/temperatures")
def temperatures():
    session = Session(engine)
    date = dt.datetime(2016, 8, 23)
    temp_results = session.query(Measurement.tobs, Measurement.date).\
    filter(Measurement.station == "USC00519281").\
    filter(Measurement.date > date).\
    order_by(Measurement.date).all()
    session.close()
    
    # Create a list of dictionaries
    temp_results_list = []
    for tobs, date in temp_results:
        temp_dict = {}
        temp_dict["temps"] = tobs
        temp_dict["date"] = date
        
        temp_results_list.append(temp_dict)
    return jsonify(temp_results_list)

@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    
    sel = [func.avg(Measurement.tobs), 
       func.min(Measurement.tobs), 
       func.max(Measurement.tobs)] 
   
    temp_averages = session.query(*sel).filter(Measurement.date >= start).all()
    session.close()
    
    
    return jsonify(f"Here is the average temperature: {temp_averages[0][0]}, minimum temperature: {temp_averages[0][1]}, and maximum temperature: {temp_averages[0][2]} from {start} to 2017-08-23.")

@app.route("/api/v1.0/<start>/<end>")
def start_and_end_date(start, end):
    session = Session(engine)
    sel = [func.avg(Measurement.tobs), 
       func.min(Measurement.tobs), 
       func.max(Measurement.tobs)] 
   
    temp_averages = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    session.close()
    
    return jsonify(f"Here is the average temperature: {temp_averages[0][0]}, minimum temperature: {temp_averages[0][1]}, and maximum temperature: {temp_averages[0][2]} from {start} to {end}.")

if __name__ == "__main__":
    app.run(debug=True)
