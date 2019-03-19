from flask import Flask
from flask import request
from flask import json
from sklearn.externals import joblib
from keras import backend
from keras import models
from keras.utils.np_utils import to_categorical
import numpy as np
import os
app = Flask(__name__)

dict = {5:0, 10:1, 30:2, 60:3, 120:4, 240:5}

predict_models={}
for model_name in os.listdir('models'):
	model = models.load_model('models/' + model_name);
	model._make_predict_function()
	predict_models[model_name[5:-3]] = model

scalers={}
for scaler_name in os.listdir('scalers'):
	scalers[scaler_name[8:-5]] = joblib.load('scalers/' + scaler_name)

@app.route('/api/predict', methods=['GET'])
def predict():
	if request.method == 'GET':
		x = request.args.get('x', type=float)
		z = request.args.get('z', type=float)
		id = request.args.get('user_id', type=str)
		time = request.args.get('time', type=float)
		timeframe = request.args.get('timeframe', type=float)
		
		features = scalers[id].transform([[time,x,z]])
		timeframe_cat = to_categorical(np.vectorize(dict.get)([timeframe]), 6)
		prediction = predict_models[id].predict([features, timeframe_cat])

		prediction = [np.append(0, prediction[0])]
		prediction_unscaled = scalers[id].inverse_transform(prediction)

		x_prediction, z_prediction = np.round(prediction_unscaled[0][1:], 2)
		
		return json.jsonify(x_prediction=x_prediction, z_prediction=z_prediction)
	return json.jsonify('')
