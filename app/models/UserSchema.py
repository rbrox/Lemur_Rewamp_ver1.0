from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserLoginSchema(BaseModel):
    
    email: EmailStr
    password: str
    class Config:
        schema_extra = {
            "example": {
                
                "email": "john@example.com",
                "password": "securepassword123"
                
            }}
        
class UserSchema(UserLoginSchema):
    name: str
    
