# Python
from uuid import UUID
from typing import Optional
from datetime import date

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

class UsersBase(BaseModel):
    """ Informacion basica del usuario cuando esta por registrarse"""
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)
    
class UserLogin(UsersBase):
    password:str = Field(...,min_length=8,max_length=64)

class User(UsersBase):
    first_name: str = Field(...,min_length=1,max_length=50)
    last_name: str = Field(...,min_length=1,max_length=50)
    birth_date: Optional[date] = Field(default=None)

class UserRegister(User, UserLogin):
    pass
