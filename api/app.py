from fastapi import FastAPI
import uvicorn
from router import products, scraper, authorization
from database.dbHandler import DBHandler
from config.app_contex import api_title, api_description, api_version, api_docs_url, image_location
import os

# Verify dot env path
env_file_path = os.path.join(os.path.dirname(__file__), '..', '.env')

# Create an instance of the FastAPI class
app = FastAPI(
    title=api_title,
    description=api_description,
    version=api_version,
    docs_url=api_docs_url,      
)

# Generate DBHandler
dbHandler = DBHandler()

#Create tables
dbHandler.create_tables()

os.makedirs(image_location, exist_ok=True)

# Including all routes
app.include_router(products.router)
app.include_router(scraper.router)
app.include_router(authorization.router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
