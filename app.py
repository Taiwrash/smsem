from flask import Flask, request, jsonify
import numpy as np
import pickle
import lightgbm

app = Flask(__name__)

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()
classifier = data['model']
vectorizer = data['vectorizer']

@app.route('/predict', methods=['POST'])
def predict():
    message = request.json.get('message', '')
    if not message:
        return jsonify({'error': 'Please provide a message'}), 400

    X = np.array([message])
    X_str = np.vectorize(str)(X)
    transformed_data = vectorizer.transform(X_str)

    prediction = classifier.predict_proba(transformed_data)[:, 1]
    result = "spam" if prediction >= 0.3 else "not spam"
    
    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(debug=True)  