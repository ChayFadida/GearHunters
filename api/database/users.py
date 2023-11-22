from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from config.logger_config import log

usersBase = declarative_base()

class User(usersBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())

    def __init__(self, username, password, role, status):
        self.username = username
        self.password = password
        self.role = role
        self.status = status

class UserHandler:
    def __init__(self, session):
        self.session = session

    def create_user(self, username, password, role, status):
        log.info(f'Creating user {username} as {role}')
        user = User(username=username, password=password, role=role, status=status)
        self.session.add(user)
        self.session.commit()
        return user

    def get_user_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()

    def get_user_by_id(self, user_id):
        return self.session.query(User).get(user_id)

    def update_user_status(self, user, new_status):
        log.info(f'Updating user {user} to status {new_status}')
        user.status = new_status
        self.session.commit()
