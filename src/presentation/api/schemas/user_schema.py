from pydantic import BaseModel

class AuthUserSchema(BaseModel):
    username: str
    password: str

class AuthUserResponseSchema(BaseModel):
    status: str
    message: str
    access_token: str