from typing import Annotated

from sqlalchemy import func
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select

from api.deps import get_async_db_session
from models import Todo
from api.dto.req import CreateTodoRequest
from api.dto.res import CreateTodoResponse, RetrieveTodoResponse, ListTodosResponse, ListTodosResponseItem


# /api/v1/todo
router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("", summary="Create a new todo")
async def create_todo(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
    reqeust_data: CreateTodoRequest,
) -> CreateTodoResponse:
    todo = Todo(content=reqeust_data.content)
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return CreateTodoResponse(
        id=todo.id,
        content=todo.content,
        created_at=todo.created_at,
        updated_at=todo.updated_at,
    )

@router.get("/{todo_id}", summary="Retrieve a todo")
async def retrieve_todo(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
    todo_id: int,
) -> RetrieveTodoResponse:
    stmt = select(
        Todo.id,
        Todo.content,
        Todo.created_at,
        Todo.updated_at,
    ).where(
        Todo.id == todo_id,
        Todo.deleted_at.is_(None),
    )
    result_row = (await db.execute(stmt)).first()

    if result_row is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    mapped_row = result_row._mapping
    return RetrieveTodoResponse(
        id=mapped_row[Todo.id],
        content=mapped_row[Todo.content],
        created_at=mapped_row[Todo.created_at],
        updated_at=mapped_row[Todo.updated_at],
    )

@router.get("", summary="List all todos")
async def list_todos(
    db: Annotated[AsyncSession, Depends(get_async_db_session)],
) -> ListTodosResponse:
    count_stmt = select(func.count(Todo.id)).where(
        Todo.deleted_at.is_(None),
    )
    count_result = (await db.execute(count_stmt)).scalar() or 0

    stmt = (
        select(
            Todo.id,
            Todo.content,
            Todo.created_at,
            Todo.updated_at,
        )
        .where(
            Todo.deleted_at.is_(None),
        )
        .order_by(Todo.created_at.desc())
    )
    result_rows = (await db.execute(stmt)).all()

    return ListTodosResponse(
        count=count_result,
        items=[
            ListTodosResponseItem(
                id=row.id,
                content=row.content,
                created_at=row.created_at,
                updated_at=row.updated_at,
            )
            for row in result_rows
        ],
    )