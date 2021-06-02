from flask import Flask,redirect,url_for,request
from flask_cors import CORS
from lightgbm import LGBMClassifier
from sklearn.preprocessing import LabelEncoder
from dateutil import rrule
from datetime import datetime
import requests
import json
import pickle

app=Flask(__name__)
CORS(app)

def get_wind_info():
    today = datetime.now()
    BASE_URL = "https://api.weather.com/v1/location/VVNB:9:VN/observations/historical.json?apiKey=e1f10a1e78da46f5b10a1e78da96f525&units=e&startDate="

    month = str(today.month)
    day = str(today.day)
    if len(month) == 1:
        month = '0' + month
    if len(day) == 1:
        day = '0' + day
    url = BASE_URL + str(today.year) + month + day

    page = requests.get(url)
    content = json.loads(page.content)
    obs = content['observations'][-1]
    data = [obs['temp'], obs['rh'], obs['pressure'], obs['uv_index'], obs['wx_phrase'], obs['wdir'], obs['wspd']]
    print(data)
    return data[-2], data[-1]

# Load model ML
filename = "weather classifier.pkl" 
with open(filename, 'rb') as file:  
    model = pickle.load(file) 

# Load encoder
filename = "weather encoder.pkl" 
with open(filename, 'rb') as file:  
    encoder = pickle.load(file) 

@app.route('/weather_conclusion', methods=['POST'])
def sha_order():
    data = request.get_json()

    temp = data['temperature']
    humid = data['humidity']
    uvid = data['uv index']
    pres = data['pressure']
    wdir, wspd = get_wind_info()
    X = [[temp, humid, pres, uvid, wdir, wspd]]
    y = model.predict(X)
    return encoder.inverse_transform(y)[0]

if __name__=='__main__':
    app.run(host='localhost', port=3000)