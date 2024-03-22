from pydantic import BaseModel


class Message(BaseModel):
    detail: str


class Success(BaseModel):
    success: bool