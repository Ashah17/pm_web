#will take functions from other files and act as main file
#**download dependencies in a virtual environment**
from flask import Flask, request, jsonify, redirect, session, url_for, render_template, make_response
from flask_cors import CORS
from flask_session import Session
import os
import requests
from datetime import datetime
#imported devOps function
from .initial_itinerary import developOptions
from .detailed_options import individual_places

# login auth tokens
from .token_validation import validate_token
import jwt
from .constants import COGNITO_AUTH_BASE_URL, COGNITO_CLIENT_ID, COGNITO_REDIRECT_URI, COGNITO_TOKEN_URL, COGNITO_LOGOUT_URL

import logging

#DynamoDB
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Configure Flask session
app.config['SECRET_KEY'] = 'big_bush'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()

# Configure DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
users_table = dynamodb.Table('Users')

# Routes
@app.route("/test")
def test():
    return {"test": ["test1","test2","test3"]}

# @app.route("/get-itinerary", methods=["GET"])
# def get_itinerary():
#     data = getOptions()
#     print("DATA RRETRUEND: " + str(data))
#     return jsonify(data)

@app.route('/login')
def login():
    #logger.debug("Login route hit")
    session.clear()    
    cognito_login_url = (
        f"{COGNITO_AUTH_BASE_URL}"
        f"?response_type=code&client_id={COGNITO_CLIENT_ID}&redirect_uri={COGNITO_REDIRECT_URI}&scope=email openid"
    )
    # logger.debug(f"Redirecting to: {cognito_login_url}")
    return redirect(cognito_login_url)

@app.route('/callback')
def callback():
    # logger.debug("Callback route hit")
    code = request.args.get('code')
    if not code:
        logger.error("No code provided in callback")
        return 'Error: No code provided', 400

    # logger.debug(f"Authorization code received: {code}")
    
    # Exchange the authorization code for tokens
    token_response = requests.post(
        COGNITO_TOKEN_URL,
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data={
            'grant_type': 'authorization_code',
            'client_id': COGNITO_CLIENT_ID,
            'code': code,
            'redirect_uri': COGNITO_REDIRECT_URI,
        }
    )

    if token_response.status_code != 200:
        return 'Failed to fetch tokens', 400

    tokens = token_response.json()
    session['tokens'] = tokens  # Store tokens in the session
    # logger.debug(f"Tokens received: {tokens}")

    # Save user info to DynamoDB
    id_token = tokens['id_token']
    try:
        user_info = validate_token(id_token)
        save_user_info(user_info)
    except jwt.PyJWTError as e:
        # logger.error(f"Token validation error: {e}")
        return str(e), 401

    return redirect('http://localhost:3000/my-account')

@app.route('/logout')
def logout():

    # logger.debug("Logout route hit")
    session.clear()  # Clear any existing session tokens

    # Create the Cognito logout URL
    cognito_logout_url = (
        f"{COGNITO_LOGOUT_URL}"
        f"?client_id={COGNITO_CLIENT_ID}"
        f"&logout_uri=http://localhost:3000/"  # Ensure this matches an allowed logout URL in Cognito
        f"&response_type=code"
    )
    # logger.debug(f"Redirecting to: {cognito_logout_url}")

    # Clear the session cookies
    response = make_response(redirect(cognito_logout_url))
    for cookie in request.cookies:
        response.set_cookie(cookie, '', expires=0)
    
    return response


    # logger.debug("Logout route hit")
    # session.clear() 
    # cognito_logout_url = (
    #     f"{COGNITO_LOGOUT_URL}"
    #     f"?client_id={COGNITO_CLIENT_ID}"
    #     f"&redirect_uri={COGNITO_REDIRECT_URI}"
    #     f"&response_type=code"
    # )
    # logger.debug(f"Redirecting to: {cognito_logout_url}")

    # # Log out from Cognito
    # cognito_response = requests.get(cognito_logout_url)
    # if cognito_response.status_code != 200:
    #     logger.error(f"Failed to log out from Cognito: {cognito_response.status_code} {cognito_response.text}")
    # # Clear the session cookies
    # response = make_response(redirect('http://localhost:3000/'))
    # for cookie in request.cookies:
    #     response.set_cookie(cookie, '', expires=0)
    
    # return response

