from flask import Flask, jsonify, request
from web3 import Web3
import joblib

app = Flask(__name__)
w3 = Web3(Web3.HTTPProvider('https://core-node.example'))

# Load the trained model
model = joblib.load('models/token_predictor.pkl')

# Smart contract setup
contract_abi = [...]  # ABI from deployed TokenTracker contract
contract_address = '0x...'  # Address of deployed TokenTracker contract
token_tracker = w3.eth.contract(address=contract_address, abi=contract_abi)

@app.route('/api/tokens', methods=['GET'])
def get_tokens():
    tokens = token_tracker.functions.getRegisteredTokens().call()
    token_list = []
    for token_address in tokens:
        token_info = token_tracker.functions.getTokenInfo(token_address).call()
        token_list.append({
            'address': token_address,
            'launchTime': token_info[1],
            'totalSupply': token_info[2],
            'liquidity': token_info[3],
            'holderCount': token_info[4]
        })
    return jsonify(token_list)

@app.route('/api/tokens/<address>', methods=['GET'])
def get_token(address):
    token_info = token_tracker.functions.getTokenInfo(address).call()
    return jsonify({
        'address': address,
        'launchTime': token_info[1],
        'totalSupply': token_info[2],
        'liquidity': token_info[3],
        'holderCount': token_info[4]
    })

@app.route('/api/tokens/metrics', methods=['GET'])
def get_metrics():
    # Implement filtering logic
    return jsonify({
        'minLiquidity': 0,
        'maxLiquidity': 1000000,
        'minHolderCount': 0,
        'maxHolderCount': 10000
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    prediction = model.predict([[
        data['liquidity'],
        data['holderCount'],
        data['totalSupply'],
        data['launchTime']
    ]])
    return jsonify({'prediction': int(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True)