# Stage 1: Use a standard Python image
FROM python:3.10-slim
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .

# Expose the port (GKE uses this)
EXPOSE 8080

# Command to run the application
CMD ["python", "app.py"]
