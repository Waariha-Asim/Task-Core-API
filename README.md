# TaskCore API

A production-style **RESTful Task Management API** built with **FastAPI**, developed progressively from an in-memory implementation to persistent **SQLite** and **PostgreSQL** database backends.

The project demonstrates how the same REST API architecture can evolve from a simple backend prototype into a database-backed service while maintaining clean API design, validation, CRUD operations, persistent storage, SQL queries, and interactive OpenAPI documentation.

---

## 🚀 Project Evolution

TaskCore was developed in progressive stages:

| Version  | Implementation    | Key Focus                                           |
| -------- | ----------------- | --------------------------------------------------- |
| **v1.0** | In-Memory Storage | REST API fundamentals & CRUD                        |
| **v2.0** | SQLite            | Persistent local database storage                   |
| **v3.0** | PostgreSQL        | Production-oriented relational database integration |

The project demonstrates the transition from a lightweight API prototype to a persistent, database-backed backend service.

---

## 📸 Project Preview

### TaskCore API — PostgreSQL v3.0

The final PostgreSQL implementation provides the complete REST API with persistent database storage.

![TaskCore API PostgreSQL v3.0](./TaskCore-API-PostgreSQL-Persistance/Screenshot%202026-08-11%20051056.png)

---

## 📸 API Documentation & Testing

TaskCore uses **FastAPI Swagger UI** for interactive API documentation and endpoint testing.

Run the API locally and open:

```text
http://127.0.0.1:8000/docs
```

### SQLite — GET `/tasks`

The SQLite implementation retrieves tasks from a persistent local SQLite database.

![SQLite GET Tasks](./Task-Core-API-Sqlite-Database/Screenshot%202026-08-11%20031242.png)

### PostgreSQL — GET `/tasks`

The PostgreSQL implementation retrieves the same task resources from a PostgreSQL database.

![PostgreSQL GET Tasks](./TaskCore-API-PostgreSQL-Persistance/Screenshot%202026-08-11%20043455.png)

> The API interface remains consistent across both database implementations while the underlying persistence layer changes from SQLite to PostgreSQL.

---

## ✨ Features

### API

* RESTful API architecture
* Complete CRUD operations
* Create, retrieve, update, and delete tasks
* Automatic task ID generation
* Task search by title
* Task statistics
* Health-check endpoint
* API metadata endpoint

### Validation & Error Handling

* Pydantic request and response models
* Task title validation
* Whitespace-only title rejection
* Structured error responses
* Proper HTTP status codes
* 404 handling for missing tasks

### Database

* SQLite persistent storage
* PostgreSQL persistent storage
* SQL-based CRUD operations
* Database connection management
* Persistent data across application restarts
* PostgreSQL environment-based configuration

### Documentation & Deployment

* Automatic OpenAPI specification
* Interactive Swagger UI
* ReDoc documentation
* Docker/Docker Compose configuration for PostgreSQL
* Environment-based configuration

---

## 🛠️ Tech Stack

| Component         | Technology              |
| ----------------- | ----------------------- |
| Language          | Python 3.11+            |
| API Framework     | FastAPI                 |
| Validation        | Pydantic                |
| ASGI Server       | Uvicorn                 |
| Database — v2     | SQLite                  |
| Database — v3     | PostgreSQL              |
| Database Driver   | Psycopg                 |
| API Documentation | OpenAPI / Swagger UI    |
| Configuration     | Environment Variables   |
| Containerization  | Docker / Docker Compose |

---

## 📁 Project Structure

```text
TaskCore-API-SQLite-PostgreSQL/
│
├── Task-Core-API-Sqlite-Database/
│   ├── main.py
│   ├── database.py
│   └── Screenshot 2026-08-11 031242.png
│
├── TaskCore-API-PostgreSQL-Persistance/
│   ├── main.py
│   ├── database.py
│   ├── .env.example
│   ├── Screenshot 2026-08-11 043455.png
│   └── Screenshot 2026-08-11 051056.png
│
└── README.md
```

The implementations are separated so the database progression can be easily inspected and compared.

---

# 🔹 v1.0 — In-Memory Storage

The initial implementation focuses on FastAPI and REST API fundamentals.

### Highlights

* FastAPI application setup
* RESTful CRUD endpoints
* Pydantic models
* Request validation
* Custom error handling
* HTTP status codes
* Swagger/OpenAPI documentation

```text
Client → FastAPI → In-Memory Store
```

Because the data is stored in memory, it is lost when the application restarts.

---

# 🔹 v2.0 — SQLite Persistence

The second implementation introduces a relational database using **SQLite**.

### Improvements

* Persistent task storage
* SQL-based CRUD operations
* Database connection handling
* Search queries
* Task statistics
* Data survives application restarts

```text
Client → FastAPI → SQLite
```

This stage demonstrates the transition from a simple in-memory backend to persistent database storage.

---

# 🔹 v3.0 — PostgreSQL Persistence

The third implementation upgrades TaskCore to **PostgreSQL**, providing a more production-oriented relational database backend.

### Improvements

* PostgreSQL integration
* Psycopg database driver
* Environment-based database configuration
* Persistent relational storage
* SQL CRUD operations
* Task search using PostgreSQL queries
* Database-level task statistics
* Docker/Docker Compose configuration

```text
Client → FastAPI → PostgreSQL
```

The API layer remains largely consistent while the persistence layer is upgraded.

---

# 🔌 API Reference

Base URL:

```text
http://127.0.0.1:8000
```

