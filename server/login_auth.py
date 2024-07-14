import requests
from flask import request, jsonify

import jwt
from jwt import PyJWTError

from server import app


@app.route('/callback')
def callback():
    auth_code = request.args.get('code')
    if not auth_code:
        return jsonify({'error': 'No code provided'}), 400

    # Define your Cognito Token Endpoint
    token_url = 'https://planmaster.auth.us-east-2.amazoncognito.com/oauth2/token'

    # Create a dictionary of the post data
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': '7geo27n56pbmbo217lq9gggfqb',
        'code': auth_code,
        'redirect_uri': 'http://localhost:8000/callback'
    }
    # Headers must include content type and can include client authentication
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # Use client secret if you have confidential client
    response = requests.post(token_url, data=token_data, headers=headers, auth=('7geo27n56pbmbo217lq9gggfqb'))
    
    tokens = response.json()
    return jsonify(tokens)

def decode_jwt(token):
    try:
        # Decode token; you might want to add more options like verify_exp to check expiration
        return jwt.decode(token, options={"verify_signature": False})
    except PyJWTError as e:
        return {'error': str(e)}

@app.route('/token_info')
def token_info():
    # Assuming the token is sent in the Authorization header
    token = request.headers.get('Authorization').split(' ')[1]  # Assumes "Bearer <token>"
    decoded_token = decode_jwt(token)
    return jsonify(decoded_token)