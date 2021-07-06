from flask import Flask
from flask_cors import CORS

from socketIO.init import createSocket, socketio
from models.db import initialize_db
from routes.sensor_bp import sensor_bp

app = Flask(__name__)
CORS(app)

createSocket(app)
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/weather',
    'port': 27017
}

initialize_db(app)

@socketio.on('connect', namespace='/')
def connect():
    print('A client connected!')

app.register_blueprint(sensor_bp, url_prefix='/api')

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=3000)