@app.route("/submit", methods=["POST"]) 
def formSubmit():
    form_data = request.get_json()

    # Process the form data 

    userInfo = []

    location = form_data.get('location', "N/A") + " " + form_data.get('middleInitial', " ") + form_data.get('lastName', "N/A")
    startDate = form_data.get('startDate', "N/A")
    endDate = form_data.get('endDate', "N/A")

    userInfo.append(location)
    userInfo.append(startDate)
    userInfo.append(endDate)

    response_data = {'userInfo': userInfo}

    print(response_data)

    #DO THE WORK HERE WITH THE RESPONSE DATA

    start_date = datetime.strptime(startDate, '%Y-%m-%d')

    end_date = datetime.strptime(endDate, '%Y-%m-%d')

    # Subtract the dates

    # Calculate the duration in days
    duration_days = (end_date - start_date).days

    # Use the developOptions function to get itinerary options
    itineraries = developOptions(location, duration_days)

    # print(itineraries)

    # Prepare the response data
    response_data = {
        'location': location,
        'startDate': startDate,
        'endDate': endDate,
        'durationDays': duration_days,
        'itineraries': itineraries
    }

    return jsonify(response_data), 201


@app.route("/detailed_options", methods=["POST"])
def getDetailedOptions():
    data = request.get_json()
    # selected_itinerary = data.get('')
    selected_option = data.get('selectedOption')
    itineraries = data.get('itineraries')

    if selected_option is None or itineraries is None:
        return jsonify({"error": "Missing data"}), 400 #error handling

    selected_itinerary = itineraries[selected_option]

    # print("HELLOOOOOO")

    # print(selected_itinerary)

    # itinerary properly sent through post request, now call functions on it for detailed options

    listedItinerary = individual_places(selected_itinerary)

    response = {
        'listedItinerary': listedItinerary
    }

    print(listedItinerary)

    return jsonify(response), 201

@app.route('/mapping_details', methods=["POST"])
def generate_map():
    data = request.get_json()
    print(data)

    # l = ['h', 'i']

    response = {
        'mappingDetails': data
    }

    return jsonify(response), 201




# @app.route("/results")
# def getResults():
#     # Fetch results from wherever they are stored: processed_data global
#     # Return results as JSON response
#     print(jsonify(processed_data))
#     return jsonify(processed_data)

# @app.route("/processed_data")
# def getProcessedData():
#     return jsonify(processed_data)





@app.route('/session_info')
def session_info():
    return jsonify(session.get('tokens'))


def save_user_info(user_info):
    # Extract the username from the user_info
    # logger.debug(f"User info to save: {user_info}")

    try:
        #need to investigate if need to update users instead of overwrite each time
        username = user_info.get('cognito:username') or user_info.get('sub')
        user_info['username'] = username
        users_table.put_item(Item=user_info)
        # logger.debug("User info saved to DynamoDB")
        # verify_user_info(username)
    except ClientError as e:
        logger.error(f"Failed to save user info to DynamoDB: {e.response['Error']['Message']}")

@app.route('/user-profile', methods=['GET'])
def user_profile():
    tokens = session.get('tokens')
    if not tokens:
        return jsonify({"error": "User not authenticated"}), 401

    id_token = tokens['id_token']
    try:
        user_info = validate_token(id_token)
        username = user_info.get('cognito:username')
        response = users_table.get_item(Key={'username': username})
        if 'Item' in response:
            # logging.debug("Sent to frontend")
            return jsonify(response['Item'])
        else:
            return jsonify({"error": "User not found"}), 404
    except jwt.PyJWTError as e:
        logger.error(f"Token validation error: {e}")
        return jsonify({"error": str(e)}), 401
    except ClientError as e:
        logger.error(f"DynamoDB error: {e.response['Error']['Message']}")
        return jsonify({"error": e.response['Error']['Message']}), 500
'''
def verify_user_info(username):
    try:
        response = users_table.get_item(Key={'username': username})
        if 'Item' in response:
            logger.debug(f"User info verified: {response['Item']}")
        else:
            logger.debug(f"User info not found for username: {username}")
    except ClientError as e:
        logger.error(f"Failed to verify user info in DynamoDB: {e.response['Error']['Message']}")
'''

if __name__ == "__main__":
    os.environ['FLASK_ENV'] = 'development'
    app.run(port=8000, debug=True)

