# Lib
from fastapi import FastAPI

# Routes
from routes.users import user_router

app = FastAPI()
app.include_router(user_router)

