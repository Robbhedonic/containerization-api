import os
from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "todos"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )


@app.get("/health")
def health():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return jsonify({"status": "ok", "service": "api"})
    except Exception:
        return jsonify({"status": "error", "service": "api"}), 500


@app.get("/todos")
def list_todos():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT id, title, done, created_at FROM todos ORDER BY id DESC"
            )
            rows = cur.fetchall()
    return jsonify(rows)


@app.post("/todos")
def create_todo():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400

    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO todos (title) VALUES (%s) RETURNING id, title, done, created_at",
                (title,),
            )
            row = cur.fetchone()
            conn.commit()
    return jsonify(row), 201


@app.patch("/todos/<int:todo_id>/toggle")
def toggle_todo(todo_id):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "UPDATE todos SET done = NOT done WHERE id = %s RETURNING id, title, done, created_at",
                (todo_id,),
            )
            row = cur.fetchone()
            conn.commit()

    if not row:
        return jsonify({"error": "todo not found"}), 404
    return jsonify(row)


@app.delete("/todos/<int:todo_id>")
def delete_todo(todo_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
            deleted = cur.rowcount
            conn.commit()

    if deleted == 0:
        return jsonify({"error": "todo not found"}), 404
    return ("", 204)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "3000"))
    app.run(host="0.0.0.0", port=port)
