# ai_service.py
from flask import Flask, request, jsonify
from severity_prediction import SeverityPredictor
from hotspot_detection import HotspotDetector
from alert_engine import AlertEngine
import pandas as pd
import os

app = Flask(__name__)

# Initialize components
severity_predictor = SeverityPredictor()
hotspot_detector = HotspotDetector()

@app.route('/predict-severity', methods=['POST'])
def predict_severity():
    data = request.json
    try:
        prediction = severity_predictor.predict(data)
        return jsonify(prediction)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/detect-hotspots', methods=['POST'])
def detect_hotspots():
    data = request.json
    df = pd.DataFrame(data)
    try:
        hotspots = hotspot_detector.detect_hotspots(df)
        return jsonify(hotspots)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/check-alerts', methods=['POST'])
def check_alerts():
    data = request.json
    user_lat = data.get('latitude')
    user_lng = data.get('longitude')
    hotspots = data.get('hotspots')
    weather = data.get('weather')
    
    engine = AlertEngine(hotspots, weather)
    alerts = engine.check_user_location(user_lat, user_lng)
    
    return jsonify({'alerts': alerts})

if __name__ == '__main__':
    # In a real scenario, we would load the model here
    # severity_predictor.load_model()
    app.run(host='0.0.0.0', port=5000)
