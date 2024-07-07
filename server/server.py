#will take functions from other files and act as main file
#**download dependencies in a virtual environment**
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
#imported devOps function
from initial_itinerary import developOptions

# Routes

app = Flask(__name__)
CORS(app)

@app.route("/test")
def test():
    return {"test": ["test1","test2","test3"]}

# @app.route("/get-itinerary", methods=["GET"])
# def get_itinerary():
#     data = getOptions()
#     print("DATA RRETRUEND: " + str(data))
#     return jsonify(data)

@app.route("/submit", methods=["POST"]) 
def formSubmit():
    global processed_data
    form_data = request.get_json()

    # Process the form data 
    # input form data -> process (run through ML model) -> processed data (output of ML model)
    # Right now there is no processing, just returning the data

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

@app.route("/results")
def getResults():
    # Fetch results from wherever they are stored: processed_data global
    # Return results as JSON response
    print(jsonify(processed_data))
    return jsonify(processed_data)

@app.route("/processed_data")
def getProcessedData():
    return jsonify(processed_data)


if __name__ == "__main__":
    os.environ['FLASK_ENV'] = 'development'
    app.run(port=8000, debug=True)

