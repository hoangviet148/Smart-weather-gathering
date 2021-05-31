from .db import db

class SensorData(db.Document):
    temperature = db.FloatField(required=True)
    humidity = db.FloatField(required=True)
    uv = db.FloatField(required=True)
    pressure = db.FloatField(required=True)