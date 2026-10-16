from fastapi import APIRouter, HTTPException


from models.auth_models import LoginForm, RegisterForm, AuthResponse

from database import test_collection

auth_router = APIRouter()

# EVERY TIME OUR SERVER REFRESHES, THIS WILL RESET ITSELF TO THIS
# ANY USERS WE CREATE WILL GET DELTED
FAKE_USER_DB = {
    "goober@gmail.com" : {
        "email" : "goober@gmail.com",
        "password" : "test",
        "account_type" : "buyer"
    }
}

@auth_router.get("/test/")
def read_root():
    return {"auth": "test"}


@auth_router.post("/register", response_model=AuthResponse)
def register_user(form: RegisterForm):


    # check if user already exists
    found_user = FAKE_USER_DB.get(form.email)

    if(found_user):
        raise HTTPException(
            status_code=403,
            detail="User with this email already exists"
        )

    user_dict = form.model_dump()

    FAKE_USER_DB[form.email] = user_dict
    print("new user database: ")
    print(FAKE_USER_DB)

    #safasfsa

    # return the user response so we can automatically log them in 
    return AuthResponse(
        email=form.email,
        account_type=form.account_type
    ) 



@auth_router.post("/login", response_model=AuthResponse)
def login_user(form: LoginForm):

    found_user = FAKE_USER_DB.get(form.email)

    # if no user found, raise an exception saying invalid credentials
    if found_user == None:
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )

    if found_user["password"] != form.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )

    return AuthResponse(
        email=form.email,
        account_type=found_user["account_type"]
    ) 



from pydantic import BaseModel
class TestAdd(BaseModel):
    email: str
    description: str

@auth_router.post("/test_add")
def test_add(data: TestAdd):

    our_data_in_dictionary_format = data.model_dump();

    test_collection.insert_one(our_data_in_dictionary_format)

    print("testing adding an item")
