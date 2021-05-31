from flask import Flask
from flask_cors import CORS

from models.db import initialize_db
from routes.sensor_bp import sensor_bp

app = Flask(__name__)
CORS(app)
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/weather',
    'port': 27017
}

initialize_db(app)

app.register_blueprint(sensor_bp, url_prefix='/api')

if __name__ == '__main__':
    app.debug = True
    app.run(host="localhost", port=3000)