# Lib
from fastapi import APIRouter, HTTPException, Query, Path, Depends
from bson.objectid import ObjectId
from typing import Annotated

# Models
from models.blog import Blog

# Config
from config.db import conn

# Utilites
from utilities.hash import oauth2_scheme, get_active_user

blog_router = APIRouter(prefix="/blogs", tags=["blogs"])

# Blog Create Endpoint
@blog_router.post("")
async def create_blog(blog: Blog, token: Annotated[str, Depends(oauth2_scheme)]):
    user = await get_active_user(token)
    try:
        new_blog = dict(blog)
        new_blog["by"] = user["username"]
        new_blog["by_id"] = user["_id"]
        new_blog["by_photo"] = user["photo"]
        conn.blogAPI.blogs.insert_one(new_blog)
        return {"Message": "Blog created successfully"}
    except Exception as e:
        print("Error occurred: ", e)

    raise HTTPException(status_code=500)

# Get Blogs Endpoint
@blog_router.get("")
async def get_blogs(*, page: int = Query(1, description="Page number to be retrieved"),
                    limit: int = Query(
                        5, description="Number of blogs retrieved"),
                    tags: list = Query(
                        [], description="List of tags to filter blogs"),
                    token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        skip = (page - 1) * limit
        if len(tags) >= 1:
            retrieved_blogs_cursor = conn.blogAPI.blogs.find(
                {"tags": {"$in": tags}}).skip(skip).limit(limit)
        else:
            retrieved_blogs_cursor = conn.blogAPI.blogs.find().skip(skip).limit(limit)
        retrieved_blogs = []
        # Convert _id to str type to avoid issues
        for blog in retrieved_blogs_cursor:
            blog["id"] = str(blog["_id"])
            del blog["_id"]
            blog["by_id"] = str(blog["by_id"])
            retrieved_blogs.append(blog)
        return retrieved_blogs
    except Exception as e:
        print("Error occurred: ", e)

    raise HTTPException(status_code=500)

# Blog by ID endpoint
@blog_router.get("/{blog_id}")
async def get_blog_by_id(*, blog_id: str = Path(description="ID of the blog to be retrieved"), token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        retrieved_blog = conn.blogAPI.blogs.find_one(
            {"_id": ObjectId(blog_id)})
        retrieved_blog["id"] = str(retrieved_blog["_id"])
        retrieved_blog["by_id"] = str(retrieved_blog["by_id"])
        del retrieved_blog["_id"]
        return retrieved_blog
    except Exception as e:
        print("Error occurred: ", e)

    raise HTTPException(status_code=500)

# Update Blog endpoint
@blog_router.put("/{blog_id}")
async def update_blog(*, blog: Blog, blog_id: str = Path(description="ID of the blog to be updated"), token: Annotated[str, Depends(oauth2_scheme)]):
    find_blog = conn.blogAPI.blogs.find_one({"_id": ObjectId(blog_id)})
    if find_blog is None:
        raise HTTPException(status_code=404, detail="Specified blog not found")
    
    # Check if user is valid
    user = await get_active_user(token)
    if find_blog["by_id"] != user["_id"]:
        raise HTTPException(status_code=401, detail="You are not authorized to edit this blog")

    # Actual update
    try:
        conn.blogAPI.blogs.find_one_and_update(
            {"_id": ObjectId(blog_id)}, {"$set": dict(blog)})
        return {"Message": "Blog updated successfully"}
    except Exception as e:
        print("Error occurred: ", e)

    raise HTTPException(status_code=500)

# Delete Blog endpoint
@blog_router.delete("/{blog_id}")
async def delete_blog(*, blog_id: str = Path(description="ID of the blog to be deleted"),
                      token: Annotated[str, Depends(oauth2_scheme)]):
    find_blog = conn.blogAPI.blogs.find_one({"_id": ObjectId(blog_id)})
    user = await get_active_user(token)
    if find_blog["by_id"] != user["_id"]:
        raise HTTPException(status_code=401, detail="You are not authorized to delete this blog")
    try:
        conn.blogAPI.blogs.delete_one({'_id': ObjectId(blog_id)})
        return {"Message": "Blog deleted successfully"}
    except Exception as e:
        print("Error occurred: ", e)
    raise HTTPException(status_code=500)
