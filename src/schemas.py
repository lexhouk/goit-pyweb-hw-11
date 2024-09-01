from pydantic import BaseModel, EmailStr, Field, PastDate


class Request(BaseModel):
    first_name: str = Field(min_length=2, max_length=30)
    last_name: str = Field(min_length=2, max_length=40)
    email: EmailStr = Field(min_length=6, max_length=50)
    phone_number: str = Field(min_length=3, max_length=20)
    birthday: PastDate = Field(None)
    bio: str = Field(None, max_length=400)


class Response(BaseModel):
    id: int = Field(default=1, ge=1)
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: PastDate
    bio: str

    class Config:
        from_attributes = True


Responses = list[Response]
