from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware 

from routes.auth_routes import auth_router
 
# this is the entire application
app = FastAPI() 

# allows our frontend to communicate with the backend
app.add_middleware( 
    CORSMiddleware, 
    allow_origins=["http://localhost:3000", "http://localhost:3001"], 
    allow_methods=["*"], 
    allow_headers=["*"], 
) 

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"]
)

 
# this is a testing endpoint for 
# easily seeing if our app crashed
@app.get("/") 
def get_test(): 
    return {"hello": "world"} 

