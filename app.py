from flask import Flask, request, jsonify, send_from_directory
import os
import warnings
import joblib
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'health_system_v1.pkl')

app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')

model_package = joblib.load(MODEL_PATH)
health_model = model_package['health_model']
stress_model = model_package['stress_model']
scaler_health = model_package['scaler_health']
scaler_stress = model_package['scaler_stress']
le_activity = model_package['le_activity']
le_health = model_package['le_health']

VALID_ACTIVITIES = set(le_activity.classes_)


def encode_activity(activity_value):
    if activity_value not in VALID_ACTIVITIES:
        raise ValueError(f"Invalid activity_level '{activity_value}'. Valid values: {', '.join(VALID_ACTIVITIES)}")
    return int(le_activity.transform([activity_value])[0])


def get_confidence_label(score):
    if score >= 0.80:
        return 'High'
    if score >= 0.65:
        return 'Medium'
    return 'Low'


def predict_stress(features):
    X = np.array([
        features['heart_rate_BPM'],
        features['blood_oxygen_level'],
        features['step_count'],
        features['sleep_duration_hr'],
        encode_activity(features['activity_level']),
        features['health_score'],
    ], dtype=float).reshape(1, -1)
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', message='X does not have valid feature names')
        X_scaled = scaler_stress.transform(X)
    stress_value = int(stress_model.predict(X_scaled)[0])
    probability = float(max(stress_model.predict_proba(X_scaled)[0])) if hasattr(stress_model, 'predict_proba') else 1.0
    return stress_value, probability


def predict_health(features):
    X = np.array([
        features['heart_rate_BPM'],
        features['blood_oxygen_level'],
        features['step_count'],
        features['sleep_duration_hr'],
        encode_activity(features['activity_level']),
        features['stress_level'],
        features['health_score'],
    ], dtype=float).reshape(1, -1)
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', message='X does not have valid feature names')
        X_scaled = scaler_health.transform(X)
    label_index = health_model.predict(X_scaled)[0]
    health_category = str(le_health.inverse_transform([label_index])[0])
    probability = float(max(health_model.predict_proba(X_scaled)[0])) if hasattr(health_model, 'predict_proba') else 1.0
    return health_category, probability


@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')


@app.route('/predict', methods=['POST'])
def predict():
    payload = request.get_json(force=True)
    required = ['heart_rate_BPM', 'blood_oxygen_level', 'step_count', 'sleep_duration_hr', 'activity_level', 'health_score', 'model']
    missing = [key for key in required if key not in payload or payload[key] == '']
    if missing:
        return jsonify({'error': 'Missing required fields', 'missing': missing}), 400

    try:
        features = {
            'heart_rate_BPM': float(payload['heart_rate_BPM']),
            'blood_oxygen_level': float(payload['blood_oxygen_level']),
            'step_count': float(payload['step_count']),
            'sleep_duration_hr': float(payload['sleep_duration_hr']),
            'activity_level': str(payload['activity_level']),
            'health_score': float(payload['health_score']),
        }

        model_choice = str(payload['model'])
        stress_source = 'Provided'
        if model_choice == 'stress' or payload.get('stress_level') in [None, '', []]:
            stress_value, stress_prob = predict_stress(features)
            stress_source = 'Estimated'
        else:
            stress_value = int(float(payload['stress_level']))
            stress_prob = None

        features['stress_level'] = stress_value
        health_category, health_prob = predict_health(features)
        confidence = get_confidence_label(health_prob)

        return jsonify({
            'health_category': health_category,
            'health_confidence': health_prob,
            'confidence_label': confidence,
            'stress_level': stress_value,
            'stress_source': stress_source,
            'model_used': 'stress_chain' if stress_source == 'Estimated' else 'health_model',
        })

    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400
    except Exception as exc:
        return jsonify({'error': 'Prediction error', 'details': str(exc)}), 500


if __name__ == '__main__':
    app.run(debug=True)
