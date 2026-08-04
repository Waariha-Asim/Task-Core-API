# TaskCore API
A lightweight, production-style **RESTful Task Management API** built with FastAPI. TaskCore demonstrates clean CRUD architecture, strict request validation, correct HTTP semantics, and auto-generated interactive documentation via OpenAPI — all in a single, readable file.

---

## 📸 API Documentation & Testing

The API can be tested interactively through FastAPI Swagger documentation:

`http://127.0.0.1:8000/docs`

---

## Project Preview

### Swagger API Documentation

<div align="center">
  <img src="App UI.png" width="85%" />
</div>

<br>

### Get All Tasks Response

<div align="center">
  <img src="Get all Tasks.png" width="85%" />
</div>

---

## Features

- **Full CRUD** — create, retrieve, update, and delete tasks
- **In-memory data store** — zero setup, no external database
- **Strict validation** — blank and whitespace-only titles are rejected
- **Custom error responses** — Pydantic validation errors are caught and returned as clean `400` JSON, not the default FastAPI `422`
- **Predictable error shape** — every error returns `{"error": "..."}`
- **Correct HTTP semantics** — `200`, `201`, `204`, `400`, `404` used precisely
- **Interactive docs** — Swagger UI and ReDoc generated automatically
- **Type-safe** — full type hints and Pydantic models throughout
- **Single-file simplicity** — the entire service lives in `main.py`

---

## Tech Stack

| Component  | Technology            |
|------------|------------------------|
| Language   | Python 3.11+           |
| Framework  | FastAPI                |
| Validation | Pydantic               |
| Server     | Uvicorn (ASGI)         |
| Docs       | OpenAPI / Swagger UI   |

---

## Project Structure

```
taskcore-api/
└── main.py
```

The entire application — models, routes, validation, and storage — lives in one file for clarity and portability.

---

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip

### Installation

```bash
git clone https://github.com/<your-username>/taskcore-api.git
cd taskcore-api
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install fastapi uvicorn
```

### Run the server

```bash
uvicorn main:app --reload
```

The API will be live at `http://127.0.0.1:8000`.

### Interactive documentation

| UI      | URL                            |
|---------|----------------------------------|
| Swagger | `http://127.0.0.1:8000/docs`   |
| ReDoc   | `http://127.0.0.1:8000/redoc`  |

---

## API Reference

Base URL: `http://127.0.0.1:8000`

### `GET /`
Returns basic API metadata.

**200 OK**
```json
{
  "name": "TaskCore API",
  "version": "1.0.0",
  "endpoints": ["/tasks"]
}
```

### `GET /health`
Liveness check.

**200 OK**
```json
{ "status": "ok" }
```

### `GET /tasks`
Returns all tasks.

**200 OK**
```json
[
  { "id": 1, "title": "Complete Backend AI assignment", "done": false },
  { "id": 2, "title": "Review FastAPI documentation", "done": true },
  { "id": 3, "title": "Push project to GitHub", "done": false }
]
```

### `GET /tasks/{id}`
Returns a single task by ID.

**200 OK**
```json
{ "id": 1, "title": "Complete Backend AI assignment", "done": false }
```

**404 Not Found**
```json
{ "error": "Task 99 not found" }
```

### `POST /tasks`
Creates a new task. ID is auto-assigned; `done` defaults to `false`.

**Request**
```json
{ "title": "Prepare internship portfolio" }
```

**201 Created**
```json
{ "id": 4, "title": "Prepare internship portfolio", "done": false }
```

**400 Bad Request** — missing, empty, or whitespace-only title
```json
{ "error": "Task title cannot be empty." }
```

### `PUT /tasks/{id}`
Updates `title` and/or `done`. Both fields optional.

**Request**
```json
{ "title": "Finalize internship portfolio", "done": true }
```

**200 OK**
```json
{ "id": 4, "title": "Finalize internship portfolio", "done": true }
```

**404 Not Found**
```json
{ "error": "Task 99 not found" }
```

**400 Bad Request**
```json
{ "error": "Task title cannot be empty." }
```

### `DELETE /tasks/{id}`
Deletes a task.

**204 No Content** — empty response body

**404 Not Found**
```json
{ "error": "Task 99 not found" }
```

---

## HTTP Status Codes

| Code | Meaning     | Trigger                                   |
|------|-------------|---------------------------------------------|
| 200  | OK          | Successful `GET` / `PUT`                    |
| 201  | Created     | Task successfully created                   |
| 204  | No Content  | Task successfully deleted                   |
| 400  | Bad Request | Missing, empty, or whitespace-only title     |
| 404  | Not Found   | Task ID does not exist                       |

---

## Example Usage

```
# Create a task
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Ship v1.0"}'

# Mark it complete
curl -X PUT http://127.0.0.1:8000/tasks/4 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'

# Delete it
curl -X DELETE http://127.0.0.1:8000/tasks/4
```

---

## License

Released under the [MIT License](LICENSE). Free to use for learning, portfolio, and derivative projects.
