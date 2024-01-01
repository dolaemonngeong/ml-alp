from flask import Flask, render_template, Response, request
import pickle
import numpy as np
from gevent.pywsgi import WSGIServer

# source: https://www.analyticsvidhya.com/blog/2020/09/web-application/
# Load Machine Learning model
model = pickle.load(open('model.pkl', 'rb')) 

# Create application
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods =['POST'])
def predict():
    
    # Put all form entries values in a list 
    features = [float(i) for i in request.form.values()]

    # Convert features variable to array
    array_features = [np.array(features)]

    # Predict features
    prediction = model.predict(array_features)
    
    output = prediction
    

    # Check the output values & return the result with html tag based on the value
    if output == 1:
        return render_template('index.html', 
                               result = 'You have no sleeping disorders.')
    elif output == 2:
        return render_template('index.html', 
                               result = 'You have Sleep Apnea')
    elif output == 3:
        return render_template('index.html', 
                               result = 'You have Insomnia')

# app.run(debug=True)

# if __name__ == "__main__":
#     from waitress import serve
#     serve(app, host="0.0.0.0", port=8080)

if __name__ == '__main__':
    http_server = WSGIServer(("127.0.0.1", 8080), app)
    http_server.serve_forever()
    