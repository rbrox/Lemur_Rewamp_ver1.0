import uvicorn
from fastapi import FastAPI, HTTPException
from app.model import UserSchema, BotSchema, UserCreateSchema


# Temporary import for demonstration purposes
users = []

app = FastAPI()


@app.get("/", tags=["test"])
def greet():
    return {"Hello":"World!"}

@app.get("/users", response_model=list[UserSchema], tags=["test"])
def get_users():
    """
    Endpoint to retrieve all users.
    """
    return users # this is a data leak to be fixed later


@app.post("/signup", tags=["auth"])
def signup(user:UserCreateSchema):
    """
    Endpoint to sign up a new user.
    """
    # Check for existing email
    for existing_user in users:
        if existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="User already exists with this email")
    
    users.append(user)
    return {"message": "User signed up successfully", "user": user}