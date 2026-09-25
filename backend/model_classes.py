from pydantic import BaseModel


class CreateUserApiData(BaseModel):
    name: str
    email: str
    password: str

class ApiData(BaseModel):
    user_id: str



