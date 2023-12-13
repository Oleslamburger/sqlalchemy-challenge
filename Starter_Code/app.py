# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
import datetime as dt
app = Flask(__name__)

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

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def index():
    return(f"Aloha! If using start or start/end routes please format in YYYY-D-M format.<br/>"
            f"/api/v1.0/precipitation<br/>"
           f"/api/v1.0/stations<br/>"
           f"/api/v1.0/tobs<br/>"
           f"/api/v1.0/start<br/>"
           f"/api/v1.0/start/end")

@app.route("/api/v1.0/precipitation")
def Precipitation():
    session = Session(engine)
    temperature = session.query(Measurement.date, func.avg(Measurement.prcp)).\
    filter(Measurement.date >= dt.date(2016,8,23)).group_by(Measurement.date).all()
    session.close()

# prepare to jsonify
    temperature_json_prep = []
    for date, prcp in temperature:
        temperature_dict = {}
        temperature_dict["date"] = date
        temperature_dict["temperature"] = prcp
        temperature_json_prep.append(temperature_dict)
    
    return jsonify(temperature_json_prep)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(Station.station, Station.name, Station.latitude,Station.longitude, Station.elevation).all()
    session.close()

# prepare to jsonify
    stations_json_prep = []
    for station, name, latitude, longitude, elevation in stations:
        stations_dict = {}
        stations_dict["station"] = station
        stations_dict["name"] = name
        stations_dict["latitude"] = latitude
        stations_dict["longitude"] = longitude
        stations_dict["elevation"] = elevation
        stations_json_prep.append(stations_dict)
    
    return jsonify(stations_json_prep)

@app.route("/api/v1.0/tobs")
def Temperatures():
    session = Session(engine)
    active_station = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= dt.date(2016,8,23)).filter(Measurement.station == 'USC00519281').all()
    session.close()

# prepare to jsonify
    active_station_json_prep = []
    for date, tobs in active_station:
        active_station_dict = {}
        active_station_dict["date"] = date
        active_station_dict["temperature"] = tobs
        active_station_json_prep.append(active_station_dict)
    
    return jsonify(active_station_json_prep)

@app.route("/api/v1.0/<start>")
def onward_date(start):
    session = Session(engine) 
    min_max_avg_start = session.query(Measurement.station,func.min(Measurement.tobs),\
    func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()

    # prepare to jsonify
    min_max_avg_json_prep = []
    min_max_avg_start_dict = {}
    min_max_avg_start_dict["Min"] = min_max_avg_start[0][1]
    min_max_avg_start_dict["Max"] = min_max_avg_start[0][2]
    min_max_avg_start_dict["Avg"] = min_max_avg_start[0][3]
    min_max_avg_json_prep.append(min_max_avg_start_dict)

    return jsonify (min_max_avg_json_prep)


@app.route("/api/v1.0/<start>/<end>")
def between_date(start, end):
    session = Session(engine) 
    min_max_avg_start_end = session.query(Measurement.station,func.min(Measurement.tobs),\
    func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date <= end).\
    filter(Measurement.date >=start).all()

    session.close()

    # prepare to jsonify
    min_max_avg_start_end_json_prep = []
    min_max_avg_start_end_dict = {}
    min_max_avg_start_end_dict["Min"] = min_max_avg_start_end[0][1]
    min_max_avg_start_end_dict["Max"] = min_max_avg_start_end[0][2]
    min_max_avg_start_end_dict["Avg"] = min_max_avg_start_end[0][3]
    min_max_avg_start_end_json_prep.append(min_max_avg_start_end_dict)

    return jsonify (min_max_avg_start_end_json_prep)

if __name__ == "__main__":
    app.run(debug=True)