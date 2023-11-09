from flask import Flask, request, jsonify, render_template
import joblib
import logging
from logging.handlers import RotatingFileHandler
import pandas as pd

# Initialize Flask application
app = Flask(__name__)

# Set up logging
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

# Load the trained model from file
model = joblib.load('intrusion_detection_model.joblib')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    app.logger.info('Prediction request received')
    try:
        # Get JSON data from the POST request
        data = request.get_json(force=True)
        
        # Transform the JSON data into a DataFrame
        features = model.feature_names_in_
        data_df = pd.DataFrame(data, columns=features)
        
        # Predict using the model
        predictions = model.predict(data_df)
        
        # Return the predictions as JSON
        return jsonify(predictions.tolist())
    except Exception as e:
        # Log the error
        app.logger.error('Error during prediction: %s', str(e))
        # Respond with an error message
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
