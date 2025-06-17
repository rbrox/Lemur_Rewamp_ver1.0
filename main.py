import uvicorn
from fastapi import FastAPI, HTTPException, Body, Depends
from app.models.user import UserSchema, UserLoginSchema
from app.auth.jwt_handler import sign_jwt, decode_jwt
from app.auth.jwt_bearer import JWTBearer





# Temporary import for demonstration purposes
users_store = []

app = FastAPI()


@app.get("/", tags=["test"])
def greet():
    return {"Hello":"World!"}

@app.get("/users", response_model=list[UserSchema], tags=["test"])
def get_users():
    """
    Endpoint to retrieve all users.
    """
    return users_store # this is a data leak to be fixed later


@app.get("/validate", dependencies=[Depends(JWTBearer())], tags=["test"])
def validate_jwt(token: str = Depends(JWTBearer())):
    """
    Endpoint to validate JWT token.
    """
    try:
        payload = decode_jwt(token)
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))




@app.post("/signup", tags=["auth"])
def signup(user:UserSchema):
    """
    Endpoint to sign up a new user.
    """
    # Check for existing email
    for existing_user in users_store:
        if existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="User already exists with this email")
        
    users_store.append(user)# TO be replaced with database logic

    return sign_jwt(user.email)
    
@app.post("/login", tags=["auth"])
def login(user: UserLoginSchema):
    """
    Endpoint to log in a user.
    """
    for existing_user in users_store:
        if existing_user.email == user.email and existing_user.password == user.password:
            return sign_jwt(user.email)
        
        elif existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="Incorrect password")

    raise HTTPException(status_code=404, detail="User not found")