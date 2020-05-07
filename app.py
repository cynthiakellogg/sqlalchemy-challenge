import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()
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
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/temperatures"
        
    )

# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
 
    # Query results to a dictionary using `date` as the key and `prcp` as the value.
    results = session.query(Measurement.prcp, Measurement.date).filter(Measurement.date > date).order_by(Measurement.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    precip_results = []
    for date, precip in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["precip"] = prcp
        
        precip_results.append(precip_dict)

    return jsonify(precip_results)

# 5. Define what to do when a user hits the /about route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
# 6. Define what to do when a user hits the /about route
@app.route("/api/v1.0/temperatures")
def temperatures():
    session = Session(engine)
    
# @app.route("/jsonified")
# def jsonified():
#     return jsonify(hello_dict)

    
    
if __name__ == "__main__":
    app.run(debug=True)
