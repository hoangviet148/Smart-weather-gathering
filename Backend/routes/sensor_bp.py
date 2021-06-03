from flask import Blueprint
from controllers.SensorController import postSensorData, getSensorData

sensor_bp = Blueprint('sensor_bp', __name__)

sensor_bp.route('/postSensorData', methods=['POST'])(postSensorData)
sensor_bp.route('/getSensorData', methods=['GET'])(getSensorData)
