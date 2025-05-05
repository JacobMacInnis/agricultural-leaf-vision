# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY backend/server.py .

# Run app
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
