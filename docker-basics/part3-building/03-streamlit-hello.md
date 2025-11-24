# Lesson 3: Streamlit Hello World

Build and containerize a real web application with Streamlit!

## 🎯 Objective

Create a complete Streamlit web application from scratch, containerize it with Docker, and understand how to build production-ready application images.

## 📝 What You'll Learn

- What Streamlit is and why it's great for quick apps
- Creating a Streamlit application
- Writing a Dockerfile for Python web apps
- Managing Python dependencies
- Running web applications in containers
- Port mapping for web services
- Adding interactivity to your app

## 🚀 Steps

### Step 1: Understanding Streamlit

Streamlit is a Python framework for building web apps quickly. Perfect for:
- Data dashboards
- Internal tools
- Prototypes
- ML/AI demos

Let's build a Hello World app!

### Step 2: Project Setup

```bash
# Create project directory
mkdir -p ~/docker-projects/streamlit-hello
cd ~/docker-projects/streamlit-hello

# We'll create these files:
# - app.py (Streamlit application)
# - requirements.txt (Python dependencies)
# - Dockerfile (Container instructions)
```

### Step 3: Create Streamlit Application

```bash
# Create the Streamlit app
cat > app.py << 'EOF'
import streamlit as st
import datetime

# Page configuration
st.set_page_config(
    page_title="Hello Docker!",
    page_icon="🐳",
    layout="wide"
)

# Title and introduction
st.title("🐳 Hello from Docker!")
st.markdown("### Welcome to your first containerized Streamlit app")

# Sidebar
with st.sidebar:
    st.header("About")
    st.info("This app is running inside a Docker container!")
    st.markdown("---")
    st.markdown("**Tech Stack:**")
    st.markdown("- 🐍 Python")
    st.markdown("- 🎈 Streamlit")
    st.markdown("- 🐳 Docker")

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 Container Info")
    st.write(f"**Current time:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.write("**Python version:** 3.11")
    st.write("**Streamlit version:** " + st.__version__)

with col2:
    st.subheader("✨ Interactive Demo")
    name = st.text_input("Enter your name:", "Docker User")
    if st.button("Say Hello!"):
        st.success(f"Hello, {name}! 👋")
        st.balloons()

# Expandable section
with st.expander("📚 Learn More"):
    st.markdown("""
    **What is Docker?**

    Docker allows you to package applications with all their dependencies
    into standardized units called containers.

    **Benefits:**
    - ✅ Consistent environments
    - ✅ Easy deployment
    - ✅ Scalability
    - ✅ Isolation
    """)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and Docker")
EOF
```

### Step 4: Create Requirements File

```bash
# List Python dependencies
cat > requirements.txt << 'EOF'
streamlit==1.29.0
EOF
```

### Step 5: Test Locally (Optional)

If you have Python installed locally, test before containerizing:

```bash
# Create virtual environment (optional)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py

# Visit http://localhost:8501
# Press Ctrl+C to stop
```

### Step 6: Create Dockerfile

```bash
# Create the Dockerfile
cat > Dockerfile << 'EOF'
# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose Streamlit's default port
EXPOSE 8501

# Configure Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Install curl for health check
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Run Streamlit when container launches
CMD ["streamlit", "run", "app.py"]
EOF
```

### Step 7: Create .dockerignore

```bash
# Exclude unnecessary files from build
cat > .dockerignore << 'EOF'
# Python
__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info
dist
build

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Git
.git/
.gitignore

# Documentation
README.md
*.md
EOF
```

### Step 8: Build the Image

```bash
# Build the Docker image
docker build -t streamlit-hello:v1.0 .

# This will:
# 1. Download Python base image
# 2. Install Streamlit
# 3. Copy your app
# 4. Configure the container

# Check the image
docker images | grep streamlit-hello
```

Output:
```
REPOSITORY        TAG    IMAGE ID       CREATED         SIZE
streamlit-hello   v1.0   abc123def456   10 seconds ago  450MB
```

### Step 9: Run the Container

```bash
# Run Streamlit app in container
docker run -d \
  --name hello-streamlit \
  -p 8501:8501 \
  streamlit-hello:v1.0

# Check it's running
docker ps | grep hello-streamlit

# View logs
docker logs hello-streamlit
```

