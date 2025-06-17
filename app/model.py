from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                
            }}
        
class UserSchema(UserCreateSchema):
    id: UUID
        
class BotSchema(BaseModel):
    id: int
    name: str
    user_id: int  # Foreign key relation
    active: bool = True
    created_at: str  # ISO format date string

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "ChatBot",
                "user_id": 1,
                "active": True,
                "created_at": "2023-10-01T12:00:00Z"
            }
        }