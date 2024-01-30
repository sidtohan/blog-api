def ConvertUser(item) -> dict:
    return {
        "_id": str(item["_id"]),
        "username": item["username"],
        "password": item["password"],
        "tags": item["tags"]
    }
