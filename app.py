from flask import Flask, render_template, redirect, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import json
import numpy as np
import pandas as pd
from bson import json_util
import datetime as dt

engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread': False})
Base = automap_base()


# reflect the tables
Base.prepare(engine, reflect=True)

Base.classes.keys()

measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)

annual_prcp = session.query(measurement.date, measurement.prcp).\
                  filter(measurement.date >= dt.datetime(2016, 8, 23, 0)).all()
dates = []
prcp = []
for row in annual_prcp:
    dates.append(row[0])
    prcp.append(row[1])


prcp_dic = {'Date' : dates, 'Percipitation' : prcp}
# Save the query results as a Pandas DataFrame and set the index to the date column
prcp_df = pd.DataFrame(prcp_dic)

prcp_df.head()

# Sort the dataframe by date

sorted_prcp_df = prcp_df.sort_values(by='Date')


app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br>"
        "/api/v1.0/stations<br>"
        "/api/v1.0/tobs<br>"
        "/api/v1.0/startdate<br>"
        "/api/v1.0/startdate/enddate<br>"
    )

sel = [func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]

@app.route("/api/v1.0/precipitation")
def prcp():
    return jsonify(prcp_dic)

@app.route("/api/v1.0/stations")
def stations():
    station_names = session.query(station.name).\
    filter(measurement.station == station.station).\
    group_by(station.id).all()
    return json_util.dumps([datum for datum in station_names])

@app.route("/api/v1.0/tobs")
def tobs():
    temp_twelve_month = session.query(measurement.tobs).\
    filter(measurement.station == station.station).\
    filter(measurement.date >= dt.datetime(2016, 8, 23, 0)).\
    filter(station.name == 'WAIHEE 837.5, HI US').all()
    return json_util.dumps([datum for datum in temp_twelve_month])


@app.route("/api/v1.0/<start>")
def start(start):
    data = session.query(*sel).\
    filter(measurement.date >= str(start)).all()
    return json_util.dumps([datum for datum in data])
    

@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
    start=dt.datetime.strptime(start, '%Y-%m-%d')
    end=dt.datetime.strptime(end, '%Y-%m-%d')
    results = session.query(*sel).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()
    return json_util.dumps([datum for datum in results])



