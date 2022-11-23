from flask import Flask, render_template, request
import numpy as np
import pickle

import requests

import json

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "iFoa__4xAdx6K2wO7l5ldK_A7sK8jRh2P1PcnTAx-7VZ"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app = Flask(__name__)

@app.route('/',methods=['GET'])
def Home():
    return render_template('Home.html')

@app.route('/index',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        rbc = float(request.form['rbc'])
        pc = float(request.form['pc'])
        bgr = float(request.form['bgr'])
        bu = float(request.form['bu'])
        pe = float(request.form['pe'])
        ane = float(request.form['ane'])
        dm = float(request.form['dm'])
        cad = float(request.form['cad'])

        values = np.array([[rbc, pc, bgr,bu, pe, ane, dm, cad]])
        print(values)
        prediction = model.predict(values)

        # NOTE: manually define and pass the array(s) of values to be scored in the next line
#payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}
payload_scoring = {"input_data": [{"field": ['red_blood_cells','pus_cell','blood glucose random','blood_urea','pedal_edema','anemia','diabetesmellitus','coronary_artery_disease'],
                                   "values": [1,1,87,38,0,0,1,0]}]}
response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/dec783ca-1e1b-43d7-80d6-ad75861bf265/predictions?version=2022-11-20', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
print(response_scoring.json())
predictions = response_scoring.json()
prediction = ["predictions"][0]["values"][0][0]
print(prediction)

        return render_template('result.html', prediction=prediction)


if __name__ == "__main__":
    app.run(debug=True)

