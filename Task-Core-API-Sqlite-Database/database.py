import sqlite3


DATABASE = "tasks.db"


def get_connection():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection


def create_table():

    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
        """
    )

    connection.commit()

    existing_tasks = connection.execute(
        "SELECT COUNT(*) FROM tasks"
    ).fetchone()[0]

    if existing_tasks == 0:

        connection.executemany(
            """
            INSERT INTO tasks (title, done)
            VALUES (?, ?)
            """,
            [
                (
                    "Complete Backend AI assignment",
                    False
                ),
                (
                    "Review FastAPI documentation",
                    True
                ),
                (
                    "Push project to GitHub",
                    False
                ),
            ],
        )

        connection.commit()

    connection.close()
