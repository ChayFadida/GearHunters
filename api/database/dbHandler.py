from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.product import productBase
from database.users import usersBase
import os

class DBHandler:
    def __init__(self):
        # Replace 'your_database_url' with your actual database URL
        db_url = os.getenv('DATABASE_URL')
        self.engine = create_engine(db_url)

        # Create a session to interact with the database
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_tables(self):
        productBase.metadata.create_all(self.engine)
        usersBase.metadata.create_all(self.engine)
