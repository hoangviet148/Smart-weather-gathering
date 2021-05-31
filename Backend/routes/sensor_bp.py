from flask import Blueprint

from controllers.SensorController import postSensorData

sensor_bp = Blueprint('sensor_bp', __name__)

sensor_bp.route('/postSensorData', methods=['POST'])(postSensorData)
