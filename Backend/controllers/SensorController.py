from flask import request, jsonify
from models.SensorData import SensorData
from ML import conclusion

def postSensorData():
    try:
        getData()
        data = request.get_json()
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
        
        sensorData = SensorData(**res).save()
        return jsonify(sensorData), 201
    except:
        print("An error occur !")
        return {"msg": "Fail"}, 400

def getData():
    for data in SensorData.objects:
        print(data["conclusion"])


    