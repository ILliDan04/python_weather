from flask import Flask, request, abort
from dotenv import load_dotenv
import os
import requests
import datetime
import json

load_dotenv()

API_KEY = os.getenv("API_KEY")
URL = os.getenv("URL")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
RAPID_API_HOST = os.getenv("RAPID_API_HOST")

headers = {
	"X-RapidAPI-Key": RAPID_API_KEY,
	"X-RapidAPI-Host": RAPID_API_HOST
}

app = Flask(__name__)

@app.route("/", methods=['GET'])
def getWeather():
    args = request.args

    req_access_key = args.get("access_key")
    if req_access_key != API_KEY:
        abort(401, description="Unauthorized")
        return

    location = args.get("location")
    requester_name = args.get("requester_name")

    querystring = {"location": location, "format": "json", "u": "f"}

    api_response = requests.request("GET", URL, headers=headers, params=querystring)
    client_response = {
        'weather': json.loads(api_response.text),
        'requester_name': requester_name,
        'timestamp': datetime.datetime.now().isoformat(),
        'location': location
    }
    
    return client_response

app.run(host='0.0.0.0')
