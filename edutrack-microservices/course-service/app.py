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
    return jsonify({"status": "OK", "service": "Course Service"}), 200

@app.route('/courses', methods=['POST'])
def create_course():
    """Creates a new course"""
    data = request.json
    title = data.get('title')
    description = data.get('description')
    
    if not title:
        return jsonify({"error": "Title is required"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO courses (title, description) VALUES (%s, %s) RETURNING id;",
            (title, description)
        )
        course_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Course created successfully", "id": course_id}), 201
    except Exception as e:
        app.logger.error(f"DB Error: {e}")
        return jsonify({"error": "Failed to create course"}), 500

@app.route('/courses', methods=['GET'])
def list_courses():
    """Lists all available courses"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, title, description FROM courses;")
        courses = cur.fetchall()
        cur.close()
        conn.close()

        course_list = []
        for course in courses:
            course_list.append({
                "id": course[0],
                "title": course[1],
                "description": course[2]
            })

        return jsonify({"courses": course_list}), 200
    except Exception as e:
        app.logger.error(f"DB Error: {e}")
        return jsonify({"error": "Failed to list courses"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
