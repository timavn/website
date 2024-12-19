from flask import Flask, jsonify, request, g
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['DATABASE'] = 'database.db'

def get_db():
    """
    Get database connection.
    This function opens a new database connection if there is none yet for the current application context.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row # allows us to return rows as dict like objects
    return g.db

@app.teardown_appcontext
def close_db(exc):
    """
    Close the database at the end of the request.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    db = get_db()
    cursor = db.execute('SELECT COUNT(*) as total_tasks FROM tasks')
    result = cursor.fetchone()
    total_tasks = result['total_tasks'] if result else 0
    return f'Total tasks: {total_tasks}'

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    db = get_db()
    cursor = db.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    # convert rows to a list of dicts
    tasks_list = [dict(task) for task in tasks]
    return jsonify(tasks_list), 200

@app.route('/api/tasks', methods=['POST'])
def create_task():
    db = get_db()
    data = request.get_json()  # Get the JSON payload
    title = data.get('title')
    description = data.get('description', '')
    deadline = data.get('deadline', '')
    status = data.get('status', 'pending')
    
    now = datetime.utcnow().isoformat()
    db.execute('INSERT INTO tasks (title, description, deadline, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)',
               (title, description, deadline, status, now, now))
    db.commit()

    # Retrieve the newly created task
    cursor = db.execute('SELECT * FROM tasks ORDER BY id DESC LIMIT 1')
    new_task = cursor.fetchone()
    return jsonify(dict(new_task)), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    db = get_db()
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    deadline = data.get('deadline')
    status = data.get('status')

    # Build an UPDATE statement dynamically or just update each field if provided
    now = datetime.utcnow().isoformat()
    db.execute('UPDATE tasks SET title = ?, description = ?, deadline = ?, status = ?, updated_at = ? WHERE id = ?',
               (title, description, deadline, status, now, task_id))
    db.commit()

    # Return the updated task
    cursor = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    updated_task = cursor.fetchone()

    if updated_task:
        return jsonify(dict(updated_task)), 200
    else:
        return jsonify({"error": "Task not found"}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    db.commit()

    # Check if the task is really deleted by trying to select it
    cursor = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    deleted_task = cursor.fetchone()
    if deleted_task:
        # If it still returns a task, something went wrong
        return jsonify({"error": "Failed to delete task"}), 500
    else:
        return jsonify({"message": "Task deleted successfully"}), 200

@app.route('/api/notes', methods=['GET'])
def get_notes():
    db = get_db()
    cursor = db.execute('SELECT * FROM notes')
    notes = cursor.fetchall()
    notes_list = [dict(note) for note in notes]
    return jsonify(notes_list), 200

@app.route('/api/notes', methods=['POST'])
def create_note():
    db = get_db()
    data = request.get_json()
    title = data.get('title')
    content = data.get('content', '')

    now = datetime.utcnow().isoformat()
    db.execute('INSERT INTO notes (title, content, created_at, updated_at) VALUES (?, ?, ?, ?)',
               (title, content, now, now))
    db.commit()

    cursor = db.execute('SELECT * FROM notes ORDER BY id DESC LIMIT 1')
    new_note = cursor.fetchone()
    return jsonify(dict(new_note)), 201

@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    db = get_db()
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    now = datetime.utcnow().isoformat()
    db.execute('UPDATE notes SET title = ?, content = ?, updated_at = ? WHERE id = ?',
               (title, content, now, note_id))
    db.commit()

    cursor = db.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
    updated_note = cursor.fetchone()
    if updated_note:
        return jsonify(dict(updated_note)), 200
    else:
        return jsonify({"error": "Note not found"}), 404

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    db = get_db()
    db.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    db.commit()

    cursor = db.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
    deleted_note = cursor.fetchone()
    if deleted_note:
        return jsonify({"error": "Failed to delete note"}), 500
    else:
        return jsonify({"message": "Note deleted successfully"}), 200    

if __name__ == '__main__':
    app.run(debug=True)