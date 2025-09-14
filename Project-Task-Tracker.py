from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "tasks.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            project TEXT NOT NULL,
                            task TEXT NOT NULL,
                            status TEXT DEFAULT 'Pending'
                        );''')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute("SELECT * FROM tasks")
        tasks = [{"id": row[0], "project": row[1], "task": row[2], "status": row[3]} for row in cursor.fetchall()]
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO tasks (project, task, status) VALUES (?, ?, ?)",
                     (data['project'], data['task'], data.get('status', 'Pending')))
    return jsonify({"message": "Task added successfully!"}), 201

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("UPDATE tasks SET project=?, task=?, status=? WHERE id=?",
                     (data['project'], data['task'], data['status'], id))
    return jsonify({"message": "Task updated successfully!"})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM tasks WHERE id=?", (id,))
    return jsonify({"message": "Task deleted successfully!"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
