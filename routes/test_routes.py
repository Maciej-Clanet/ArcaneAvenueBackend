from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from database import test_collection
from pymongo.errors import DuplicateKeyError

test_router = APIRouter()


# add item
class AddItemModel(BaseModel):
    email: str
    description: str


@test_router.post("/add")
def add_item(data: AddItemModel):

    new_item = {
        "email": data.email,
        "description" : data.description
    }

    try:
        result = test_collection.insert_one(new_item)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail="already exists"
        )
    
    print(result.inserted_id)