### Step 10: Access the Application

Open your browser and visit:
```
http://localhost:8501
```

You should see your Streamlit app running! 🎉

Try:
- Entering your name
- Clicking the "Say Hello!" button
- Exploring the sidebar
- Expanding the "Learn More" section

### Step 11: View Container Logs

```bash
# Follow logs in real-time
docker logs -f hello-streamlit

# You'll see Streamlit's output:
# - Server starting
# - Client connections
# - Any Python print statements
```

### Step 12: Update the App

Let's add more features to demonstrate hot-reloading:

```bash
# Stop the current container
docker rm -f hello-streamlit

# Update app.py with more features
cat > app.py << 'EOF'
import streamlit as st
import datetime
import random

# Page configuration
st.set_page_config(
    page_title="Hello Docker!",
    page_icon="🐳",
    layout="wide"
)

# Title
st.title("🐳 Hello from Docker!")
st.markdown("### Your Containerized Streamlit Application")

# Sidebar
with st.sidebar:
    st.header("About")
    st.info("This app is running inside a Docker container!")
    st.markdown("---")

    # Add some controls
    st.header("Settings")
    theme_color = st.selectbox("Choose theme", ["Blue", "Green", "Red", "Purple"])
    show_time = st.checkbox("Show current time", value=True)

    st.markdown("---")
    st.markdown("**Tech Stack:**")
    st.markdown("- 🐍 Python 3.11")
    st.markdown("- 🎈 Streamlit " + st.__version__)
    st.markdown("- 🐳 Docker")

# Main content
if show_time:
    st.info(f"⏰ Current time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Three columns
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📊 Counter")
    if 'counter' not in st.session_state:
        st.session_state.counter = 0

    if st.button("Increment"):
        st.session_state.counter += 1

    st.metric("Count", st.session_state.counter)

with col2:
    st.subheader("🎲 Random Number")
    if st.button("Generate Random"):
        num = random.randint(1, 100)
        st.success(f"Your random number: **{num}**")

with col3:
    st.subheader("✨ Greeting")
    name = st.text_input("Your name:", "Docker User")
    if st.button("Greet Me!"):
        st.success(f"Hello, {name}! 👋")
        st.balloons()

# Tabs
tab1, tab2, tab3 = st.tabs(["📈 Charts", "🗂️ Data", "📚 Docs"])

with tab1:
    st.subheader("Sample Chart")
    import numpy as np
    chart_data = np.random.randn(20, 3)
    st.line_chart(chart_data)

with tab2:
    st.subheader("Sample Data")
    import pandas as pd
    df = pd.DataFrame({
        'Column 1': [1, 2, 3, 4],
        'Column 2': [10, 20, 30, 40]
    })
    st.dataframe(df)

with tab3:
    st.markdown("""
    ### 🐳 Docker Commands Used

    Build the image:
    ```bash
    docker build -t streamlit-hello:v1.0 .
    ```

    Run the container:
    ```bash
    docker run -d -p 8501:8501 --name hello-streamlit streamlit-hello:v1.0
    ```

    View logs:
    ```bash
    docker logs -f hello-streamlit
    ```

    Stop and remove:
    ```bash
    docker rm -f hello-streamlit
    ```
    """)

# Progress bar demo
with st.expander("🔄 See a progress bar"):
    import time
    if st.button("Run Progress"):
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i in range(100):
            progress_bar.progress(i + 1)
            status_text.text(f"Progress: {i + 1}%")
            time.sleep(0.01)

        st.success("Complete!")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using **Streamlit** and **Docker**")
EOF

# Update requirements to include pandas and numpy
cat > requirements.txt << 'EOF'
streamlit==1.29.0
pandas==2.1.4
numpy==1.26.2
EOF

# Rebuild with updated app
docker build -t streamlit-hello:v1.1 .

# Run new version
docker run -d \
  --name hello-streamlit \
  -p 8501:8501 \
  streamlit-hello:v1.1

# Check logs
docker logs hello-streamlit
```

Refresh your browser to see the enhanced app!

