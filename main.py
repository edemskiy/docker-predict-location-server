from flask import Flask
from flask import request
from flask import json
from sklearn.externals import joblib
from keras import backend
from keras import models
from keras.utils.np_utils import to_categorical
from keras.utils.data_utils import get_file
import numpy as np

import utils
app = Flask(__name__)

dict = {5:0, 10:1, 30:2, 60:3, 120:4, 240:5}

predict_models={}
scalers={}

models_urls = utils.get_git_folder_files(utils.models_folder_url)
scalers_urls = utils.get_git_folder_files(utils.scalers_models_folder_url)

for url in models_urls:
	model_name=url[url.rfind('/') + 1:-9]
	model_path = get_file(model_name, url)
	model = models.load_model(model_path);
	model._make_predict_function()
	predict_models[model_name[5:-3]] = model

for url in scalers_urls:
	scaler_name=url[url.rfind('/') + 1:-9]
	scaler_path = get_file(scaler_name, url)
	scalers[scaler_name[8:-5]] = joblib.load(scaler_path)


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