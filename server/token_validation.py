import jwt
import requests
import json
from flask import request, jsonify


from .constants import COGNITO_JWKS_URL, COGNITO_CLIENT_ID


def get_jwks():
    response = requests.get(COGNITO_JWKS_URL)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch JWKS: {response.status_code}")

    jwks = response.json()    

    return jwks

def validate_token(token):

    jwks = get_jwks()
    if 'keys' not in jwks:
        raise ValueError("JWKS response does not contain 'keys'")
    public_keys = {}
    for key in jwks['keys']:
        kid = key['kid']
        public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
    
    kid = jwt.get_unverified_header(token)['kid']
    key = public_keys[kid]
    return jwt.decode(token, key=key, algorithms=['RS256'], audience=COGNITO_CLIENT_ID)
