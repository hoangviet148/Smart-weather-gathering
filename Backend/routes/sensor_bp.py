from flask import Blueprint
from controllers.SensorController import postSensorData, predictFutureTemp, getChartData

sensor_bp = Blueprint('sensor_bp', __name__)

sensor_bp.route('/postSensorData', methods=['POST'])(postSensorData)
sensor_bp.route('/getFutureTemp', methods=['GET'])(predictFutureTemp)
sensor_bp.route('/getChartData', methods=['GET'])(getChartData)

