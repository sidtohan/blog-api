# Lib
from fastapi import APIRouter, HTTPException, Depends, Form
from datetime import timedelta
from jose import jwt, JWTError
from typing import Annotated

# Models
from models.user import User, Token, TokenData

# Config
from config.db import conn

# Utilites
from utilities.hash import SECRET_KEY, ALGORITHM, get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, oauth2_scheme, get_user, get_active_user
user_router = APIRouter(prefix='/users', tags=['users'])

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
        new_user = conn.blogAPI.users.insert_one(dict(user))
        return {"Message": "User added successfully"}
    except Exception as e:
        print("Error occurred: ", e)
    raise HTTPException(status_code=500)


# Login Endpoint
@user_router.post("/login")
async def login_user(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    find_user = conn.blogAPI.users.find_one({"username": username})
    if find_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    hashed_password = find_user["password"]
    if verify_password(password, hashed_password) == False:
        raise HTTPException(status_code=401, detail="Incorrect password")

    # Access Token Generate
    try:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
    except Exception as e:
        print("Error occurred: ", e)
    raise HTTPException(status_code=500)


# Update Endpoint
@user_router.put("/update")
async def update_user(user: User, token: Annotated[str, Depends(oauth2_scheme)]):
    username = user.username
    password = user.password

    # Check if user present
    find_user = conn.blogAPI.users.find_one({"username": username})
    if find_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Updation possible only if user is logged in
    token_user = await get_active_user(token)
    if token_user["username"] != username or verify_password(password, token_user["password"]) == False:
        raise HTTPException(status_code=401)

    # Update user now
    user.password = get_password_hash(user.password)
    conn.blogAPI.users.find_one_and_update(
        {"_id": find_user["_id"]}, {"$set": dict(user)})
    return {"Message": "User updated successfully"}
