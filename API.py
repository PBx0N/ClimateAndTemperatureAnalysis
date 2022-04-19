from flask import Flask, jsonify, render_template, request
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# Reflect database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement_Table = Base.classes.measurement

Station_Table = Base.classes.station

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

### List all routes that are available ###

@app.route("/")

def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
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

    recent_prcp = session.query(Measurement_Table.date, Measurement_Table.prcp).filter(Measurement_Table.date >= '2016-08-22').filter(Measurement_Table.date <= '2017-08-23').order_by(Measurement_Table.date).all()
    
    # convert results to a dictionary with date as key and prcp as value
    dict_ver = {}
    for date, prcp in recent_prcp:
        dict_ver[date] = prcp
    
    session.close()

    # return json list of dictionary
    return jsonify(dict_ver)
    
@app.route("/api/v1.0/stations")

def stations():

    session = Session(engine)
    
    Stations_results = session.query(Station_Table.station, Station_Table.id, Station_Table.name, Station_Table.latitude, Station_Table.longitude, Station_Table.elevation).all()

    session.close()
    
    all_stations = list(np.ravel(Stations_results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")

def tobs():
    
    session = Session(engine)
    
    ActiveStationData_12Months = session.query(Measurement_Table.tobs).filter(Measurement_Table.date >= '2016-08-22').filter(Measurement_Table.station == "USC00519281").all()
    
    session.close()
    
    all_temperatures = list(np.ravel(ActiveStationData_12Months))
    
    return jsonify(all_temperatures)
    
@app.route("/api/v1.0/<start>")

def StartDate(start):
    
    session = Session(engine)
    
    try:
    
        start = dt.datetime.strptime(start, "%Y-%m-%d")

        StartDate = session.query(func.min(Measurement_Table.tobs),
                            func.max(Measurement_Table.tobs),
                            func.avg(Measurement_Table.tobs)).filter(Measurement_Table.date >= start).all()

        session.close()
        
        startdate = list(np.ravel(StartDate))
        dict_startdate =  {"Min_Temp":startdate[0],"Max_Temp":startdate[1],"Ave_Temp":startdate[2]}
    
        return jsonify(dict_startdate)
    
    except ValueError:
        return "Please enter date in the format of YYYY-MM-DD"
    
@app.route("/api/v1.0/<start>/<end>")


def TempBetweenStarttoEndDate(start, end):
    
    session = Session(engine)
    
    try:
    
        start = dt.datetime.strptime(start, "%Y-%m-%d")
        end = dt.datetime.strptime(end, "%Y-%m-%d")
        
        if start >= end:
             return jsonify({
                    "error": f' The start date of {start} is greater than the end date of {end}'
                })
        else:
            TempBetween = session.query(func.min(Measurement_Table.tobs),
                            func.max(Measurement_Table.tobs),
                            func.avg(Measurement_Table.tobs)).filter(Measurement_Table.date >= start).filter(Measurement_Table.date <= end).all()
            session.close()
        
            TempBetween_Data = list(np.ravel(TempBetween))
            dict_TempBetween =  {"Start_Date": start, "End_date": end,  "Min_Temp":TempBetween_Data[0],"Max_Temp":TempBetween_Data[1],"Ave_Temp":TempBetween_Data[2]}
    
            return jsonify(dict_TempBetween)
    
    except ValueError:
        return "Please enter date in the format of YYYY-MM-DD"


if __name__ == '__main__':
    app.run(debug=True)

