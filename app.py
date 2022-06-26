from flask import Flask, render_template, redirect, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import json
import numpy as np
import pandas as pd
from bson import json_util
from climate_python import prcp_dic, station_names, temp_twelve_month, start_tobs_measures, end_tobs_measures

engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread': False})
Base = automap_base()


# reflect the tables
Base.prepare(engine, reflect=True)

Base.classes.keys()

measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)






app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end><br>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    return jsonify(prcp_dic)

@app.route("/api/v1.0/stations")
def stations():
    return json_util.dumps([datum for datum in station_names])

@app.route("/api/v1.0/tobs")
def tobs():
    return json_util.dumps([datum for datum in temp_twelve_month])


@app.route("/api/v1.0/<start>")
def start(start):
    return json_util.dumps(start_tobs_measures(start))
    

@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
    return json_util.dumps(end_tobs_measures(start, end))



