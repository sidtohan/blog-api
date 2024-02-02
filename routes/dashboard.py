# Lib
from fastapi import APIRouter, HTTPException, Depends, Path, Query
from typing import Annotated, List
from bson.objectid import ObjectId

# Utilities
from utilities.hash import oauth2_scheme, get_active_user
from utilities.mapBlog import mapBlog

# Models
from models.blog import BlogInDb

# Config
from config.db import conn

dashboard_router = APIRouter(prefix="/dashboard", tags=["dashboard"])

# Get Blogs endpoint
@dashboard_router.get("/explore")
async def get_blogs_for_user(*, page: int = Query(1, description="Page number to be fetched"), 
                            limit: int = Query(5, description="Number of blogs to fetch"),
                            token: Annotated[str, Depends(oauth2_scheme)]) -> List[BlogInDb]:
    
    user = await get_active_user(token)
    skip = (page - 1) * limit

    # List of tags also obtained with this
    tags = user["tags"]

    try:
        # Aggregation pipeline
        blogs_retrieved_cursor = conn.blogAPI.blogs.aggregate([{"$match": {
            "tags": {
                "$in": tags
            }
        }}, 
        {
            "$set": {
                "matches": {
                    "$size": {
                        "$setIntersection": [tags, "$tags"]
                    }
                }
            }
        }, 
        {
            "$sort": {
                "matches": -1
            }
        },
        {
            "$skip": skip
        },
        {
            "$limit": limit
        },
        {
            "$unset": "matches"
        }])

        # Actual blogs
        blogs_retrieved = []
        for blog in blogs_retrieved_cursor:
            blog["id"] = str(blog["_id"])
            blog["by_id"] = str(blog["by_id"])
            del blog["_id"]
            blogs_retrieved.append(blog)

        return blogs_retrieved
    
    except Exception as e:
        print("Error occurred: ", e)

    raise HTTPException(status_code=500)


# Get Trending Blogs endpoint
@dashboard_router.get("/trending")
async def get_trending_blogs(*, page: int = Query(1, description="Page number to be fetched"), 
                            limit: int = Query(5, description="Number of blogs to fetch"),
                            token: Annotated[str, Depends(oauth2_scheme)]) -> List[BlogInDb]:
    skip = (page - 1) * limit
    try:
        blogs_retrieved_cursor = conn.blogAPI.blogs.aggregate([{
            "$set": {
                "likes": {
                    "$size": "$liked"
                }
            }
        },
        {
            "$sort": {
                "likes": -1
            }
        }, 
        {
            "$skip": skip
        },
        {
            "$limit": limit
        }, 
        {
            "$unset": "likes"
        }])        
        blogs_retrieved = []
        for blog in blogs_retrieved_cursor:
            blogs_retrieved.append(mapBlog(blog))

        return blogs_retrieved
    except Exception as e:
        print("Error occurred: ", e)

    raise HTTPException(status_code = 500)


# Like Blog endpoint
@dashboard_router.put("/{blog_id}")
async def like_blog(token: Annotated[str, Depends(oauth2_scheme)], 
                    blog_id: str = Path(description="ID of the blog to be liked")):
    find_blog = conn.blogAPI.blogs.find_one({"_id": ObjectId(blog_id)})

    if find_blog is None:
        raise HTTPException(status_code=404, detail="Specified blog not found")
    
    user = await get_active_user(token)
    if user in find_blog["liked"]:
        raise HTTPException(status_code=400, detail="You have already liked this blog")
    
    try:
        updated_blog = dict(find_blog)
        updated_blog["liked"].append(user["_id"])
        conn.blogAPI.blogs.find_one_and_update({"_id": ObjectId(blog_id)},{"$set": dict(updated_blog)})

        return {"Message": "Blog liked successfully"}
    
    except Exception as e:
        print("Error occurred: ", e)

    raise HTTPException(status_code=500)