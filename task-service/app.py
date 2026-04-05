from flask import Flask, jsonify, request
import requests
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DB_CONFIG = {
    "host": "postgres",
    "database": "tasksdb",
    "user": "admin", 
    "password": "password"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM tasks ORDER BY id")
        tasks = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([dict(task) for task in tasks])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id",
            (data.get("title", ""), False)
        )
        task_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"id": task_id, "title": data.get("title"), "done": False}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/tasks-with-users", methods=["GET"])
def tasks_with_users():
    try:
        users_resp = requests.get("http://users-service:5001/users", timeout=5)
        users = users_resp.json()
        tasks_resp = get_tasks()
        return jsonify({
            "tasks": tasks_resp.get_json()["tasks"],
            "users": users
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)