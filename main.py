from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request

app = FastAPI(
    title="TaskCore API",
    version="1.0.0",
    description=(
        "A RESTful Task Management API built with FastAPI that demonstrates "
        "CRUD operations, request validation, proper HTTP status codes, and "
        "interactive Swagger documentation using OpenAPI."
    ),
)

class Task(BaseModel):
    id: int
    title: str
    done: bool

class TaskCreate(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        if value is None or not value.strip():
            raise ValueError("Task title cannot be empty.")
        return value.strip()

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank_if_provided(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("Task title cannot be empty.")
        return value.strip() if value is not None else value

class RootResponse(BaseModel):
    name: str
    version: str
    endpoints: List[str]

class HealthResponse(BaseModel):
    status: str

tasks: List[dict] = [
    {
        "id": 1,
        "title": "Complete Backend AI assignment",
        "done": False,
    },
    {
        "id": 2,
        "title": "Review FastAPI documentation",
        "done": True,
    },
    {
        "id": 3,
        "title": "Push project to GitHub",
        "done": False,
    },
]

def _get_next_id() -> int:
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1

def _find_task(task_id: int) -> Optional[dict]:
    return next((task for task in tasks if task["id"] == task_id), None)

@app.get(
    "/",
    response_model=RootResponse,
    status_code=status.HTTP_200_OK,
    summary="API overview",
    description="Return basic metadata about the TaskCore API.",
    tags=["Meta"],
)
def read_root() -> RootResponse:
    return RootResponse(name="TaskCore API", version="1.0.0", endpoints=["/tasks"])

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

@app.get(
    "/tasks",
    response_model=List[Task],
    status_code=status.HTTP_200_OK,
    summary="List all tasks",
    description="Retrieve the full list of tasks currently stored in memory.",
    tags=["Tasks"],
)
def get_tasks() -> List[dict]:
    return tasks

@app.get(
    "/tasks/{task_id}",
    response_model=Task,
    status_code=status.HTTP_200_OK,
    summary="Get a single task",
    description="Retrieve a single task by its unique ID.",
    tags=["Tasks"],
)
def get_task(task_id: int):
    task = _find_task(task_id)
    if task is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Task {task_id} not found"},
        )
    return task

@app.post(
    "/tasks",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task with an auto-generated ID and done=false.",
    tags=["Tasks"],
)
def create_task(payload: TaskCreate):
    new_task = {
        "id": _get_next_id(),
        "title": payload.title,
        "done": False,
    }
    tasks.append(new_task)
    return new_task

@app.put(
    "/tasks/{task_id}",
    response_model=Task,
    status_code=status.HTTP_200_OK,
    summary="Update an existing task",
    description="Update the title and/or done status of an existing task.",
    tags=["Tasks"],
)
def update_task(task_id: int, payload: TaskUpdate):
    task = _find_task(task_id)
    if task is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Task {task_id} not found"},
        )

    if payload.title is not None:
        task["title"] = payload.title
    if payload.done is not None:
        task["done"] = payload.done

    return task

@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Delete a task by its unique ID.",
    tags=["Tasks"],
)
def delete_task(task_id: int):
    task = _find_task(task_id)
    if task is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"Task {task_id} not found"},
        )
    tasks.remove(task)
    return None

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    message = "Invalid request data."

    if errors:
        first_error = errors[0]
        error_type = first_error.get("type", "")
        error_msg = first_error.get("msg", "")

        if "title" in first_error.get("loc", []):
            if "missing" in error_type:
                message = "Task title is required."
            elif "empty" in error_msg.lower():
                message = "Task title cannot be empty."
            else:
                message = error_msg.replace("Value error, ", "")
        else:
            message = error_msg.replace("Value error, ", "")

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": message},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)