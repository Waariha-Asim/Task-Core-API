from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, field_validator

from database import get_connection


app = FastAPI(
    title="TaskCore API",
    version="3.0.0",
    description=(
        "A RESTful Task Management API built with FastAPI and PostgreSQL. "
        "It demonstrates CRUD operations, request validation, task search, "
        "statistics, persistent database storage, and container-ready deployment."
    ),
)


# ============================================================
# Database Initialization
# ============================================================

def initialize_database():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT FALSE
                );
                """
            )

            cursor.execute(
                """
                INSERT INTO tasks (title, done)
                SELECT 'Complete Backend AI assignment', FALSE
                WHERE NOT EXISTS (
                    SELECT 1 FROM tasks
                );
                """
            )

            cursor.execute(
                """
                INSERT INTO tasks (title, done)
                SELECT 'Review PostgreSQL documentation', TRUE
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM tasks
                    WHERE title = 'Review PostgreSQL documentation'
                );
                """
            )

            cursor.execute(
                """
                INSERT INTO tasks (title, done)
                SELECT 'Test PostgreSQL persistence', FALSE
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM tasks
                    WHERE title = 'Test PostgreSQL persistence'
                );
                """
            )

        connection.commit()

    finally:
        connection.close()


@app.on_event("startup")
def startup():
    initialize_database()


# ============================================================
# Pydantic Models
# ============================================================

class Task(BaseModel):
    id: int
    title: str
    done: bool


class TaskCreate(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Task title cannot be empty.")

        return value.strip()


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("Task title cannot be empty.")

        return value.strip() if value is not None else value


class TaskStats(BaseModel):
    total: int
    completed: int
    pending: int


class HealthResponse(BaseModel):
    status: str


class RootResponse(BaseModel):
    name: str
    version: str
    storage: str


# ============================================================
# Meta Endpoints
# ============================================================

@app.get(
    "/",
    response_model=RootResponse,
    tags=["Meta"],
    summary="API overview",
)
def read_root():
    return {
        "name": "TaskCore API",
        "version": "3.0.0",
        "storage": "PostgreSQL",
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Meta"],
    summary="Health check",
)
def health_check():
    return {"status": "ok"}


# ============================================================
# Task Endpoints
# ============================================================

@app.get(
    "/tasks",
    response_model=list[Task],
    tags=["Tasks"],
    summary="List all tasks",
)
def get_tasks(search: Optional[str] = None):

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            if search:
                cursor.execute(
                    """
                    SELECT id, title, done
                    FROM tasks
                    WHERE title ILIKE %s
                    ORDER BY id;
                    """,
                    (f"%{search}%",),
                )
            else:
                cursor.execute(
                    """
                    SELECT id, title, done
                    FROM tasks
                    ORDER BY id;
                    """
                )

            return cursor.fetchall()

    finally:
        connection.close()


@app.get(
    "/tasks/stats",
    response_model=TaskStats,
    tags=["Tasks"],
    summary="Get task statistics",
)
def get_task_stats():

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    COUNT(*) AS total,
                    COUNT(*) FILTER (WHERE done = TRUE) AS completed,
                    COUNT(*) FILTER (WHERE done = FALSE) AS pending
                FROM tasks;
                """
            )

            return cursor.fetchone()

    finally:
        connection.close()


@app.get(
    "/tasks/{task_id}",
    response_model=Task,
    tags=["Tasks"],
    summary="Get a single task",
)
def get_task(task_id: int):

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT id, title, done
                FROM tasks
                WHERE id = %s;
                """,
                (task_id,),
            )

            task = cursor.fetchone()

            if task is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Task {task_id} not found",
                )

            return task

    finally:
        connection.close()


@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"],
    summary="Create a new task",
)
def create_task(payload: TaskCreate):

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO tasks (title, done)
                VALUES (%s, FALSE)
                RETURNING id, title, done;
                """,
                (payload.title,),
            )

            task = cursor.fetchone()

        connection.commit()

        return task

    finally:
        connection.close()


@app.put(
    "/tasks/{task_id}",
    response_model=Task,
    tags=["Tasks"],
    summary="Update an existing task",
)
def update_task(task_id: int, payload: TaskUpdate):

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT id, title, done
                FROM tasks
                WHERE id = %s;
                """,
                (task_id,),
            )

            existing_task = cursor.fetchone()

            if existing_task is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Task {task_id} not found",
                )

            new_title = (
                payload.title
                if payload.title is not None
                else existing_task["title"]
            )

            new_done = (
                payload.done
                if payload.done is not None
                else existing_task["done"]
            )

            cursor.execute(
                """
                UPDATE tasks
                SET title = %s,
                    done = %s
                WHERE id = %s
                RETURNING id, title, done;
                """,
                (new_title, new_done, task_id),
            )

            updated_task = cursor.fetchone()

        connection.commit()

        return updated_task

    finally:
        connection.close()


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Tasks"],
    summary="Delete a task",
)
def delete_task(task_id: int):

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                DELETE FROM tasks
                WHERE id = %s
                RETURNING id;
                """,
                (task_id,),
            )

            deleted_task = cursor.fetchone()

            if deleted_task is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Task {task_id} not found",
                )

        connection.commit()

    finally:
        connection.close()
