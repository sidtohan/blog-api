# Lib
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

# Routes
from routes.users import user_router
from routes.blogs import blog_router
from routes.dashboard import dashboard_router

app = FastAPI()
app.add_middleware(CORSMiddleware, 
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )

@app.get("/")
async def docs_redirect():
    return RedirectResponse(url="/docs")

app.include_router(user_router)
app.include_router(blog_router)
app.include_router(dashboard_router)
