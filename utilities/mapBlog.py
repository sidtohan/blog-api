from models.blog import Blog, BlogInDb

def mapBlog(blog: dict) -> dict:
        blog["id"] = str(blog["_id"])
        del blog["_id"]
        blog["by_id"] = str(blog["by_id"])
        blog["liked"] = [str(id) for id in blog["liked"]]
        return blog