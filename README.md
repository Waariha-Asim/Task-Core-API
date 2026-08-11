# TaskCore API

A production-style **RESTful Task Management API** built with **FastAPI**, developed progressively across three persistence stages:

**In-Memory → SQLite → PostgreSQL (Neon)**

The project demonstrates REST API design, CRUD operations, validation, SQL-based persistence, database integration, task search, statistics, and interactive OpenAPI documentation.

---

## 🚀 Project Evolution

| Version  | Backend           | Focus                       |
| -------- | ----------------- | --------------------------- |
| **v1.0** | In-Memory         | FastAPI & REST fundamentals |
| **v2.0** | SQLite            | Local persistent storage    |
| **v3.0** | PostgreSQL (Neon) | Cloud database integration  |

The API contract remains consistent while the underlying persistence layer evolves.

---

## 📸 Project Preview

### PostgreSQL v3.0 — API UI

![PostgreSQL API UI](https://github.com/Waariha-Asim/TaskCore-API-SQLite-PostgreSQL/blob/main/TaskCore-API-PostgreSQL-Persistance/Screenshot%202026-08-11%20051056.png)

### GET `/tasks` — In-Memory

![In-Memory GET Tasks](https://github.com/Waariha-Asim/TaskCore-API-SQLite-PostgreSQL/blob/main/Get%20all%20Tasks.png)

### GET `/tasks` — SQLite

![SQLite GET Tasks](https://github.com/Waariha-Asim/TaskCore-API-SQLite-PostgreSQL/blob/main/Task-Core-API-Sqlite-Database/Screenshot%202026-08-11%20031242.png)

### GET `/tasks` — PostgreSQL

![PostgreSQL GET Tasks](https://github.com/Waariha-Asim/TaskCore-API-SQLite-PostgreSQL/blob/main/TaskCore-API-PostgreSQL-Persistance/Screenshot%202026-08-11%20043455.png)

> The API interface remains consistent across all three implementations while storage progresses from **in-memory → SQLite → PostgreSQL**.

---

## ✨ Features

* RESTful CRUD operations
* Task search by title
* Task statistics
* Pydantic request/response validation
* Empty-title validation
* Structured error handling
* Proper HTTP status codes
* Persistent SQLite storage
* PostgreSQL integration using Neon
* Environment-based database configuration
* Interactive Swagger UI and ReDoc
* Automatic OpenAPI documentation

---

## 🛠️ Tech Stack

| Component         | Technology           |
| ----------------- | -------------------- |
| Language          | Python 3.11+         |
| Framework         | FastAPI              |
| Validation        | Pydantic             |
| Server            | Uvicorn              |
| v1.0 Storage      | In-Memory            |
| v2.0 Database     | SQLite               |
| v3.0 Database     | PostgreSQL / Neon    |
| PostgreSQL Driver | Psycopg              |
| Configuration     | python-dotenv        |
| Documentation     | OpenAPI / Swagger UI |

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
├── Get all Tasks.png
└── README.md
```

---

# 🔹 v1.0 — In-Memory API

The initial implementation establishes the core REST API using FastAPI with an in-memory task store.

```text
Client → FastAPI → In-Memory Store
```

Data is temporary and resets when the application restarts.

---

# 🔹 v2.0 — SQLite Database

The second implementation introduces persistent local database storage using SQLite.

```text
Client → FastAPI → SQLite
```

Tasks are stored using SQL queries and remain available after application restarts.

---

# 🔹 v3.0 — PostgreSQL with Neon

The final implementation upgrades the persistence layer to **PostgreSQL hosted on Neon**, introducing cloud-based relational database integration.

```text
Client → FastAPI → Neon PostgreSQL
```

The database connection is configured through the `DATABASE_URL` environment variable.

---

# 🔌 API Reference

| Method   | Endpoint           | Description     |
| -------- | ------------------ | --------------- |
| `GET`    | `/`                | API metadata    |
| `GET`    | `/health`          | Health check    |
| `GET`    | `/tasks`           | List tasks      |
| `GET`    | `/tasks?search=`   | Search tasks    |
| `GET`    | `/tasks/{task_id}` | Get a task      |
| `POST`   | `/tasks`           | Create a task   |
| `PUT`    | `/tasks/{task_id}` | Update a task   |
| `DELETE` | `/tasks/{task_id}` | Delete a task   |
| `GET`    | `/tasks/stats`     | Task statistics |

---

## Example Task

### Create

```json
{
  "title": "Prepare internship portfolio"
}
```

### Response

```json
{
  "id": 4,
  "title": "Prepare internship portfolio",
  "done": false
}
```

### Search

```text
GET /tasks?search=backend
```

### Statistics

```json
{
  "total": 4,
  "completed": 1,
  "pending": 3
}
```

---

## 🔒 Validation & HTTP Status Codes

| Code  | Usage                |
| ----- | -------------------- |
| `200` | Successful GET / PUT |
| `201` | Task created         |
| `204` | Task deleted         |
| `400` | Invalid task data    |
| `404` | Task not found       |

Task titles are validated using Pydantic, including rejection of empty or whitespace-only values.

---

# ⚙️ Getting Started

## Prerequisites

* Python 3.11+
* pip
* Neon PostgreSQL account for v3.0

## Clone

```bash
git clone https://github.com/Waariha-Asim/TaskCore-API-SQLite-PostgreSQL.git
cd TaskCore-API-SQLite-PostgreSQL
```

## Virtual Environment

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

## Dependencies

```bash
pip install fastapi uvicorn psycopg python-dotenv
```

---

# ▶️ Run SQLite Version

```bash
cd Task-Core-API-Sqlite-Database
uvicorn main:app --reload
```

---

# ▶️ Run PostgreSQL Version

```bash
cd TaskCore-API-PostgreSQL-Persistance
```

Create `.env`:

```env
DATABASE_URL=your_neon_postgresql_connection_string
```

Then run:

```bash
uvicorn main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

> **Security:** Never commit your actual `.env` file or database credentials. Use `.env.example` when sharing configuration.

---

# 🏗️ Architecture Progression

```text
A1 — FastAPI + In-Memory
          ↓
A2 — FastAPI + SQLite
          ↓
A3 — FastAPI + Neon PostgreSQL
```

The project demonstrates how a REST API can evolve from a simple prototype into a persistent, cloud-connected backend while keeping the API layer consistent.

---

## 🎯 Learning Outcomes

* FastAPI REST API development
* CRUD architecture
* Pydantic validation
* SQL queries
* SQLite persistence
* PostgreSQL integration
* Neon cloud database
* Database connection management
* Environment variables
* OpenAPI / Swagger documentation
* Backend architecture

---

## 👩‍💻 Author

**Waariha Asim**
AI Engineer | Backend AI Engineering

[GitHub](https://github.com/Waariha-Asim)

---

## 📄 License

For educational, portfolio, and learning purposes.
