from flask import Flask, request, jsonify
import os
import psycopg2

app = Flask(__name__)

# --- Database Connection Setup ---
def get_db_connection():
    # Retrieve credentials from environment variables set by Kubernetes Secrets/ConfigMap
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        database=os.environ.get("DB_NAME", "edutrack"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "password")
    )
    return conn

# --- API Endpoints ---
@app.route('/health', methods=['GET'])
def health_check():
    """Kubernetes Readiness/Liveness Probe"""
    return jsonify({"status": "OK", "service": "Student Service"}), 200

@app.route('/students', methods=['POST'])
def register_student():
    """Registers a new student"""
    data = request.json
    name = data.get('name')
    email = data.get('email')
    
    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO students (name, email) VALUES (%s, %s) RETURNING id;",
            (name, email)
        )
        student_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Student registered successfully", "id": student_id}), 201
    except Exception as e:
        app.logger.error(f"DB Error: {e}")
        return jsonify({"error": "Failed to register student"}), 500

@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    """Get student profile by ID"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, email FROM students WHERE id = %s;", (id,))
        student = cur.fetchone()
        cur.close()
        conn.close()

        if student:
            return jsonify({
                "id": student[0],
                "name": student[1],
                "email": student[2]
            }), 200
        else:
            return jsonify({"error": "Student not found"}), 404
    except Exception as e:
        app.logger.error(f"DB Error: {e}")
        return jsonify({"error": "Failed to fetch student"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
