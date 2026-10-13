from fastapi import APIRouter


from models.auth_models import LoginForm, RegisterForm

auth_router = APIRouter()


@auth_router.get("/test")
def read_root():
    return {"auth": "test"}