## 🧪 Practical Enhancements

### Enhancement 1: Development Mode with Live Reload

```bash
# Create docker-compose.yml for easy development
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  streamlit:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./app.py:/app/app.py
    environment:
      - STREAMLIT_SERVER_RUNON SAVE=true
    restart: unless-stopped
EOF

# Now changes to app.py reload automatically!
docker-compose up -d

# Make a change to app.py and save
# Refresh browser to see changes
```

### Enhancement 2: Environment Variables

```bash
# Update app.py to use environment variables
cat >> app.py << 'EOF'

# Environment info
st.sidebar.markdown("---")
st.sidebar.subheader("Environment")
import os
env = os.getenv('APP_ENV', 'development')
st.sidebar.write(f"Environment: **{env}**")
EOF

# Rebuild
docker build -t streamlit-hello:v1.2 .

# Run with environment variable
docker run -d \
  --name hello-streamlit \
  -p 8501:8501 \
  -e APP_ENV=production \
  streamlit-hello:v1.2
```

### Enhancement 3: Persistent Data with Volumes

```bash
# Update app to save data
cat > app.py << 'EOF'
import streamlit as st
import json
import os

st.title("🐳 Streamlit with Data Persistence")

# Data file path
DATA_FILE = '/app/data/notes.json'

# Ensure directory exists
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

# Load existing notes
def load_notes():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

# Save notes
def save_notes(notes):
    with open(DATA_FILE, 'w') as f:
        json.dump(notes, f)

# Load notes
notes = load_notes()

# Add new note
st.subheader("Add a Note")
new_note = st.text_input("Enter a note:")
if st.button("Save Note"):
    if new_note:
        notes.append({
            'text': new_note,
            'timestamp': str(datetime.datetime.now())
        })
        save_notes(notes)
        st.success("Note saved!")
        st.rerun()

# Display notes
st.subheader("Your Notes")
if notes:
    for i, note in enumerate(notes):
        st.write(f"**{i+1}.** {note['text']}")
        st.caption(f"Added: {note['timestamp']}")
else:
    st.info("No notes yet. Add one above!")

# Clear all notes
if notes and st.button("Clear All Notes"):
    notes = []
    save_notes(notes)
    st.rerun()
EOF

# Rebuild
docker build -t streamlit-hello:v1.3 .

# Run with volume for persistence
docker run -d \
  --name hello-streamlit \
  -p 8501:8501 \
  -v streamlit-data:/app/data \
  streamlit-hello:v1.3

# Notes persist even if container is recreated!
```

## 💡 Key Concepts

### Streamlit in Docker

```
Streamlit Architecture in Container:

┌────────────────────────────────────┐
│  Container                         │
│  ┌──────────────────────────────┐ │
│  │  Streamlit Server            │ │
│  │  (runs on 0.0.0.0:8501)     │ │
│  │  ├─ Auto-reload enabled      │ │
│  │  ├─ WebSocket connection     │ │
│  │  └─ Serves app.py            │ │
│  └──────────────────────────────┘ │
└────────────────────────────────────┘
          ↓ Port mapping (-p 8501:8501)
┌────────────────────────────────────┐
│  Your Browser                      │
│  http://localhost:8501             │
└────────────────────────────────────┘
```

### Dockerfile Best Practices for Web Apps

```dockerfile
# ✅ GOOD: Optimized order
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .          # Copy requirements first
RUN pip install -r requirements.txt  # Install dependencies
COPY app.py .                    # Copy code last (changes often)
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]

# ❌ BAD: Poor caching
FROM python:3.11-slim
WORKDIR /app
COPY . .                         # Copies everything
RUN pip install -r requirements.txt  # Reinstalls every code change
```

### Port Configuration

```bash
# Streamlit default port: 8501
# Container port: 8501
# Host port: Can be anything

# Map to same port
docker run -p 8501:8501 app  # localhost:8501 → container:8501

# Map to different port
docker run -p 3000:8501 app  # localhost:3000 → container:8501

# Bind to specific interface
docker run -p 127.0.0.1:8501:8501 app  # Only localhost access
```

### Health Checks for Web Apps

