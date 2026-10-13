from fastapi import APIRouter, HTTPException


from models.auth_models import LoginForm, RegisterForm, AuthResponse

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

@auth_router.get("/test")
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
