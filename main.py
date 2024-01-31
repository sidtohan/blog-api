# Lib
from fastapi import FastAPI

# Routes
from routes.users import user_router
from routes.blogs import blog_router

app = FastAPI()
app.include_router(user_router)
app.include_router(blog_router)
