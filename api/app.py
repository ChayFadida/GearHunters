from fastapi import FastAPI
import uvicorn
from router import products, scraper, authorization
from database.dbHandler import DBHandler
from config.app_contex import api_title, api_description, api_version, api_docs_url
import os

# Verify dot env path
env_file_path = os.path.join(os.path.dirname(__file__), '..', '.env')

# Load environment variables from the .env file
# load_dotenv(dotenv_path=env_file_path)

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

# Including all routes
app.include_router(products.router)
app.include_router(scraper.router)
app.include_router(authorization.router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
