# Flask


from regex import D
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import numpy as np
import datetime as dt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Resources/hawaii.sqlite"

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

@app.route("/")
def Homepage():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs_page</br>"
        f"/api/v1.0/<start></br>"
        f"/api/v1.0/<start>/<end>"
    )


date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= date).all()
prcp_dict = {date: prcp for date, prcp in query}

@app.route("/api/v1.0/precipitation")
def precipitation():
    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()
    return jsonify(stations)


@app.route("/api/v1.0/tobs_page")
def tobs_page():
    tobs_query = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281', Measurement.date >= date).all()
    tobs_list = list(np.ravel(tobs_query))
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def temperature(start):

    start = dt.datetime.strptime(start, "%y %m %D")

    temp_query = session.query(Measurement.station, Measurement.date, func.max(Measurement.tobs), 
    func.min(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    temps = list(np.ravel(temp_query))
    return jsonify(temps)





@app.route("/api/v1.0/<start>/<end>")
def temperature(start, end):

    start = dt.datetime.strftime(start, "%y-%m-%D")
    end = dt.datetime.strftime(end, "%y-%m-%D")

    temp_query = session.query(Measurement.station, Measurement.date, func.max(Measurement.tobs), 
    func.min(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end_date).all()

    temps = list(np.ravel(temp_query))
    return jsonify(temps)


if __name__=="__main__":
    app.run(debug=True)
