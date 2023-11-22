from flask import request, jsonify
from config.app_contex import API_AUTHENTICATION_URL, API_USER, API_PASSWORD
import requests
import os

# Initialize the access token as None initially
access_token = None

# Function to check if a given token is valid by making an API request
def is_token_valid(token):
    response = requests.get(f"{API_AUTHENTICATION_URL}/verify_token", headers={"Authorization": f"Bearer {token}"})
    return response.status_code == 200

# Function to retrieve an access token from the API
def get_token(username, password):
    # If the token is expired or invalid, get a new one
    data = {
        "username": username,
        "password": password
    }
    try:
        response = requests.post(f"{API_AUTHENTICATION_URL}/login", data=data)
    except Exception as e:
        print("API is not active")
        
    if response.status_code == 200:
        access_token = response.json()["access_token"]
        return access_token
    else:
        return None

# Function to get a valid access token, either by reusing the existing token or obtaining a new one
def get_valid_access_token(username, password):
    global access_token  # Use the global keyword to modify a module-level variable
    if not access_token:
        # Fetch a new access token if it doesn't exist
        access_token = get_token(username, password)

    # Check if the current access token is valid
    response = requests.get(f"{API_AUTHENTICATION_URL}/verify_token", headers={"Authorization": f"Bearer {access_token}"})
    if response.status_code == 200:
        return access_token
    else:
        # If the token is expired or invalid, get a new one
        get_token(username, password)

def login_to_api():
    username = API_USER
    password = API_PASSWORD

    if username is None or password is None:
        # Return an error response if username or password is missing
        return jsonify({"message": "Username and password are required"}), 400

    # Get a valid access token or fetch a new one
    valid_token = get_valid_access_token(username, password)

    if valid_token:
        # Return a success response with the access token
        return jsonify({"message": "Valid token, start integrating with the API", "access_token": valid_token}), 200
    else:
        # Return an error response if the token retrieval fails
        return jsonify({"message": "Failed to obtain a valid token"}), 401
