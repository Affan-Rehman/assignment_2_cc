# EduTrack Microservices

This repository contains the microservices for the EduTrack application.

## Structure

- `/student-service`: Manages student registration and profiles.
- `/course-service`: Manages course creation and listing.
- `/enrollment-service`: Manages student enrollments in courses.
- `/kubernetes-manifests`: Contains Kubernetes YAML files for deployment (Phase 3).

## Prerequisites

- Docker
- Kubernetes (Minikube or GKE)
- PostgreSQL

## Running Locally (Docker)

Each service can be built and run using Docker.

```bash
cd student-service
docker build -t student-service .
docker run -p 8081:8080 -e DB_HOST=host.docker.internal -e DB_PASSWORD=yourpassword student-service
```

Repeat for other services.

## API Endpoints

### Student Service

- `POST /students`: Register a new student.
- `GET /students/<id>`: Get student details.
- `GET /health`: Health check.

### Course Service

- `POST /courses`: Create a new course.
- `GET /courses`: List all courses.
- `GET /health`: Health check.

### Enrollment Service

- `POST /enrollments`: Enroll a student in a course.
- `GET /health`: Health check.
