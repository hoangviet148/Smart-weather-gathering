from flask import Blueprint
from controllers.SensorController import postSensorData, predictFutureTemp1, predictFutureTemp4, getChartData

sensor_bp = Blueprint('sensor_bp', __name__)

sensor_bp.route('/postSensorData', methods=['POST'])(postSensorData)
sensor_bp.route('/getFutureTemp1', methods=['GET'])(predictFutureTemp1)
sensor_bp.route('/getFutureTemp4', methods=['GET'])(predictFutureTemp4)
sensor_bp.route('/getChartData', methods=['GET'])(getChartData)

