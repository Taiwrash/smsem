from flask import Flask, request, jsonify
import numpy as np
import pickle
import lightgbm
from dotenv import load_dotenv
import os
from web3 import Web3

load_dotenv()

app = Flask(__name__)

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()
classifier = data['model']
vectorizer = data['vectorizer']

w3 = Web3(Web3.HTTPProvider(os.getenv('WEB3_PROVIDER_URI')))
contract = w3.eth.contract(address=os.getenv('CONTRACT_ADDRESS'), abi=os.getenv('ABI'))

@app.route('/predict', methods=['POST'])
def predict():
    message = request.json.get('message', '')
    if not message:
        return jsonify({'error': 'Please provide a message'}), 400

    X = np.array([message])
    X_str = np.vectorize(str)(X)
    transformed_data = vectorizer.transform(X_str)

    account = w3.eth.account.from_key(os.getenv('PRIVATE_KEY'))
    w3.eth.default_account = account.address

    prediction = classifier.predict_proba(transformed_data)[:, 1]
    result = "spam" if prediction >= 0.3 else "not spam"

    result_to_blockchain = f'{{"isFraud": {result}}}'

    nonce = w3.eth.get_transaction_count(w3.eth.default_account)
    tx = contract.functions.addTransaction(result_to_blockchain).build_transaction({
            'chainId': 11155111,
            'gas': 2000000,
            'gasPrice': w3.to_wei('50', 'gwei'),
            'nonce': nonce,
        })
    
    signed_tx = w3.eth.account.sign_transaction(tx, os.getenv('PRIVATE_KEY'))
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    tx_hash_hex = w3.to_hex(tx_hash)
    
    return jsonify({'prediction': result, 'tx_hash': tx_hash_hex})

if __name__ == '__main__':
    app.run(debug=True)  