# Streamlit Hello World App

A simple Streamlit application containerized with Docker.

## Quick Start

### Build the image:
```bash
docker build -t streamlit-hello:v1.0 .
```

### Run the container:
```bash
docker run -d -p 8501:8501 --name hello-streamlit streamlit-hello:v1.0
```

### Access the app:
Open your browser and visit: http://localhost:8501

### View logs:
```bash
docker logs -f hello-streamlit
```

### Stop and remove:
```bash
docker rm -f hello-streamlit
```

## Features

- Interactive counter
- Random number generator
- Personalized greetings
- Sample charts and data visualization
- Progress bar demo
- Responsive design

## Files

- `app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container build instructions
- `.dockerignore` - Files to exclude from build

## Tech Stack

- Python 3.11
- Streamlit 1.29.0
- Pandas 2.1.4
- NumPy 1.26.2
- Docker

## Learn More

See the full lesson: [03-streamlit-hello.md](../03-streamlit-hello.md)
