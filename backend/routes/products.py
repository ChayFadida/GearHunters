from flask import Blueprint, request, jsonify
import requests
import os
from utils.authentication_with_api import login_to_api
from config.app_contex import API_PRODUCTS_URL
import json
# Create a Flask Blueprint for authentication routes
products_bp = Blueprint('products', __name__)

# Define a route for fetching a product using a valid token
@products_bp.route("/fetch_product")
def fetch_product():
    login_response = login_to_api()
    
    if login_response and login_response[1] == 200:  # Check if the status code is 200 (OK)
        token = login_response[0].json['access_token']
        
        if token:
            # Make a request to the FastAPI product endpoint with the valid token
            response = requests.get(f"{API_PRODUCTS_URL}", headers={"Authorization": f"Bearer {token}"})
            
            if response.status_code == 200:
                response_data = response.content.decode('utf-8', errors='ignore')
                product_data = json.loads(response_data)
                response = jsonify(product_data)
                return jsonify(product_data)
            else:
                error_data = response.json()
                return jsonify({"error": error_data}), response.status_code
        else:
            return jsonify({"error": "Unable to obtain a valid token."}), 401
    else:
        return login_response[0]
