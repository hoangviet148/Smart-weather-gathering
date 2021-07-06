from models.SensorData import SensorData
import pandas as pd
import numpy as np
import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"    
import tensorflow.keras as keras

inputs = keras.layers.Input(shape=(120, 4))
lstm_out = keras.layers.LSTM(32)(inputs)
outputs = keras.layers.Dense(1)(lstm_out)

model = keras.Model(inputs=inputs, outputs=outputs)
model.compile()
model.summary()

model.load_weights("ML\model_checkpoint_v2.h5")

def normalize(data):
    data_mean = data.mean(axis=0)
    data_std = data.std(axis=0)
    print(data, data_mean, data_std)
    return (data - data_mean) / data_std, data_mean[0], data_std[0]

def get_data():
    data = []
    i = 0
    for obj in SensorData.objects[len(SensorData.objects) - 240:]:
        if i % 2 == 0:
            data.append([obj['temperature'], obj['humidity'], obj['pressure'], obj['uv']])
        i += 1
    df = pd.DataFrame.from_records(data)
    print(df.head())
    print("check1")
    df, mean, std = normalize(df)
    
    X = np.expand_dims(df, axis=0)
    y = model.predict(X)
    res = y[0][0] * std + mean
    return res