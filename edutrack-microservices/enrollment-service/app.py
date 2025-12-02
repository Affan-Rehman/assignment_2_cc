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
    return jsonify({"status": "OK", "service": "Enrollment Service"}), 200

@app.route('/enrollments', methods=['POST'])
def enroll_student():
    """Allows a student to enroll in a course"""
    data = request.json
    student_id = data.get('student_id')
    course_id = data.get('course_id')
    
    if not student_id or not course_id:
        return jsonify({"error": "student_id and course_id are required"}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Optional: Check if student and course exist (would require cross-service calls or shared DB access)
        # For this microservice architecture sharing a DB, we can check foreign keys if constraints exist
        # Or simply try to insert and catch integrity errors
        
        cur.execute(
            "INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s) RETURNING id;",
            (student_id, course_id)
        )
        enrollment_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Student enrolled successfully", "id": enrollment_id}), 201
    except psycopg2.IntegrityError:
        return jsonify({"error": "Enrollment failed. Check if student_id and course_id are valid."}), 400
    except Exception as e:
        app.logger.error(f"DB Error: {e}")
        return jsonify({"error": "Failed to enroll student"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
