from flask import request, jsonify
from models.SensorData import SensorData

def postSensorData():
    try:
        body = request.get_json()
        # **body unpacks the body dictionary into the Movie object as named parameters
        # For example if body = {"temp": 20, "humi": 85},
        # Then Movie(**body) is the same as SensorData(temp=20, humi=85)
        sensorData = SensorData(**body).save()
        return jsonify(sensorData), 201
    except:
        print("An error occour !")


    