```dockerfile
# Check if Streamlit is responding
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Benefits:
# - Docker knows if app is healthy
# - Can restart unhealthy containers
# - Load balancers can check health
```

## ✅ Practice Exercises

### Exercise 1: Add a Calculator

Add a simple calculator to the app:

<details>
<summary>Solution</summary>

```python
# Add this to app.py
st.subheader("🔢 Calculator")
calc_col1, calc_col2, calc_col3 = st.columns(3)

with calc_col1:
    num1 = st.number_input("First number", value=0.0)

with calc_col2:
    operation = st.selectbox("Operation", ["+", "-", "*", "/"])

with calc_col3:
    num2 = st.number_input("Second number", value=0.0)

if st.button("Calculate"):
    if operation == "+":
        result = num1 + num2
    elif operation == "-":
        result = num1 - num2
    elif operation == "*":
        result = num1 * num2
    elif operation == "/" and num2 != 0:
        result = num1 / num2
    else:
        result = "Error"

    st.success(f"Result: {result}")
```

Rebuild and run:
```bash
docker build -t streamlit-hello:calculator .
docker run -d -p 8501:8501 --name calc streamlit-hello:calculator
```
</details>

### Exercise 2: File Upload

Add file upload capability:

<details>
<summary>Solution</summary>

```python
# Add to app.py
st.subheader("📁 File Upload")
uploaded_file = st.file_uploader("Choose a file", type=['txt', 'csv', 'json'])

if uploaded_file is not None:
    st.write("Filename:", uploaded_file.name)
    st.write("File size:", uploaded_file.size, "bytes")

    # Read content
    content = uploaded_file.read().decode('utf-8')
    st.text_area("File content:", content, height=200)
```

Rebuild:
```bash
docker build -t streamlit-hello:upload .
docker run -d -p 8501:8501 streamlit-hello:upload
```
</details>

### Exercise 3: Multi-Page App

Create a multi-page Streamlit app:

<details>
<summary>Solution</summary>

```bash
# Create pages directory
mkdir -p pages

# Main app
cat > app.py << 'EOF'
import streamlit as st

st.title("🐳 Multi-Page Streamlit App")
st.write("Use the sidebar to navigate between pages!")
EOF

# Page 1
cat > pages/1_📊_Dashboard.py << 'EOF'
import streamlit as st
import numpy as np

st.title("Dashboard")
st.line_chart(np.random.randn(20, 3))
EOF

# Page 2
cat > pages/2_🔧_Settings.py << 'EOF'
import streamlit as st

st.title("Settings")
st.slider("Volume", 0, 100, 50)
st.selectbox("Theme", ["Light", "Dark"])
EOF

# Update Dockerfile to copy pages
cat > Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY pages/ ./pages/
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
EOF

# Build and run
docker build -t streamlit-multipage .
docker run -d -p 8501:8501 streamlit-multipage
```
</details>

## 🎯 Best Practices

### 1. Use Multi-Stage Build for Production

```dockerfile
# Build stage
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app.py .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

### 2. Configure Streamlit for Production

```bash
# Create .streamlit/config.toml
mkdir -p .streamlit
cat > .streamlit/config.toml << 'EOF'
[server]
port = 8501
address = "0.0.0.0"
headless = true
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
EOF

# Update Dockerfile to include config
COPY .streamlit/config.toml /app/.streamlit/config.toml
```

### 3. Add Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("Streamlit app started")
```

## 🎉 Lesson Complete!

You've successfully:

✅ Created a Streamlit web application
✅ Containerized it with Docker
✅ Built and ran the container
✅ Added interactive features
✅ Learned web app best practices

Your Streamlit app is now:
- Portable (runs anywhere with Docker)
- Isolated (doesn't affect host system)
- Reproducible (same environment every time)
- Easy to deploy (just push the image)

### What's Next?

**Next Lesson:** [04 - Multi-Stage Builds →](04-multi-stage.md)

Learn how to dramatically reduce image size using multi-stage builds!

---

**Lesson Duration:** 30 minutes
**Difficulty:** Intermediate
**Prerequisites:** Lessons 1-2 completed
**Skills:** Web app containerization, Streamlit, Python Docker apps
