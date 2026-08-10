from typing import List, Optional

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request

from database import get_connection, create_table


app = FastAPI(
    title="TaskCore API",
    version="2.0.0",
    description=(
        "A RESTful Task Management API built with FastAPI and SQLite. "
        "It demonstrates CRUD operations, request validation, persistent "
        "database storage, task search, and task statistics."
    ),
)


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
    def title_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Task title cannot be empty.")
        return value.strip()


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank_if_provided(
        cls,
        value: Optional[str]
    ) -> Optional[str]:

        if value is not None and not value.strip():
            raise ValueError("Task title cannot be empty.")

        return value.strip() if value is not None else value


class RootResponse(BaseModel):
    name: str
    version: str
    endpoints: List[str]


class HealthResponse(BaseModel):
    status: str


class TaskStats(BaseModel):
    total: int
    completed: int
    pending: int


# ============================================================
# Application Startup
# ============================================================

@app.on_event("startup")
def startup():
    create_table()


# ============================================================
# Meta Endpoints
# ============================================================

@app.get(
    "/",
    response_model=RootResponse,
    status_code=status.HTTP_200_OK,
    summary="API overview",
    description="Return basic information about the TaskCore API.",
    tags=["Meta"],
)
def read_root() -> RootResponse:

    return RootResponse(
        name="TaskCore API",
        version="2.0.0",
        endpoints=[
            "/tasks",
            "/tasks/{task_id}",
            "/tasks/stats",
            "/health",
        ],
    )


@app.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Return the current health status of the service.",
    tags=["Meta"],
)
def health_check() -> HealthResponse:

    return HealthResponse(status="ok")


# ============================================================
# GET ALL TASKS + SEARCH
# ============================================================

@app.get(
    "/tasks",
    response_model=List[Task],
    status_code=status.HTTP_200_OK,
    summary="List tasks",
    description=(
        "Retrieve all tasks from SQLite. "
        "Optionally search tasks by title."
    ),
    tags=["Tasks"],
)
def get_tasks(search: Optional[str] = None) -> List[Task]:

    connection = get_connection()

    if search:

        rows = connection.execute(
            """
            SELECT id, title, done
            FROM tasks
            WHERE title LIKE ?
            ORDER BY id
            """,
            (f"%{search}%",),
        ).fetchall()

    else:

        rows = connection.execute(
            """
            SELECT id, title, done
            FROM tasks
            ORDER BY id
            """
        ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


# ============================================================
# GET TASK STATISTICS
# ============================================================

@app.get(
    "/tasks/stats",
    response_model=TaskStats,
    status_code=status.HTTP_200_OK,
    summary="Get task statistics",
    description="Return total, completed, and pending task counts.",
    tags=["Tasks"],
)
def get_task_stats() -> TaskStats:

    connection = get_connection()

    total = connection.execute(
        "SELECT COUNT(*) FROM tasks"
    ).fetchone()[0]

    completed = connection.execute(
        "SELECT COUNT(*) FROM tasks WHERE done = 1"
    ).fetchone()[0]

    pending = connection.execute(
        "SELECT COUNT(*) FROM tasks WHERE done = 0"
    ).fetchone()[0]

    connection.close()

    return TaskStats(
        total=total,
        completed=completed,
        pending=pending,
    )


# ============================================================
# GET SINGLE TASK
# ============================================================

@app.get(
    "/tasks/{task_id}",
    response_model=Task,
    status_code=status.HTTP_200_OK,
    summary="Get a single task",
    description="Retrieve a task by its unique ID.",
    tags=["Tasks"],
)
def get_task(task_id: int):

    connection = get_connection()

    row = connection.execute(
        """
        SELECT id, title, done
        FROM tasks
        WHERE id = ?
        """,
        (task_id,),
    ).fetchone()

    connection.close()

    if row is None:

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": f"Task {task_id} not found"
            },
        )

    return dict(row)


# ============================================================
# CREATE TASK
# ============================================================

@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task with an automatically generated ID.",
    tags=["Tasks"],
)
def create_task(payload: TaskCreate):

    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO tasks (title, done)
        VALUES (?, ?)
        """,
        (payload.title, False),
    )

    connection.commit()

    task_id = cursor.lastrowid

    row = connection.execute(
        """
        SELECT id, title, done
        FROM tasks
        WHERE id = ?
        """,
        (task_id,),
    ).fetchone()

    connection.close()

    return dict(row)


# ============================================================
# UPDATE TASK
# ============================================================

@app.put(
    "/tasks/{task_id}",
    response_model=Task,
    status_code=status.HTTP_200_OK,
    summary="Update an existing task",
    description="Update the title and/or completion status of a task.",
    tags=["Tasks"],
)
def update_task(
    task_id: int,
    payload: TaskUpdate
):

    connection = get_connection()

    existing_task = connection.execute(
        """
        SELECT id, title, done
        FROM tasks
        WHERE id = ?
        """,
        (task_id,),
    ).fetchone()

    if existing_task is None:

        connection.close()

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": f"Task {task_id} not found"
            },
        )

    if payload.title is not None:

        connection.execute(
            """
            UPDATE tasks
            SET title = ?
            WHERE id = ?
            """,
            (payload.title, task_id),
        )

    if payload.done is not None:

        connection.execute(
            """
            UPDATE tasks
            SET done = ?
            WHERE id = ?
            """,
            (payload.done, task_id),
        )

    connection.commit()

    updated_task = connection.execute(
        """
        SELECT id, title, done
        FROM tasks
        WHERE id = ?
        """,
        (task_id,),
    ).fetchone()

    connection.close()

    return dict(updated_task)


# ============================================================
# DELETE TASK
# ============================================================

@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Delete a task by its unique ID.",
    tags=["Tasks"],
)
def delete_task(task_id: int):

    connection = get_connection()

    existing_task = connection.execute(
        """
        SELECT id
        FROM tasks
        WHERE id = ?
        """,
        (task_id,),
    ).fetchone()

    if existing_task is None:

        connection.close()

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": f"Task {task_id} not found"
            },
        )

    connection.execute(
        """
        DELETE FROM tasks
        WHERE id = ?
        """,
        (task_id,),
    )

    connection.commit()
    connection.close()

    return None


# ============================================================
# Validation Error Handler
# ============================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):

    errors = exc.errors()

    message = "Invalid request data."

    if errors:

        first_error = errors[0]

        error_type = first_error.get("type", "")
        error_msg = first_error.get("msg", "")
        location = first_error.get("loc", [])

        if "title" in location:

            if "missing" in error_type:
                message = "Task title is required."

            elif "empty" in error_msg.lower():
                message = "Task title cannot be empty."

            else:
                message = error_msg.replace(
                    "Value error, ",
                    ""
                )

        else:

            message = error_msg.replace(
                "Value error, ",
                ""
            )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": message
        },
    )


# ============================================================
# Run Application
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )
