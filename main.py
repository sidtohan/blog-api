from fastapi import FastAPI, HTTPException, Path, Query
from config.db import conn
from schemas.user import ConvertUser
from models.user import User
import bcrypt

app = FastAPI()
salt = bcrypt.gensalt()
@app.post("/users")
def add_user(user: User):
    try:
        user.password = str(bcrypt.hashpw(password=bytes(user.password, "utf-8"), salt=salt))
        new_user = conn.blogApp.users.insert_one(dict(user))
        return {"Message": "User added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)
