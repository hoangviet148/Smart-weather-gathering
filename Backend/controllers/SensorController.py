from flask import request, jsonify
from models.SensorData import SensorData
from ML import conclusion, prediction
import time

def postSensorData():
    try:
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
        y = conclusion.predict(data)
        fields = ["temperature", "humidity", "uv", "pressure", "wdir", "wspd", "conclusion"]
        res = {}
        for k, v in zip(fields, y):
            res[k] = v
        print(res)
        sensorData = SensorData(**res).save()
        return jsonify(sensorData), 201
    except:
        return {"msg": "Fail"}, 400

def getSensorData():
    start = time.time()
    res = str(int(prediction.get_data()))
    end = time.time()
    print('Time taken: {}'.format(end - start))
    return res
   


    