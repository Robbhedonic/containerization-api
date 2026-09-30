import os
import requests
from flask import Flask, redirect, render_template_string, request, url_for

app = Flask(__name__)
API_BASE_URL = os.getenv("API_BASE_URL", "http://api:3000")

TEMPLATE = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Todo Microservice</title>
  <style>
    :root {
      --bg: #f6f7fb;
      --surface: #ffffff;
      --ink: #1f2937;
      --brand: #0f766e;
      --muted: #6b7280;
      --danger: #b91c1c;
      --ring: #99f6e4;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Avenir Next", "Segoe UI", sans-serif;
      color: var(--ink);
      background: radial-gradient(circle at top right, #d1fae5 0%, var(--bg) 45%);
      min-height: 100vh;
      display: flex;
      justify-content: center;
      padding: 24px;
    }
    .card {
      width: min(860px, 100%);
      background: var(--surface);
      border-radius: 18px;
      box-shadow: 0 20px 40px rgba(15, 23, 42, 0.08);
      padding: 24px;
    }
    h1 { margin-top: 0; }
    p { color: var(--muted); }
    form.row {
      display: flex;
      gap: 10px;
      margin: 18px 0 24px;
    }
    input[type="text"] {
      flex: 1;
      border: 2px solid #e5e7eb;
      border-radius: 10px;
      padding: 10px 12px;
      font-size: 16px;
      outline: none;
    }
    input[type="text"]:focus { border-color: var(--ring); }
    button {
      border: none;
      border-radius: 10px;
      padding: 10px 14px;
      cursor: pointer;
      font-weight: 600;
      color: white;
      background: var(--brand);
    }
    ul { list-style: none; padding: 0; margin: 0; }
    li {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: #f8fafc;
      border: 1px solid #e5e7eb;
      border-radius: 10px;
      margin-bottom: 8px;
      padding: 10px 12px;
      gap: 10px;
    }
    .title.done { text-decoration: line-through; color: #64748b; }
    .actions { display: flex; gap: 8px; }
    .danger { background: var(--danger); }
    .tiny { padding: 8px 10px; font-size: 13px; }
  </style>
</head>
<body>
  <main class="card">
    <h1>Todo App</h1>
    <p>Web (Python Flask) -> API (Python Flask) -> PostgreSQL</p>

    <form class="row" method="post" action="/todos">
      <input type="text" name="title" placeholder="Nueva tarea" required />
      <button type="submit">Agregar</button>
    </form>

    <ul>
      {% for t in todos %}
      <li>
        <span class="title {% if t.done %}done{% endif %}">{{ t.title }}</span>
        <div class="actions">
          <form method="post" action="/todos/{{ t.id }}/toggle">
            <button class="tiny" type="submit">{{ 'Desmarcar' if t.done else 'Completar' }}</button>
          </form>
          <form method="post" action="/todos/{{ t.id }}/delete">
            <button class="tiny danger" type="submit">Eliminar</button>
          </form>
        </div>
      </li>
      {% endfor %}
    </ul>
  </main>
</body>
</html>
"""


def fetch_todos():
    response = requests.get(f"{API_BASE_URL}/todos", timeout=5)
    response.raise_for_status()
    return response.json()


@app.get("/")
def home():
    try:
        todos = fetch_todos()
    except requests.RequestException:
        todos = []
    return render_template_string(TEMPLATE, todos=todos)


@app.post("/todos")
def add_todo():
    title = (request.form.get("title") or "").strip()
    if title:
        try:
            requests.post(f"{API_BASE_URL}/todos", json={"title": title}, timeout=5)
        except requests.RequestException:
            pass
    return redirect(url_for("home"))


@app.post("/todos/<int:todo_id>/toggle")
def toggle(todo_id):
    try:
        requests.patch(f"{API_BASE_URL}/todos/{todo_id}/toggle", timeout=5)
    except requests.RequestException:
        pass
    return redirect(url_for("home"))


@app.post("/todos/<int:todo_id>/delete")
def remove(todo_id):
    try:
        requests.delete(f"{API_BASE_URL}/todos/{todo_id}", timeout=5)
    except requests.RequestException:
        pass
    return redirect(url_for("home"))


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
