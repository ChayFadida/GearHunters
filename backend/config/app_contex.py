import os

API_BASE_URL = f"{os.getenv('API_BASE_URL')}"
API_AUTHENTICATION_URL = f"{API_BASE_URL}/authentication"
API_PRODUCTS_URL = F"{API_BASE_URL}/products"
API_USER = os.getenv("API_USER")
API_PASSWORD = os.getenv("API_PASSWORD")
