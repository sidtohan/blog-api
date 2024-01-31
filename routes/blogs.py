# Lib
from fastapi import APIRouter, HTTPException, Query

# Models
from models.blog import Blog

# Config
from config.db import conn


blog_router = APIRouter(prefix="/blogs", tags=["blogs"])

# Blog Create Endpoint
@blog_router.post("")
async def create_blog(blog: Blog):
    try:
        new_blog = conn.blogAPI.blogs.insert_one(dict(blog))
        return {"Message": "Blog created successfully"}
    except Exception as e:
        print("Error occurred: ", e)

    raise HTTPException(status_code=500)

# Get Blogs Endpoint
@blog_router.get("")
async def get_blogs(page: int = Query(1, description="Page number to be retrieved"), limit: int = Query(5, description="Number of blogs retrieved"), tags: list = Query([],description="List of tags to filter blogs")):
    try:
        skip = (page - 1) * limit
        if len(tags) >= 1: retrieved_blogs_cursor = conn.blogAPI.blogs.find({"tags": {"$in": tags}}).skip(skip).limit(limit)
        else: retrieved_blogs_cursor = conn.blogAPI.blogs.find().skip(skip).limit(limit)
        retrieved_blogs = []
        # Convert _id to str type to avoid issues
        for blog in retrieved_blogs_cursor:
            blog["id"] = str(blog["_id"])
            del blog["_id"]
            retrieved_blogs.append(blog)
        return retrieved_blogs
    except Exception as e:
        print("Error occurred: ", e)

    raise HTTPException(status_code=500)
