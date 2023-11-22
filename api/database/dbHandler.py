from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.product import productBase
from database.users import usersBase
from config.logger_config import log
from config.app_contex import DB_URL
import os

class DBHandler:
    def __init__(self):
        db_url = DB_URL
        self.engine = create_engine(db_url)

        # Create a session to interact with the database
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_tables(self):
        log.info("Creating tables")
        productBase.metadata.create_all(self.engine)
        usersBase.metadata.create_all(self.engine)
