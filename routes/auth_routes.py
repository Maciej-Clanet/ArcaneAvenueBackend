from fastapi import APIRouter, HTTPException


from models.auth_models import AuthResponse, LoginForm, RegisterForm

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

    # check if account already exists
    
    existing_user = TEMP_USERS.get(form.email)

    if(existing_user):
        raise HTTPException(
            status_code=409,
            detail="A user with this email already exists"
        )
    

    #add the user
    TEMP_USERS[form.email] = form.model_dump()

    print(TEMP_USERS)

    
    return AuthResponse(
        email=form.email,
        account_type=form.account_type
    )


@auth_router.post("/Login", response_model=AuthResponse)
def register_user(form: LoginForm):

    print(TEMP_USERS)

    existing_user = TEMP_USERS.get(form.email)
    print(existing_user)
    if(existing_user == None):
       raise HTTPException(
           status_code=404,
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

