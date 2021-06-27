from .db import db

class SensorData(db.Document):
    temperature = db.FloatField(required=True)
    humidity = db.FloatField(required=True)
    uv = db.FloatField(required=True)
    pressure = db.FloatField(required=True)
    wdir = db.FloatField(required=True)
    wspd = db.FloatField(required=True)
    conclusion = db.StringField(required=True)
    time = db.StringField(required=True)