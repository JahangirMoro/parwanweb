from pydantic import BaseModel, EmailStr

class AdminUserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class AdminUserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True
