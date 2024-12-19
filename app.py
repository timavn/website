from flask import Flask
import sqlite3

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
    cursor = db.execute('SELECT COUNT(*) FROM tasks')
    result = cursor.fetchone()
    total_tasks = result['total_tasks'] if result else 0
    return f'Total tasks: {total_tasks}'

if __name__ == '__main__':
    app.run(debug=True)