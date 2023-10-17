from fastapi import FastAPI
import uvicorn
from router import products, scraper, authorization
from database.dbHandler import DBHandler
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer

# Verify dot env path
env_file_path = os.path.join(os.path.dirname(__file__), '..', '.env')

# Load environment variables from the .env file
load_dotenv(dotenv_path=env_file_path)

# Create an instance of the FastAPI class
app = FastAPI(
    title="Your API Title",
    description="Product API",
    version="1.0.0",
    docs_url="/docs",      
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
