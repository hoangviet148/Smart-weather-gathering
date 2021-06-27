from flask import request, jsonify
from models.SensorData import SensorData
from ML import conclusion, prediction
from flask_socketio import SocketIO
import time
import json
import datetime

# socketio = SocketIO(app, engineio_logger=True)

def postSensorData():
    try:
        # get data from sensor
        now = datetime.datetime.now()
        data = request.get_json()
        print("===========================")
        print(data)
        # **body unpacks the body dictionary into the Movie object as named parameters
        # For example if body = {"temp": 20, "humi": 85},
        # Then SensorData(**body) is the same as SensorData(temp=20, humi=85)
        # sensorData = SensorData(**body).save()
        temp = data['temperature']
        humid = data['humidity']
        uvid = data['uv']
        pres = data['pressure']
        data = [temp, humid, pres, uvid]

        # send data via socket.io to client
        socketData = {
            "temp": temp,
            "humid": humid,
            "uvid": uvid
        }

        # make conclusion
        y = conclusion.predict(data)
        fields = ["temperature", "humidity", "uv", "pressure", "wdir", "wspd", "conclusion"]
        res = {}
        for k, v in zip(fields, y):
            res[k] = v
        res["time"] = str(now.hour)
        print(res)
        sensorData = SensorData(**res).save()
        return jsonify(sensorData), 201
    except:
        return {"msg": "Fail"}, 400

def predictFutureTemp():
    start = time.time()
    res = str(int(prediction.get_data()))
    end = time.time()
    print('Time taken: {}'.format(end - start))
    return res
   
def getChartData():
    result = {}
    i = 0
    for data in SensorData.objects:
        result[i] = data.temperature
        i = i + 1
    return result


