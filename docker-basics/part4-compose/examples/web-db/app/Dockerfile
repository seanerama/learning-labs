FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .

# Install curl for health check
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=10s --timeout=3s --start-period=40s \
  CMD curl --fail http://localhost:5000/health || exit 1

# Run app
CMD ["python", "app.py"]
