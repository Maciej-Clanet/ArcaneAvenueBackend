from fastapi import FastAPI
from routes.auth_routes import auth_router
from routes.test_routes import test_router

app = FastAPI()

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"],
)
app.include_router(
    test_router,
    prefix="/test",
    tags=["Test"]
)

@app.get("/")
def read_root():
    return {"Hello": "goobers"}
