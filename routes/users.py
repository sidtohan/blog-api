# Lib
from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from datetime import timezone, timedelta, datetime

# Models
from models.user import User, UserLR

# Config
from config.db import conn

user_router = APIRouter(prefix='/users', tags=['users'])
pwd_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")


# For JWT
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Utility Functions
def verify_password(plain_pass: str, hashed_pass: str) -> bool:
    return pwd_context.verify(plain_pass, hashed_pass)

def get_password_hash(plain_pass: str) -> str:
    return pwd_context.hash(plain_pass)

async def user_present(username: str) -> bool:
    return conn.blogAPI.users.find_one({"username": username}) is not None
    
# Register Endpoint
@user_router.post("/register")
async def register_user(user: User):
    # Check if present
    if user_present(user.username):
        raise HTTPException(status_code=400, detail="User already present")
    # Add
    try:
        user.password = get_password_hash(user.password)
        new_user = conn.blogApp.users.insert_one(dict(user))
        return {"Message": "User added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

# Login Endpoint
@user_router.post("/login")
async def login_user(user: UserLR):
    username = user.username
    password = user.password
    try:
        find_user = conn.blogApp.users.find_one({"username": username})
        if find_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        hashed_password = find_user["password"]
        if verify_password(password, hashed_password) == False:
            raise HTTPException(status_code=400, detail="Incorrect password")
        return {"Message": "Login test successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    