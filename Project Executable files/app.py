from flask import Flask, render_template, request, redirect
import joblib

app = Flask(__name__)

model = joblib.load('flask\model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/submit_values', methods=['POST'])
def submit_values():
    try:
        # Retrieve data from the form
        step = float(request.form['step'])
        type = float(request.form['type'])
        amount = float(request.form['amount'])
        nameOrig = float(request.form['nameOrig'])
        oldbalanceOrg = float(request.form['oldbalanceOrg'])
        newbalanceOrig = float(request.form['newbalanceOrig'])
        nameDest = float(request.form['nameDest'])
        oldbalanceDest = float(request.form['oldbalanceDest'])
        newbalanceDest = float(request.form['newbalanceDest'])
        isFraud = float(request.form['isFraud'])

        # Perform prediction using the loaded model
        input_values = [[step, type, amount, nameOrig, oldbalanceOrg, newbalanceOrig, nameDest, oldbalanceDest, newbalanceDest, isFraud]]
        prediction = model.predict(input_values)[0]

        # Determine the prediction result
        if prediction == 1:
            prediction_result = "Fraudulent Transaction &#9888;"  # Add caution symbol for fraudulent transaction
        else:
            prediction_result = "Non-Fraudulent Transaction"

        # Pass the prediction result to the submit page
        return render_template('submit.html', prediction_result=prediction_result)

    except KeyError:
        # If any of the form fields are missing, return a caution symbol with an error message
        return render_template('submit.html', prediction_result='&#9888; Missing form field(s)')

if __name__ == '__main__':
    app.run(debug=True)

