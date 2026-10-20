import json

from fastapi import APIRouter, HTTPException 

from database import users
from models.auth_models import LoginForm, RegisterForm

from pymongo.errors import DuplicateKeyError

# name this something sensible, usually same as name of the file 
auth_router = APIRouter() 




@auth_router.get("/")
def test_auth_router():
    return {"status" : "works"}

# GET function for requesting data
# We don't need to provide any specifying information for this functionality
@auth_router.get("/all")
def get_all_users():
    # get all users from database
    result = users.find().to_list()
    for user in result:
        user["_id"] = str(user["_id"])
    # result is a Cursor
    print(result)
    
    return{"all_users" : result}


@auth_router.post("/register")
def register_user(form: RegisterForm):


    try:
        users.insert_one({
            "email" : form.email,
            "password" : form.password,
            "account_type" : form.account_type
        })
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail="Account already exists"
        )

    
    return {"status" : "success"}



@auth_router.post("/login")
def login(form: LoginForm):

    found_user = users.find_one({"email" : form.email, "password" : form.password})

    if found_user == None:
        raise HTTPException(
            status_code=404,
            detail="invalid credentials"
        )
    
    return {
        "email" : found_user["email"],
        "account_type" : found_user["account_type"]
    }