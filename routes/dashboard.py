# Lib
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Annotated

# Utilities
from utilities.hash import oauth2_scheme, get_active_user

# Config
from config.db import conn

dashboard_router = APIRouter(prefix="/dashboard")

# Get Blogs endpoint


@dashboard_router.get("")
async def get_blogs_for_user(*, page: int = Query(1, description="Page number to be fetched"), 
                            limit: int = Query(5, description="Number of blogs to fetch"),
                            token: Annotated[str, Depends(oauth2_scheme)]):
    
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
