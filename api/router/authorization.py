# Import required modules and dependencies
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database.dbHandler import DBHandler
from database.users import UserHandler
from sqlalchemy.orm import Session
from pydantic import BaseModel
from config.logger_config import log
from config.app_contex import TOKEN_ALGORITHM, JWT_SECRET_KEY
import jwt
import datetime
import os
import bcrypt

preflix = "/authentication"

# Define a FastAPI router
router = APIRouter(prefix=preflix)

# Token request form used for user login
class TokenRequest(BaseModel):
    username: str
    password: str

# Token response model returned after successful login
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Create an OAuth2 password bearer scheme for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{preflix}/login")

# Function to get a database session
def get_db(request: Request):
    log.debug("Get database session")
    db = DBHandler()
    session = db.session
    try:
        yield session
    finally:
        session.close()

# Function to verify and decode tokens
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[TOKEN_ALGORITHM])
        return payload['data']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate token", headers={"WWW-Authenticate": "Bearer"})

# Function to check if the user is an administrator
def is_admin(current_user: dict = Depends(verify_token)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only administrators can access this endpoint")
    return current_user

# Function to generate access tokens
def create_access_token(data: dict):
    log.debug("Creating access token")
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {"data": data, "exp": expiration}
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=TOKEN_ALGORITHM)
    return token

# Define a route for user registration
@router.post("/register", summary="User Registration Endpoint", tags=["User"], response_model=dict)
async def register_user(username: str, password: str, role: str, db: Session = Depends(get_db)):
    log.info(f'{username} registered as {role}')
    user_handler = UserHandler(db)

    # Check if the user already exists
    if user_handler.get_user_by_username(username):
        log.warning(f'User {username} is already exists')
        raise HTTPException(status_code=400, detail="User already exists")

    # Ensure the provided role is valid
    valid_roles = ["user", "admin", "developer"]
    if role not in valid_roles:
        log.warning(f'Please choose one of the following roles {valid_roles}')
        raise HTTPException(status_code=400, detail="Invalid role. Choose from user, admin, or developer.")

    # Hash the user's password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Store user data with the hashed password
    user_handler.create_user(username, hashed_password, role=role, status="pending")
    return {"message": "User registered successfully"}


# Define a route for user login
@router.post("/login", response_model=dict)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_handler = UserHandler(db)
    user = user_handler.get_user_by_username(form_data.username)

    if not user:
        log.info('No such user')
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify the hashed password
    if not bcrypt.checkpw(form_data.password.encode('utf-8'), user.password.encode('utf-8')):
        log.info('Invalid credentials')
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if user.status == "approved":
        access_token = create_access_token({"sub": form_data.username, "role": user.role})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Account not approved")


# Define a route for an administrator to approve a user
@router.post("/approve_user/{username}", tags=["admin"], response_model=dict)
async def approve_user(username: str, current_user: dict = Depends(is_admin), db: Session = Depends(get_db)):
    user_handler = UserHandler(db)
    user = user_handler.get_user_by_username(username)

    if not user:
        log.info(f'User {username} not found')
        raise HTTPException(status_code=404, detail="User not found")

    if user.status == 'pending':
        user_handler.update_user_status(user, 'approved')
        return {"message": f"User '{username}' has been approved"}
    else:
        raise HTTPException(status_code=400, detail="User is not in a pending state")

# Define a route to check token validity and expiration
@router.get("/verify_token", summary="Check Token Validity", tags=["User"], response_model=dict)
async def check_token(current_user: dict = Depends(verify_token)):
    if current_user is None:
        log.info('token validity expired')
        return {"message": "Token is expired", "status_code": 403}
    return {"message": "Token is valid and ready to use"}