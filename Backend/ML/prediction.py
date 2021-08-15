from models.SensorData import SensorData
import pandas as pd
import numpy as np
import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"    
import tensorflow.keras as keras

inputs = keras.layers.Input(shape=(120, 4))
lstm_out = keras.layers.LSTM(32)(inputs)
outputs = keras.layers.Dense(1)(lstm_out)

model_1 = keras.Model(inputs=inputs, outputs=outputs)
model_1.compile()
model_1.summary()

inputs = keras.layers.Input(shape=(30, 4))
lstm_out = keras.layers.LSTM(32)(inputs)
outputs = keras.layers.Dense(1)(lstm_out)

model_4 = keras.Model(inputs=inputs, outputs=outputs)
model_4.compile()
model_4.summary()

model_1.load_weights("ML\model_1_hour.h5")
model_4.load_weights("ML\model_4_hour.h5")

def normalize(data):
    data_mean = data.mean(axis=0) 
    data_std = data.std(axis=0) + 0.000001
    return (data - data_mean) / data_std, data_mean[0], data_std[0]

def get_data(model, step):
    data = []
    i = 0
    for obj in SensorData.objects[len(SensorData.objects) - 240:]:
        if i % step == 0:
            data.append([obj['temperature'], obj['humidity'], obj['pressure'], obj['uv']])
        i += 1
    df = pd.DataFrame.from_records(data)
    df = df.loc[ : , df.columns != 'time']
    df, mean, std = normalize(df)
    
    X = np.expand_dims(df, axis=0)
    y = model.predict(X)
    res = y[0][0] * std + mean
    return res

def predict_1_hour():
    return get_data(model_1, 2)

def predict_4_hour():
    return get_data(model_4, 8)