from pydantic import BaseModel


class CreateTodoRequest(BaseModel):
    content: str

class UpdateTodoRequest(BaseModel):
    content: str
