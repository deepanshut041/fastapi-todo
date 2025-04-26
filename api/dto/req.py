from pydantic import BaseModel


class CreateTodoRequest(BaseModel):
    content: str
