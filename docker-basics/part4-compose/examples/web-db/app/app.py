from flask import Flask, jsonify
import psycopg2
import os
import time

app = Flask(__name__)

def get_db_connection():
    """Connect to PostgreSQL database"""
    max_retries = 5
    retry_count = 0

    while retry_count < max_retries:
        try:
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST', 'database'),
                database=os.getenv('DB_NAME', 'myapp'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', 'secret')
            )
            return conn
        except psycopg2.OperationalError:
            retry_count += 1
            time.sleep(2)

    raise Exception("Could not connect to database")

@app.route('/')
def index():
    return jsonify({
        "message": "Hello from Flask!",
        "status": "running",
        "database": "connected"
    })

@app.route('/health')
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "healthy"}), 200
    except:
        return jsonify({"status": "unhealthy"}), 500

@app.route('/init')
def init_db():
    """Initialize database with sample table"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Create table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS visits (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Insert visit
        cur.execute('INSERT INTO visits (timestamp) VALUES (CURRENT_TIMESTAMP)')

        # Get total visits
        cur.execute('SELECT COUNT(*) FROM visits')
        count = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "message": "Database initialized",
            "total_visits": count
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
