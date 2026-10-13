from fastapi import APIRouter, HTTPException


from models.auth_models import AuthResponse, LoginForm, RegisterForm

from database import users


from pymongo.errors import DuplicateKeyError
auth_router = APIRouter()


TEMP_USERS = {
    "goob@gmail.com" : {
        "email": "goob@gmail.com",
        "password" : "test",
        "account_type":"buyer"
    }
}


@auth_router.get("/test")
def read_root():
    return {"auth": "test"}


@auth_router.post("/regiser", response_model=AuthResponse)
def register_user(form: RegisterForm):


    try: 
        users.insert_one( form.model_dump() )
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail="A user with this email already exists"
        )

    
    return AuthResponse(
        email=form.email,
        account_type=form.account_type
    )


@auth_router.post("/Login", response_model=AuthResponse)
def register_user(form: LoginForm):

   

    existing_user = users.find_one({"email" : form.email})

    if(existing_user == None):
       raise HTTPException(
           status_code=401,
           detail="Incorrect Credentials"
       )

    if(form.password != existing_user["password"]):
        raise HTTPException(
            status_code=500,
            detail="Incorrect Credentials"
        )



    return AuthResponse(
        email=existing_user["email"],
        account_type=existing_user["account_type"]
    )