## Meta Endpoints

### `GET /`

Returns basic API metadata.

**PostgreSQL v3.0 example:**

```json
{
  "name": "TaskCore API",
  "version": "3.0.0",
  "storage": "PostgreSQL"
}
```

---

### `GET /health`

Returns the service health status.

```json
{
  "status": "ok"
}
```

---

## Task Endpoints

### `GET /tasks`

Returns all tasks.

```json
[
  {
    "id": 1,
    "title": "Complete Backend AI assignment",
    "done": false
  },
  {
    "id": 2,
    "title": "Review PostgreSQL documentation",
    "done": true
  }
]
```

### Search Tasks

Tasks can optionally be filtered by title:

```text
GET /tasks?search=backend
```

---

### `GET /tasks/{task_id}`

Retrieves a single task by ID.

```json
{
  "id": 1,
  "title": "Complete Backend AI assignment",
  "done": false
}
```

---

### `POST /tasks`

Creates a new task.

**Request:**

```json
{
  "title": "Prepare internship portfolio"
}
```

**Response — `201 Created`:**

```json
{
  "id": 4,
  "title": "Prepare internship portfolio",
  "done": false
}
```

---

### `PUT /tasks/{task_id}`

Updates an existing task.

**Request:**

```json
{
  "title": "Finalize internship portfolio",
  "done": true
}
```

---

### `DELETE /tasks/{task_id}`

Deletes a task.

**Response:**

```text
204 No Content
```

---

### `GET /tasks/stats`

Returns task statistics.

```json
{
  "total": 4,
  "completed": 1,
  "pending": 3
}
```

---

## 🔒 Request Validation

TaskCore validates incoming request data using Pydantic.

For example, empty or whitespace-only task titles are rejected:

```json
{
  "title": "   "
}
```

This prevents invalid data from reaching the database layer.

---

## 📊 HTTP Status Codes

| Code  | Meaning     | Usage                     |
| ----- | ----------- | ------------------------- |
| `200` | OK          | Successful GET / PUT      |
| `201` | Created     | Task successfully created |
| `204` | No Content  | Task successfully deleted |
| `400` | Bad Request | Invalid task data         |
| `404` | Not Found   | Task does not exist       |

---

# ⚙️ Getting Started

## Prerequisites

* Python 3.11+
* pip
* SQLite for v2.0
* PostgreSQL or a PostgreSQL-compatible database for v3.0

---

## Clone the Repository

```bash
git clone https://github.com/Waariha-Asim/TaskCore-API-SQLite-PostgreSQL.git

cd TaskCore-API-SQLite-PostgreSQL
```

---

## Create a Virtual Environment

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install fastapi uvicorn
```

For PostgreSQL:

```bash
pip install psycopg python-dotenv
```

---

# ▶️ Running the SQLite Version

Navigate to:

```bash
cd Task-Core-API-Sqlite-Database
```

Run:

```bash
uvicorn main:app --reload
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# ▶️ Running the PostgreSQL Version

Navigate to:

```bash
cd TaskCore-API-PostgreSQL-Persistance
```

Configure your database connection in `.env`:

```env
DATABASE_URL=your_postgresql_connection_string
```

Then run:

```bash
uvicorn main:app --reload
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

> Never commit your actual `.env` file or database credentials. Use `.env.example` for sharing configuration structure.

---

# 🐳 Docker Support

The PostgreSQL implementation includes Docker/Docker Compose configuration for containerized deployment.

The containerized setup provides a reproducible environment for:

* FastAPI
* PostgreSQL
* Application/database networking
* Environment-based configuration
* Persistent database storage

Docker is optional when running the API directly against an existing PostgreSQL database.

---

# 🏗️ Architecture Progression

```text
                  TaskCore API
                       │
                       ▼
                FastAPI REST Layer
                       │
          ┌────────────┼────────────┐
          │            │            │
        v1.0          v2.0         v3.0
          │            │            │
     In-Memory       SQLite     PostgreSQL
       Storage     Persistence   Persistence
```

The core architectural principle is:

> **The API contract remains stable while the persistence layer evolves.**

This allows the application to progress from a simple prototype to a more production-oriented backend without redesigning the entire API.

---

# 🎯 Learning Outcomes

This project demonstrates practical experience with:

* REST API development
* FastAPI
* Pydantic validation
* CRUD operations
* HTTP status codes
* SQL queries
* Relational databases
* SQLite
* PostgreSQL
* Database persistence
* Database connection management
* Environment variables
* OpenAPI documentation
* Swagger UI
* Backend architecture
* Docker and Docker Compose fundamentals

---

# 📈 Project Progression

```text
A1 — FastAPI + In-Memory CRUD
              ↓
A2 — FastAPI + SQLite Persistence
              ↓
A3 — FastAPI + PostgreSQL Persistence
              ↓
      Containerized Deployment
```

TaskCore demonstrates the progression from **basic REST API development to persistent database-backed backend engineering**.

---

## 🔮 Future Improvements

Potential future extensions include:

* Authentication and authorization
* Automated testing with Pytest
* Database migrations with Alembic
* SQLAlchemy / SQLModel integration
* Pagination and advanced filtering
* Redis caching
* Background task processing
* CI/CD pipeline
* Cloud deployment

---

## 👩‍💻 Author

**Waariha Asim**

AI Engineer | Backend AI Engineering

GitHub:
https://github.com/Waariha-Asim

---

## 📄 License

This project is intended for educational, portfolio, and learning purposes.
