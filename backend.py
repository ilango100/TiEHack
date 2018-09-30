import json
import pandas as pd
from flask import Flask,request

df = pd.read_csv("china_aqi.csv",parse_dates=["est_time"],index_col="est_time")

app = Flask(__name__)

@app.route("/index.html",methods=["GET"])
def index():
    print("index")
    return open("index.html").read()

@app.route("/getdates",methods=["GET"])
def senddates():
    return json.dumps(list(map(str,(set(df.index.date)))))

@app.route("/gettimes",methods=["GET"])
def sendtimes():
    request.parameter_storage_class = dict
    print(request.args)
#     df.index.time[df.index.date == request.args["date"]]
    dts = df.index[df.index.date == pd.to_datetime(request.args["date"]).date()].time
    dts = list(map(str,set(dts)))
    return json.dumps(dts)

@app.route("/getdata",methods=["GET"])
def senddata():
    request.parameter_storage_class = dict
    print(request.args)
    return df[df.index == pd.to_datetime(request.args["date"]+" "+request.args["time"])].to_json(orient="records")
    
app.run("0.0.0.0",2000)
