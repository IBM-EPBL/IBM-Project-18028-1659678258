from flask import Flask, render_template, request
import numpy as np
import pickle


app = Flask(__name__)
model = pickle.load(open('CKD.pkl', 'rb'))

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

        return render_template('result.html', prediction=prediction)

print(predict)

if __name__ == "__main__":
    app.run(debug=True)

