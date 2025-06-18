import uvicorn
from fastapi import FastAPI, HTTPException, Body, Depends
from app.models.UserSchema import UserSchema, UserLoginSchema
from app.auth.jwt_handler import sign_jwt, decode_jwt
from app.auth.jwt_bearer import JWTBearer
from app.database import crud
from app.database.models.user import User
from app.database.db import Base, engine, get_db
from sqlalchemy.orm import Session

# Create tables if not exist
Base.metadata.create_all(bind=engine)



app = FastAPI()


@app.get("/", tags=["test"])
def greet():
    return {"Hello":"World!"}

@app.get("/users", response_model=list[UserSchema], tags=["test"])
def get_users( db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all users.
    """
    
    try: 
        users =  crud.get_users(db)
    except Exception as e: 
        return HTTPException(status_code=500, detail="Something went wrong while fetching users")

    return users
    # this is a data leak to be fixed later


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
def signup(user:UserSchema, db: Session = Depends(get_db)):
    """
    Endpoint to sign up a new user.
    """
    # Check for existing email
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="User already exists with this email")
        
    
    user = crud.create_user(db=db, name=user.name, email=user.email, password=user.password)

    return sign_jwt(user.email)
    
@app.post("/login", tags=["auth"])
def login(user: UserLoginSchema, db: Session = Depends(get_db)):
    """
    Endpoint to log in a user.
    """
    try :
        existing_user = crud.get_user_by_email(db, user.email)
        if existing_user.email == user.email and existing_user.password == user.password:
            return sign_jwt(user.email)
        elif existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="Incorrect password")
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Something went wrong while logging in")

        
        
        

    