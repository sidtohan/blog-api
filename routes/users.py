# Lib
from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from datetime import timezone, timedelta, datetime
from jose import jwt, JWTError

# Models
from models.user import User, UserLR, Token, TokenData

# Config
from config.db import conn

user_router = APIRouter(prefix='/users', tags=['users'])
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


# For JWT
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Utility Functions
def verify_password(plain_pass: str, hashed_pass: str) -> bool:
    return pwd_context.verify(plain_pass, hashed_pass)


def get_password_hash(plain_pass: str) -> str:
    return pwd_context.hash(plain_pass)


async def get_user(username: str) -> User | None:
    find_user = conn.blogAPI.users.find_one({"username": username})
    return find_user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_active_user(token: str) -> User | None:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Register Endpoint
@user_router.post("/register")
async def register_user(user: User):
    # Check if present
    find_user = await get_user(user.username)
    if find_user is not None:
        raise HTTPException(status_code=400, detail="User already present")
    # Add
    try:
        user.password = get_password_hash(user.password)
        new_user = conn.blogApp.users.insert_one(dict(user))
        return {"Message": "User added successfully"}
    except Exception as e:
        print("Error occurred:", e)

# Login Endpoint
@user_router.post("/login")
async def login_user(user: UserLR):
    username = user.username
    password = user.password
    find_user = conn.blogApp.users.find_one({"username": username})
    if find_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    hashed_password = find_user["password"]
    if verify_password(password, hashed_password) == False:
        raise HTTPException(status_code=401, detail="Incorrect password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
