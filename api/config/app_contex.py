import os

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
TOKEN_ALGORITHM = "HS256"
DB_URL = os.getenv('DATABASE_URL')
api_title = "Gearhunter API"
api_description="Gearhunter official API"
api_version="1.0.0"
api_docs_url="/docs"
image_location = "/Images"