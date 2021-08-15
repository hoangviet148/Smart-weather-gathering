from flask import request, jsonify

from models.SensorData import SensorData
from ML import conclusion, prediction
import time
import datetime
from socketIO.init import socketio

def postSensorData():
    try:
        # get data from sensor
        now = datetime.datetime.now()
        data = request.get_json()
        print("===========sensor data================")
        print(data)
        print("\n")
        # **body unpacks the body dictionary into the Movie object as named parameters
        # For example if body = {"temp": 20, "humi": 85},
        # Then SensorData(**body) is the same as SensorData(temp=20, humi=85)
        # sensorData = SensorData(**body).save()
        temp = float(data['temperature'])
        humid = float(data['humidity'])
        uvid = float(data['uv'])
        pres = float(data['pressure'])
        data = [temp, humid, pres, uvid]

        if str(temp) == None or str(humid) == None or str(uvid) == None or str(pres) == None:
            return {"msg": "Invalid value from sensor"}, 400

        # make conclusion
        y = conclusion.predict(data)
        fields = ["temperature", "humidity", "pressure", "uv", "wdir", "wspd", "conclusion"]
        res = {}
        for k, v in zip(fields, y):
            res[k] = v
        res["time"] = str(now)
        print("===========data after predict================")
        print(res)

         # send data via socket.io to client
        socketData = {
            "curTemp": temp,
            "conclusion": res["conclusion"],
            "uv": uvid,
            "humid": humid,
            "pressure": pres
        }
        socketio.emit('UpdateData', socketData)

        #Save data to database
        sensorData = SensorData(**res).save()
        return jsonify(sensorData), 201
    except:
        return {"msg": "Fail"}, 400

def predictFutureTemp1():
    start = time.time()
    res = round(prediction.predict_1_hour(), 1)
    end = time.time()
    print('Time taken: {}'.format(end - start))
    
    return str(res)
    

def predictFutureTemp4():
    start = time.time()
    res = round(prediction.predict_1_hour(), 1)
    end = time.time()
    print('Time taken: {}'.format(end - start))

    return str(res)
   
def getChartData():
    res = []
    hour = datetime.datetime.now().hour
    for i in range(0, hour*720, 720):
        obj = SensorData.objects[i]
        record = {
            "hour": obj.time[11:].split(":")[0],
            "temp": obj.temperature
        }
        res.append(record)

    return {"chartData": res}

