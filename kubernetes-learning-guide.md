# Kubernetes Learning Guide for Network Engineers

## Table of Contents
1. [Introduction](#introduction)
2. [Docker vs Kubernetes](#docker-vs-kubernetes)
3. [Core Kubernetes Concepts](#core-kubernetes-concepts)
4. [Networking in Kubernetes](#networking-in-kubernetes)
5. [Setup: Docker Desktop with Kubernetes](#setup-docker-desktop-with-kubernetes)
6. [Example 1: Hello World with Nginx](#example-1-hello-world-with-nginx)
7. [Example 2: FastAPI Web Application with PostgreSQL](#example-2-fastapi-web-application-with-postgresql)
8. [Example 3: Multi-Cluster Deployment](#example-3-multi-cluster-deployment)
9. [Geographic Distribution and Latency Considerations](#geographic-distribution-and-latency-considerations)
10. [Troubleshooting Commands](#troubleshooting-commands)

---

## Introduction

This guide introduces Kubernetes from a network engineer's perspective, focusing on container orchestration, networking concepts, and practical deployment examples.

**What is Kubernetes?**
- Container orchestration platform
- Manages deployment, scaling, and operations of application containers
- Provides declarative configuration (you specify what you want, not how to do it)
- Automatic failover, self-healing, and load balancing

**Why Kubernetes for Network Engineers?**
- Think of it as "software-defined compute and networking"
- Manages application networking: service discovery, load balancing, ingress
- Handles distributed systems across multiple nodes/regions
- Critical for modern infrastructure and cloud-native applications

---

## Docker vs Kubernetes

### The Relationship

**Docker** and **Kubernetes** are complementary technologies:

| Aspect | Docker | Kubernetes |
|--------|--------|------------|
| **Purpose** | Containerization platform | Container orchestration |
| **Analogy** | The "shipping container" | The "shipping yard manager" |
| **What it does** | Packages apps into containers | Runs and manages containers at scale |
| **Scope** | Single host | Multiple hosts (cluster) |

### The Flow

```
Developer → Dockerfile → Docker Build → Container Image → Kubernetes → Running Pods
```

**Docker's Role:**
- Build container images from Dockerfiles
- Run containers on a single machine
- Provides the container runtime

**Kubernetes' Role:**
- Deploy containers across multiple machines
- Restart containers if they fail
- Load balance traffic between containers
- Handle networking between containers
- Scale up/down based on demand

### Key Distinction

```bash
# Docker: Imperative (tell it what to do)
docker run -d -p 80:80 nginx

# Kubernetes: Declarative (tell it what state you want)
kubectl apply -f deployment.yaml
# "I want 3 nginx pods running, make it happen and keep it that way"
```

---

## Core Kubernetes Concepts

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Control Plane                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  API Server  │  │  Scheduler   │  │  Controller  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────┐                                       │
│  │     etcd     │  (Cluster state database)            │
│  └──────────────┘                                       │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   ┌────▼────┐       ┌────▼────┐      ┌────▼────┐
   │ Node 1  │       │ Node 2  │      │ Node 3  │
   │         │       │         │      │         │
   │ kubelet │       │ kubelet │      │ kubelet │
   │ kube-   │       │ kube-   │      │ kube-   │
   │ proxy   │       │ proxy   │      │ proxy   │
   │         │       │         │      │         │
   │ Pods    │       │ Pods    │      │ Pods    │
   └─────────┘       └─────────┘      └─────────┘
```

### Key Resources

| Resource | Description | Network Engineer Analogy |
|----------|-------------|--------------------------|
| **Pod** | Smallest deployable unit; 1+ containers | A single server/VM |
| **Deployment** | Manages replica sets of Pods | Auto-scaling group |
| **Service** | Stable network endpoint for Pods | Load balancer VIP |
| **Namespace** | Virtual cluster within a cluster | VLAN/VRF |
| **Ingress** | HTTP/HTTPS routing to services | Reverse proxy/Layer 7 LB |
| **ConfigMap** | Configuration data | Configuration files |
| **Secret** | Sensitive data (passwords, keys) | Encrypted credentials |
| **PersistentVolume** | Storage that persists beyond Pod lifecycle | SAN/NAS storage |

### YAML Structure

Kubernetes uses YAML manifests to declare desired state:

```yaml
apiVersion: apps/v1          # API version for this resource type
kind: Deployment             # Type of resource
metadata:                    # Identifying information
  name: my-app
  labels:
    app: my-app
spec:                        # Desired state specification
  replicas: 3               # How many copies to run
  selector:                 # How to find pods to manage
    matchLabels:
      app: my-app
  template:                 # Pod template
    metadata:
      labels:
        app: my-app
    spec:
      containers:           # Container specifications
      - name: my-app
        image: nginx:latest
        ports:
        - containerPort: 80
```

---

## Networking in Kubernetes

### Network Model

Kubernetes has a flat network model with these requirements:
1. **All Pods can communicate** with each other without NAT
2. **All Nodes can communicate** with all Pods without NAT
3. **Pod sees its own IP** the same as others see it (no NAT)

### Service Types

| Type | Description | Use Case | External Access |
|------|-------------|----------|-----------------|
| **ClusterIP** | Internal cluster IP only | Internal microservices | No |
| **NodePort** | Exposes on each Node's IP at a static port | Development/testing | Yes (NodeIP:Port) |
| **LoadBalancer** | Cloud provider load balancer | Production external services | Yes (External IP) |
| **ExternalName** | DNS CNAME record | External service integration | N/A |

### Network Flow Example

```
User Request
    │
    ▼
┌─────────────────┐
│  LoadBalancer   │ (External IP: 203.0.113.10)
│    Service      │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌────────┐
│ Pod 1  │ │ Pod 2  │ (Internal IPs: 10.244.x.x)
│ :8000  │ │ :8000  │
└────────┘ └────────┘
    │         │
    └────┬────┘
         ▼
┌─────────────────┐
│   PostgreSQL    │ (ClusterIP Service)
│     Service     │ (Internal: postgres-service:5432)
└────────┬────────┘
         ▼
┌─────────────────┐
│  PostgreSQL Pod │ (10.244.x.x:5432)
└─────────────────┘
```

### DNS in Kubernetes

Kubernetes provides automatic DNS for services:

```
Service: my-service
Namespace: my-namespace

Full DNS Name: my-service.my-namespace.svc.cluster.local

Within same namespace: my-service
Across namespaces: my-service.my-namespace
```

### Network Policies

Control traffic flow between Pods (similar to firewall rules):

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
spec:
  podSelector:
    matchLabels:
      app: backend
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

---

## Setup: Docker Desktop with Kubernetes

### Prerequisites

1. Windows 11 with WSL2 enabled
2. Docker Desktop installed

### Installation Steps

#### 1. Install Docker Desktop

Download from: https://www.docker.com/products/docker-desktop/

#### 2. Enable WSL2 Backend

- Open Docker Desktop
- Go to **Settings** → **General**
- Check "Use the WSL 2 based engine"
- Click "Apply & Restart"

#### 3. Enable Kubernetes

- Go to **Settings** → **Kubernetes**
- Check "Enable Kubernetes"
- Click "Apply & Restart"
- Wait 5-10 minutes for Kubernetes to start (green indicator appears)

#### 4. Enable WSL Integration

- Go to **Settings** → **Resources** → **WSL Integration**
- Enable integration with your WSL2 distro
- Click "Apply & Restart"

#### 5. Install kubectl in WSL

```bash
# Download kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Make executable and install
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Verify installation
kubectl version --client
```

#### 6. Verify Cluster

```bash
# Check cluster info
kubectl cluster-info

# Get nodes
kubectl get nodes

# Should see:
# NAME             STATUS   ROLES           AGE   VERSION
# docker-desktop   Ready    control-plane   ...   v1.x.x
```

#### 7. Fix Docker Permissions (Optional)

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Restart WSL (from Windows PowerShell)
wsl --shutdown

# Open WSL again and test
docker ps
```

---

## Example 1: Hello World with Nginx

### Quick Deploy

```bash
# Create deployment
kubectl create deployment hello-world --image=nginx:latest

# Expose as a service
kubectl expose deployment hello-world --type=LoadBalancer --port=80

# Check status
kubectl get deployments
kubectl get pods
kubectl get services

# Test (wait for EXTERNAL-IP to show "localhost")
curl http://localhost
```

### Expected Output

```bash
$ kubectl get all
NAME                              READY   STATUS    RESTARTS   AGE
pod/hello-world-8649b9445b-j4sm7  1/1     Running   0          30s

NAME                  TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
service/hello-world   LoadBalancer   10.103.235.4   localhost     80:32317/TCP   15s

NAME                          READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/hello-world   1/1     1            1           30s
```

### Access the Application

- **Browser**: http://localhost
- **curl**: `curl http://localhost`

You should see the "Welcome to nginx!" page.

### Scale the Deployment

```bash
# Scale to 3 replicas
kubectl scale deployment hello-world --replicas=3

# Verify
kubectl get pods

# You'll see 3 pods running
```

### View Logs

```bash
# Get pod name
kubectl get pods

# View logs
kubectl logs <pod-name>

# Follow logs in real-time
kubectl logs -f <pod-name>
```

### Cleanup

```bash
kubectl delete deployment hello-world
kubectl delete service hello-world
```

---

## Example 2: FastAPI Web Application with PostgreSQL

This example demonstrates a multi-tier application with:
- FastAPI web application (Python)
- PostgreSQL database
- Persistent storage
- Environment variables
- Service-to-service communication

### Architecture

```
┌──────────────────────────────────────────────────┐
│           Kubernetes Cluster                     │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │     fastapi-service (LoadBalancer)         │ │
│  │         External: localhost:8000           │ │
│  └──────────────────┬─────────────────────────┘ │
│                     │                            │
│         ┌───────────┴───────────┐                │
│         ▼                       ▼                │
│  ┌─────────────┐         ┌─────────────┐        │
│  │ FastAPI Pod │         │ FastAPI Pod │        │
│  │   (Replica) │         │   (Replica) │        │
│  └──────┬──────┘         └──────┬──────┘        │
│         │                       │                │
│         └───────────┬───────────┘                │
│                     ▼                            │
│  ┌──────────────────────────────────────┐       │
│  │  postgres-service (ClusterIP)        │       │
│  │    Internal: postgres-service:5432   │       │
│  └────────────────┬─────────────────────┘       │
│                   ▼                              │
│  ┌──────────────────────────────────────┐       │
│  │       PostgreSQL Pod                 │       │
│  │                                      │       │
│  │  ┌────────────────────────────────┐ │       │
│  │  │  Persistent Volume (Storage)   │ │       │
│  │  └────────────────────────────────┘ │       │
│  └──────────────────────────────────────┘       │
└──────────────────────────────────────────────────┘
```

### Step 1: Create Project Directory

```bash
mkdir -p ~/fastapi-demo
cd ~/fastapi-demo
```

### Step 2: Create FastAPI Application

Create [main.py](main.py):

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from typing import List, Optional

app = FastAPI(title="FastAPI Demo with PostgreSQL")

# Database connection parameters
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "postgres-service"),
    "database": os.getenv("DB_NAME", "demodb"),
    "user": os.getenv("DB_USER", "demouser"),
    "password": os.getenv("DB_PASSWORD", "demopass"),
    "port": os.getenv("DB_PORT", "5432")
}

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float

def get_db_connection():
    """Create a database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

def init_db():
    """Initialize the database with a table"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL
            )
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    init_db()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "FastAPI + PostgreSQL Demo",
        "status": "running",
        "database": DB_CONFIG["host"]
    }

@app.get("/health")
async def health_check():
    """Check if database is accessible"""
    try:
        conn = get_db_connection()
        conn.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database unhealthy: {str(e)}")

@app.post("/items/", response_model=ItemResponse)
async def create_item(item: Item):
    """Create a new item"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            "INSERT INTO items (name, description, price) VALUES (%s, %s, %s) RETURNING *",
            (item.name, item.description, item.price)
        )
        new_item = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return new_item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/items/", response_model=List[ItemResponse])
async def get_items():
    """Get all items"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM items")
        items = cur.fetchall()
        cur.close()
        conn.close()
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    """Get a specific item by ID"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM items WHERE id = %s", (item_id,))
        item = cur.fetchone()
        cur.close()
        conn.close()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """Delete an item"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM items WHERE id = %s RETURNING id", (item_id,))
        deleted = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if deleted is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"message": f"Item {item_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Step 3: Create Requirements File

Create [requirements.txt](requirements.txt):

```
fastapi==0.115.5
uvicorn[standard]==0.32.1
psycopg2-binary==2.9.10
pydantic==2.10.3
```

### Step 4: Create Dockerfile

Create [Dockerfile](Dockerfile):

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 5: Build Docker Image

```bash
cd ~/fastapi-demo
docker build -t fastapi-demo:latest .
```

**What this does:**
- Builds a Docker image from the Dockerfile
- Tags it as `fastapi-demo:latest`
- Image is now available locally for Kubernetes to use

### Step 6: Create PostgreSQL Deployment

Create [postgres-deployment.yaml](postgres-deployment.yaml):

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  labels:
    app: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:16
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_DB
          value: demodb
        - name: POSTGRES_USER
          value: demouser
        - name: POSTGRES_PASSWORD
          value: demopass
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
          subPath: postgres
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
  labels:
    app: postgres
spec:
  type: ClusterIP
  ports:
  - port: 5432
    targetPort: 5432
  selector:
    app: postgres
```

**Key Networking Concepts:**
- **PersistentVolumeClaim**: Storage that survives pod restarts
- **ClusterIP Service**: Internal-only endpoint at `postgres-service:5432`
- **No external exposure**: Database only accessible within cluster

### Step 7: Create FastAPI Deployment

Create [fastapi-deployment.yaml](fastapi-deployment.yaml):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
  labels:
    app: fastapi-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: fastapi-app
  template:
    metadata:
      labels:
        app: fastapi-app
    spec:
      containers:
      - name: fastapi-app
        image: fastapi-demo:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8000
        env:
        - name: DB_HOST
          value: postgres-service
        - name: DB_NAME
          value: demodb
        - name: DB_USER
          value: demouser
        - name: DB_PASSWORD
          value: demopass
        - name: DB_PORT
          value: "5432"
---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
  labels:
    app: fastapi-app
spec:
  type: LoadBalancer
  ports:
  - port: 8000
    targetPort: 8000
  selector:
    app: fastapi-app
```

**Key Networking Concepts:**
- **imagePullPolicy: Never**: Use local Docker image (not pull from registry)
- **Environment Variables**: Pass configuration to containers
- **DB_HOST: postgres-service**: Uses Kubernetes DNS for service discovery
- **LoadBalancer Service**: Exposes app externally on `localhost:8000`
- **replicas: 2**: Run 2 instances for high availability

### Step 8: Deploy PostgreSQL

```bash
kubectl apply -f postgres-deployment.yaml
```

**Wait for PostgreSQL to be ready:**

```bash
kubectl get pods -w
# Press Ctrl+C when postgres pod shows Running
```

### Step 9: Deploy FastAPI Application

```bash
kubectl apply -f fastapi-deployment.yaml
```

**Verify deployment:**

```bash
kubectl get all
```

Expected output:
```
NAME                               READY   STATUS    RESTARTS   AGE
pod/fastapi-app-xxx                1/1     Running   0          30s
pod/fastapi-app-yyy                1/1     Running   0          30s
pod/postgres-zzz                   1/1     Running   0          2m

NAME                       TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)
service/fastapi-service    LoadBalancer   10.96.x.x       localhost     8000:xxxxx/TCP
service/postgres-service   ClusterIP      10.96.x.x       <none>        5432/TCP
```

### Step 10: Test the Application

**Check root endpoint:**

```bash
curl http://localhost:8000
```

**Check health:**

```bash
curl http://localhost:8000/health
```

**Create an item:**

```bash
curl -X POST http://localhost:8000/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "description": "Dell XPS 13", "price": 1299.99}'
```

**Get all items:**

```bash
curl http://localhost:8000/items/
```

**Get specific item:**

```bash
curl http://localhost:8000/items/1
```

**Delete an item:**

```bash
curl -X DELETE http://localhost:8000/items/1
```

### Step 11: Access Interactive API Documentation

Open in browser:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Step 12: Inspect Resources

**View pod details:**

```bash
kubectl describe pod <pod-name>
```

**View logs:**

```bash
# All FastAPI pods
kubectl logs -l app=fastapi-app --tail=50

# Specific pod
kubectl logs <pod-name>

# Follow logs
kubectl logs -f <pod-name>
```

**Check service endpoints:**

```bash
kubectl get endpoints
```

**Execute commands in a pod:**

```bash
# Open shell in FastAPI pod
kubectl exec -it <fastapi-pod-name> -- /bin/bash

# Test database connection from inside pod
kubectl exec -it <fastapi-pod-name> -- curl http://postgres-service:5432
```

### Cleanup

```bash
kubectl delete -f fastapi-deployment.yaml
kubectl delete -f postgres-deployment.yaml
```

---

## Example 3: Multi-Cluster Deployment

This example demonstrates geographic distribution using multiple independent Kubernetes clusters.

### Architecture

```
┌─────────────────────────────────┐  ┌─────────────────────────────────┐
│       US-East Cluster           │  │       EU-West Cluster           │
│       (localhost:8080)          │  │       (localhost:8081)          │
│                                 │  │                                 │
│  ┌─────────────────────────┐   │  │  ┌─────────────────────────┐   │
│  │ FastAPI Service (LB)    │   │  │  │ FastAPI Service (LB)    │   │
│  └───────────┬─────────────┘   │  │  └───────────┬─────────────┘   │
│              │                  │  │              │                  │
│      ┌───────┴───────┐          │  │      ┌───────┴───────┐          │
│      ▼               ▼          │  │      ▼               ▼          │
│  ┌────────┐     ┌────────┐     │  │  ┌────────┐     ┌────────┐     │
│  │FastAPI │     │FastAPI │     │  │  │FastAPI │     │FastAPI │     │
│  │Pod (US)│     │Pod (US)│     │  │  │Pod (EU)│     │Pod (EU)│     │
│  └────┬───┘     └────┬───┘     │  │  └────┬───┘     └────┬───┘     │
│       └──────┬───────┘          │  │       └──────┬───────┘          │
│              ▼                  │  │              ▼                  │
│  ┌──────────────────────────┐  │  │  ┌──────────────────────────┐  │
│  │  PostgreSQL (US Data)    │  │  │  │  PostgreSQL (EU Data)    │  │
│  └──────────────────────────┘  │  │  └──────────────────────────┘  │
│                                 │  │                                 │
└─────────────────────────────────┘  └─────────────────────────────────┘
       Completely Independent              Completely Independent
```

### Why Multi-Cluster?

**Single Cluster Limitations:**
- Latency < 10ms between nodes required
- Geographic distribution causes instability
- etcd (cluster database) is latency-sensitive

**Multi-Cluster Benefits:**
- Each region has its own independent cluster
- Low latency within each cluster
- Regional data residency
- Fault isolation (one region failure doesn't affect others)

### Latency Requirements

| Component | Recommended Latency | Maximum Tolerable |
|-----------|-------------------|-------------------|
| etcd nodes | < 5ms | ~10ms |
| Control plane to nodes | < 20ms | ~50ms |
| Node to node | < 10ms | ~100ms |
| Multi-cluster | Any | No hard limit |

### Step 1: Install kind (Kubernetes in Docker)

```bash
# Download kind
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.24.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Verify installation
kind version
```

**What is kind?**
- Creates Kubernetes clusters using Docker containers
- Each cluster runs in Docker containers on your machine
- Perfect for testing multi-cluster scenarios locally

### Step 2: Create Cluster Configuration Files

**US-East Cluster:**

```bash
cat > us-east-cluster.yaml <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: us-east
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30080
    hostPort: 8080
    protocol: TCP
- role: worker
EOF
```

**EU-West Cluster:**

```bash
cat > eu-west-cluster.yaml <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: eu-west
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30080
    hostPort: 8081
    protocol: TCP
- role: worker
EOF
```

**Port Mapping Explanation:**
- `containerPort: 30080`: Port inside the cluster
- `hostPort: 8080/8081`: Port on your Windows machine
- This allows accessing each cluster on different ports

### Step 3: Create Both Clusters

```bash
# Create US-East cluster
kind create cluster --config us-east-cluster.yaml

# Create EU-West cluster
kind create cluster --config eu-west-cluster.yaml
```

**What happens:**
- Two independent Kubernetes clusters are created
- Each has its own control plane and worker nodes
- Both are added to your kubeconfig

### Step 4: View Available Clusters

```bash
kubectl config get-contexts
```

Output:
```
CURRENT   NAME               CLUSTER            AUTHINFO
          docker-desktop     docker-desktop     docker-desktop
*         kind-eu-west       kind-eu-west       kind-eu-west
          kind-us-east       kind-us-east       kind-us-east
```

### Step 5: Switch Between Clusters

```bash
# Switch to US-East
kubectl config use-context kind-us-east

# Switch to EU-West
kubectl config use-context kind-eu-west

# Switch back to Docker Desktop
kubectl config use-context docker-desktop
```

**Context = Active Cluster:**
- All `kubectl` commands target the current context
- Think of it like SSH'ing to different servers

### Step 6: Load Docker Image into Both Clusters

kind clusters can't access Docker Desktop images by default, so we load them:

```bash
# Load into US-East
kind load docker-image fastapi-demo:latest --name us-east

# Load into EU-West
kind load docker-image fastapi-demo:latest --name eu-west
```

### Step 7: Create Regional Deployment Manifests

**US-East Deployment:**

```bash
cat > us-east-deployment.yaml <<'EOF'
apiVersion: v1
kind: Namespace
metadata:
  name: fastapi
  labels:
    region: us-east
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: fastapi
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: fastapi
  labels:
    app: postgres
    region: us-east
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
        region: us-east
    spec:
      containers:
      - name: postgres
        image: postgres:16
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_DB
          value: demodb
        - name: POSTGRES_USER
          value: demouser
        - name: POSTGRES_PASSWORD
          value: demopass
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
          subPath: postgres
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
  namespace: fastapi
  labels:
    app: postgres
    region: us-east
spec:
  type: ClusterIP
  ports:
  - port: 5432
    targetPort: 5432
  selector:
    app: postgres
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
  namespace: fastapi
  labels:
    app: fastapi-app
    region: us-east
spec:
  replicas: 2
  selector:
    matchLabels:
      app: fastapi-app
  template:
    metadata:
      labels:
        app: fastapi-app
        region: us-east
    spec:
      containers:
      - name: fastapi-app
        image: fastapi-demo:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8000
        env:
        - name: DB_HOST
          value: postgres-service
        - name: DB_NAME
          value: demodb
        - name: DB_USER
          value: demouser
        - name: DB_PASSWORD
          value: demopass
        - name: DB_PORT
          value: "5432"
        - name: REGION
          value: "us-east"
---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
  namespace: fastapi
  labels:
    app: fastapi-app
    region: us-east
spec:
  type: NodePort
  ports:
  - port: 8000
    targetPort: 8000
    nodePort: 30080
  selector:
    app: fastapi-app
EOF
```

**EU-West Deployment:**

```bash
cat > eu-west-deployment.yaml <<'EOF'
apiVersion: v1
kind: Namespace
metadata:
  name: fastapi
  labels:
    region: eu-west
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: fastapi
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: fastapi
  labels:
    app: postgres
    region: eu-west
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
        region: eu-west
    spec:
      containers:
      - name: postgres
        image: postgres:16
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_DB
          value: demodb
        - name: POSTGRES_USER
          value: demouser
        - name: POSTGRES_PASSWORD
          value: demopass
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
          subPath: postgres
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
  namespace: fastapi
  labels:
    app: postgres
    region: eu-west
spec:
  type: ClusterIP
  ports:
  - port: 5432
    targetPort: 5432
  selector:
    app: postgres
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
  namespace: fastapi
  labels:
    app: fastapi-app
    region: eu-west
spec:
  replicas: 2
  selector:
    matchLabels:
      app: fastapi-app
  template:
    metadata:
      labels:
        app: fastapi-app
        region: eu-west
    spec:
      containers:
      - name: fastapi-app
        image: fastapi-demo:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8000
        env:
        - name: DB_HOST
          value: postgres-service
        - name: DB_NAME
          value: demodb
        - name: DB_USER
          value: demouser
        - name: DB_PASSWORD
          value: demopass
        - name: DB_PORT
          value: "5432"
        - name: REGION
          value: "eu-west"
---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
  namespace: fastapi
  labels:
    app: fastapi-app
    region: eu-west
spec:
  type: NodePort
  ports:
  - port: 8000
    targetPort: 8000
    nodePort: 30080
  selector:
    app: fastapi-app
EOF
```

**Key Differences:**
- Different region labels (`us-east` vs `eu-west`)
- Different `REGION` environment variable
- Same NodePort (30080) but maps to different host ports (8080 vs 8081)

### Step 8: Deploy to US-East Cluster

```bash
# Switch to US-East cluster
kubectl config use-context kind-us-east

# Deploy application
kubectl apply -f us-east-deployment.yaml

# Wait for pods to be ready
kubectl get pods -n fastapi -w
# Press Ctrl+C when all pods show Running
```

### Step 9: Deploy to EU-West Cluster

```bash
# Switch to EU-West cluster
kubectl config use-context kind-eu-west

# Deploy application
kubectl apply -f eu-west-deployment.yaml

# Wait for pods to be ready
kubectl get pods -n fastapi -w
# Press Ctrl+C when all pods show Running
```

### Step 10: Verify Both Clusters

```bash
# Check US-East
kubectl --context kind-us-east get pods -n fastapi

# Check EU-West
kubectl --context kind-eu-west get pods -n fastapi
```

### Step 11: Test Both Clusters

**Test US-East (port 8080):**

```bash
# Root endpoint
curl http://localhost:8080

# Health check
curl http://localhost:8080/health

# Create item in US database
curl -X POST http://localhost:8080/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "US Product", "description": "Sold in USA", "price": 99.99}'

# Get all US items
curl http://localhost:8080/items/
```

**Test EU-West (port 8081):**

```bash
# Root endpoint
curl http://localhost:8081

# Health check
curl http://localhost:8081/health

# Create item in EU database
curl -X POST http://localhost:8081/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "EU Product", "description": "Sold in Europe", "price": 79.99}'

# Get all EU items
curl http://localhost:8081/items/
```

**Verify Data Isolation:**

```bash
# US items (should only have US products)
curl http://localhost:8080/items/

# EU items (should only have EU products)
curl http://localhost:8081/items/
```

Each cluster has its own independent database with its own data.

### Step 12: Query Multiple Clusters Simultaneously

```bash
# Get all pods across both clusters
kubectl --context kind-us-east get pods -n fastapi -o wide
kubectl --context kind-eu-west get pods -n fastapi -o wide

# Get services in both clusters
kubectl --context kind-us-east get services -n fastapi
kubectl --context kind-eu-west get services -n fastapi
```

### Multi-Cluster Management Tools

In production, you'd use tools to coordinate multiple clusters:

**KubeFed (Kubernetes Federation):**
```bash
# Example: Deploy to all clusters with one command
kubefedctl create federateddeployment my-app \
  --placement-clusters us-east,eu-west
```

**ArgoCD (GitOps):**
```yaml
# Example: ArgoCD ApplicationSet for multi-cluster
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: fastapi-multicluster
spec:
  generators:
  - list:
      elements:
      - cluster: us-east
        url: https://us-east.example.com
      - cluster: eu-west
        url: https://eu-west.example.com
  template:
    spec:
      source:
        path: manifests/fastapi
```

### Cleanup

```bash
# Delete both clusters
kind delete cluster --name us-east
kind delete cluster --name eu-west

# Verify clusters are gone
kind get clusters
```

---

## Geographic Distribution and Latency Considerations

### Single Cluster Requirements

A single Kubernetes cluster works best in these conditions:

| Scenario | Latency | Works? |
|----------|---------|--------|
| Same datacenter | < 1ms | ✅ Excellent |
| Same city | 1-5ms | ✅ Good |
| Same region | 5-20ms | ⚠️ Acceptable |
| Cross-region (same continent) | 20-50ms | ❌ Problematic |
| Cross-continent | 50-200ms | ❌ Won't work |

### Why Latency Matters

**etcd (Cluster Database):**
- Uses Raft consensus protocol
- Requires majority of nodes to agree on writes
- High latency = slow writes and potential leader election failures
- Recommended: < 5ms between etcd nodes

**kubelet Heartbeats:**
- Worker nodes send heartbeats every 10 seconds
- If missed, node marked as "NotReady"
- Pods on "NotReady" nodes are evicted
- High latency = false positives and instability

**API Server Communication:**
- All cluster operations go through API server
- Controllers constantly query and update state
- High latency = slow operations and timeouts

### Multi-Cluster Strategies

#### 1. Regional Clusters

Deploy separate clusters in each geographic region:

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   US-East    │  │   US-West    │  │   EU-West    │
│   Cluster    │  │   Cluster    │  │   Cluster    │
└──────────────┘  └──────────────┘  └──────────────┘
       ↓                 ↓                 ↓
  US East Coast    US West Coast     Europe
    Users              Users           Users
```

**Benefits:**
- Low latency for users (route to nearest cluster)
- Data residency compliance (EU data stays in EU)
- Fault isolation (one region failure doesn't affect others)

#### 2. Active-Active with Global Load Balancing

Use DNS-based or Anycast load balancing:

```
                  ┌──────────────────┐
                  │  Global DNS/LB   │
                  │  (Route53, etc)  │
                  └─────────┬────────┘
                            │
         ┌──────────────────┼──────────────────┐
         ▼                  ▼                  ▼
  ┌─────────────┐    ┌─────────────┐   ┌─────────────┐
  │  Cluster 1  │    │  Cluster 2  │   │  Cluster 3  │
  │  (US-East)  │    │  (US-West)  │   │  (EU-West)  │
  └─────────────┘    └─────────────┘   └─────────────┘
```

**Tools:**
- AWS Route53 with geolocation routing
- Google Cloud Load Balancer (global)
- Cloudflare for anycast routing
- Azure Traffic Manager

#### 3. Database Replication Across Regions

Replicate data between regional databases:

```
┌─────────────────┐              ┌─────────────────┐
│   US Cluster    │              │   EU Cluster    │
│                 │              │                 │
│  ┌───────────┐  │              │  ┌───────────┐  │
│  │PostgreSQL │  │◄────────────►│  │PostgreSQL │  │
│  │ (Primary) │  │  Replication │  │ (Replica) │  │
│  └───────────┘  │              │  └───────────┘  │
└─────────────────┘              └─────────────────┘
```

**Options:**
- PostgreSQL streaming replication
- MySQL/MariaDB replication
- MongoDB replica sets with geographic distribution
- Cloud-native databases (Aurora Global, Cosmos DB)

#### 4. Service Mesh for Cross-Cluster Communication

Use service meshes to enable secure communication between clusters:

```
┌──────────────────┐           ┌──────────────────┐
│   Cluster 1      │           │   Cluster 2      │
│                  │           │                  │
│  ┌────────────┐  │  Istio    │  ┌────────────┐  │
│  │  Service A │  │◄─────────►│  │  Service B │  │
│  └────────────┘  │  mTLS     │  └────────────┘  │
└──────────────────┘           └──────────────────┘
```

**Tools:**
- Istio multi-cluster
- Linkerd multi-cluster
- Consul service mesh

### Real-World Architecture Example

**Global E-commerce Platform:**

```
┌─────────────────────────────────────────────────────┐
│            Global Traffic Manager (DNS)             │
│              (Routes based on geography)            │
└─────────────────┬──────────────┬────────────────────┘
                  │              │
        ┌─────────┴────┐    ┌────┴─────────┐
        ▼              ▼    ▼              ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   US-EAST    │  │   US-WEST    │  │   EU-WEST    │
│   Cluster    │  │   Cluster    │  │   Cluster    │
│              │  │              │  │              │
│ Web Tier     │  │ Web Tier     │  │ Web Tier     │
│ API Tier     │  │ API Tier     │  │ API Tier     │
│ Cache        │  │ Cache        │  │ Cache        │
│              │  │              │  │              │
│ PostgreSQL   │  │ PostgreSQL   │  │ PostgreSQL   │
│ (Primary)    │  │ (Replica)    │  │ (Primary-EU) │
└──────┬───────┘  └───────┬──────┘  └──────┬───────┘
       │                  │                 │
       └──────────────────┴─────────────────┘
              Async Database Replication
```

**Characteristics:**
- Each region serves local users
- Low latency within each region (< 5ms)
- Database replication across regions (eventual consistency)
- Failover: If US-East fails, route traffic to US-West

### Best Practices

1. **One Cluster Per Region**
   - Don't stretch a single cluster across continents
   - Keep all nodes in the same datacenter or metro area

2. **Use Multi-Cluster Management**
   - ArgoCD, Flux for GitOps deployment
   - Rancher, Anthos for centralized management
   - KubeFed for federated resources

3. **Implement Global Load Balancing**
   - Route users to nearest cluster
   - Health checks for automatic failover
   - Weighted routing for blue/green deployments

4. **Data Strategy**
   - Decide: Replicate globally or keep regional?
   - Consider data residency regulations (GDPR, etc.)
   - Use appropriate replication (sync vs async)

5. **Monitoring Across Clusters**
   - Centralized logging (ELK, Splunk, Datadog)
   - Distributed tracing (Jaeger, Zipkin)
   - Multi-cluster monitoring (Prometheus Federation, Thanos)

6. **Disaster Recovery**
   - Regular backups of persistent data
   - Test failover procedures
   - Document runbooks for regional failures

---

## Troubleshooting Commands

### Cluster Information

```bash
# View cluster info
kubectl cluster-info

# View all nodes
kubectl get nodes

# Detailed node info
kubectl describe node <node-name>

# Cluster component status
kubectl get componentstatuses
```

### Pod Debugging

```bash
# List all pods
kubectl get pods

# List pods in all namespaces
kubectl get pods --all-namespaces

# Detailed pod information
kubectl describe pod <pod-name>

# Pod logs
kubectl logs <pod-name>

# Follow logs in real-time
kubectl logs -f <pod-name>

# Previous container logs (if crashed)
kubectl logs <pod-name> --previous

# Logs from specific container (multi-container pod)
kubectl logs <pod-name> -c <container-name>

# Execute command in pod
kubectl exec <pod-name> -- <command>

# Interactive shell in pod
kubectl exec -it <pod-name> -- /bin/bash

# Port forward to local machine
kubectl port-forward <pod-name> 8080:8000
```

### Service Debugging

```bash
# List all services
kubectl get services

# Detailed service info
kubectl describe service <service-name>

# Show service endpoints (which pods)
kubectl get endpoints <service-name>

# Test service DNS from within cluster
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup <service-name>

# Test service connectivity
kubectl run -it --rm debug --image=nicolaka/netshoot --restart=Never -- curl http://<service-name>:<port>
```

### Deployment Debugging

```bash
# List deployments
kubectl get deployments

# Detailed deployment info
kubectl describe deployment <deployment-name>

# View deployment history
kubectl rollout history deployment/<deployment-name>

# Check rollout status
kubectl rollout status deployment/<deployment-name>

# Rollback to previous version
kubectl rollout undo deployment/<deployment-name>

# Scale deployment
kubectl scale deployment <deployment-name> --replicas=5
```

### Resource Usage

```bash
# Node resource usage
kubectl top nodes

# Pod resource usage
kubectl top pods

# Resource usage in specific namespace
kubectl top pods -n <namespace>
```

### Events and Logs

```bash
# View cluster events
kubectl get events

# Sort events by timestamp
kubectl get events --sort-by=.metadata.creationTimestamp

# Events for specific namespace
kubectl get events -n <namespace>

# Watch events in real-time
kubectl get events -w
```

### Network Debugging

```bash
# Create debug pod with network tools
kubectl run debug-pod --image=nicolaka/netshoot -it --rm -- /bin/bash

# Inside debug pod, test connectivity:
# ping <pod-ip>
# curl http://<service-name>:<port>
# nslookup <service-name>
# traceroute <external-ip>

# View pod IPs
kubectl get pods -o wide

# View service cluster IPs
kubectl get services -o wide

# Check DNS configuration
kubectl exec <pod-name> -- cat /etc/resolv.conf
```

### Configuration and Context

```bash
# View current context
kubectl config current-context

# List all contexts
kubectl config get-contexts

# Switch context
kubectl config use-context <context-name>

# View kubeconfig
kubectl config view

# Set namespace for current context
kubectl config set-context --current --namespace=<namespace>
```

### Resource Cleanup

```bash
# Delete specific resource
kubectl delete <resource-type> <resource-name>

# Delete resources from file
kubectl delete -f <file.yaml>

# Delete all resources with label
kubectl delete pods -l app=myapp

# Delete all pods in namespace
kubectl delete pods --all -n <namespace>

# Force delete stuck pod
kubectl delete pod <pod-name> --grace-period=0 --force
```

### YAML Validation

```bash
# Dry run to validate YAML
kubectl apply -f <file.yaml> --dry-run=client

# Server-side validation
kubectl apply -f <file.yaml> --dry-run=server

# Show what would be changed
kubectl diff -f <file.yaml>
```

### Common Issues and Solutions

#### Pod is Pending

```bash
# Check events for scheduling issues
kubectl describe pod <pod-name>

# Common causes:
# - Insufficient resources (CPU/memory)
# - Node selector doesn't match any nodes
# - PersistentVolumeClaim not bound
```

#### Pod is CrashLoopBackOff

```bash
# Check logs for errors
kubectl logs <pod-name>
kubectl logs <pod-name> --previous

# Common causes:
# - Application error on startup
# - Missing environment variables
# - Database connection failure
# - Insufficient permissions
```

#### ImagePullBackOff

```bash
# Check events
kubectl describe pod <pod-name>

# Common causes:
# - Image doesn't exist
# - Wrong image name/tag
# - No pull credentials for private registry
# - Network issues accessing registry
```

#### Service Not Accessible

```bash
# Check if service exists
kubectl get service <service-name>

# Check endpoints (are pods selected?)
kubectl get endpoints <service-name>

# If no endpoints, check labels
kubectl get pods --show-labels
kubectl describe service <service-name>  # Check selector

# Test from within cluster
kubectl run debug --image=busybox -it --rm -- wget -O- http://<service-name>:<port>
```

#### DNS Not Working

```bash
# Check CoreDNS pods
kubectl get pods -n kube-system -l k8s-app=kube-dns

# Check CoreDNS logs
kubectl logs -n kube-system -l k8s-app=kube-dns

# Test DNS from pod
kubectl exec <pod-name> -- nslookup kubernetes.default
```

---

## Additional Resources

### Official Documentation
- Kubernetes Documentation: https://kubernetes.io/docs/
- kubectl Cheat Sheet: https://kubernetes.io/docs/reference/kubectl/cheatsheet/
- kind Documentation: https://kind.sigs.k8s.io/

### Networking Deep Dive
- Kubernetes Networking Guide: https://kubernetes.io/docs/concepts/cluster-administration/networking/
- Service Types: https://kubernetes.io/docs/concepts/services-networking/service/
- Network Policies: https://kubernetes.io/docs/concepts/services-networking/network-policies/

### Multi-Cluster Management
- KubeFed: https://github.com/kubernetes-sigs/kubefed
- Istio Multi-Cluster: https://istio.io/latest/docs/setup/install/multicluster/
- ArgoCD: https://argo-cd.readthedocs.io/

### Learning Platforms
- Play with Kubernetes: https://labs.play-with-k8s.com/
- Kubernetes by Example: https://kubernetesbyexample.com/
- Interactive Tutorials: https://kubernetes.io/docs/tutorials/

---

## Glossary

| Term | Definition |
|------|------------|
| **Container** | Lightweight, standalone package of software including code, runtime, and dependencies |
| **Pod** | Smallest deployable unit in Kubernetes; contains one or more containers |
| **Node** | Worker machine (physical or virtual) that runs pods |
| **Cluster** | Set of nodes managed by Kubernetes control plane |
| **Control Plane** | Components that manage the cluster (API server, scheduler, controller manager, etcd) |
| **Deployment** | Declares desired state for pods; manages rolling updates and rollbacks |
| **Service** | Stable network endpoint for accessing pods; provides load balancing |
| **Namespace** | Virtual cluster for resource isolation and multi-tenancy |
| **Label** | Key-value pair for organizing and selecting resources |
| **Selector** | Query to match resources based on labels |
| **ConfigMap** | Store configuration data as key-value pairs |
| **Secret** | Store sensitive information (passwords, tokens, keys) |
| **PersistentVolume (PV)** | Storage resource in the cluster |
| **PersistentVolumeClaim (PVC)** | Request for storage by a pod |
| **Ingress** | HTTP/HTTPS routing rules for external access to services |
| **kubectl** | Command-line tool for interacting with Kubernetes |
| **kind** | Tool for running local Kubernetes clusters using Docker |
| **etcd** | Distributed key-value store used as cluster database |

---

## Summary

This guide covered:

1. **Docker vs Kubernetes**: Understanding the relationship and roles
2. **Core Concepts**: Pods, Services, Deployments, Namespaces
3. **Networking**: Service types, DNS, network flow
4. **Setup**: Docker Desktop with Kubernetes on Windows 11/WSL2
5. **Example 1**: Simple nginx hello world
6. **Example 2**: Multi-tier FastAPI + PostgreSQL application
7. **Example 3**: Multi-cluster deployment simulating geographic distribution
8. **Latency Considerations**: Single vs multi-cluster architecture
9. **Troubleshooting**: Essential commands for debugging

**Key Takeaways for Network Engineers:**

- Kubernetes is "infrastructure as code" for container orchestration
- Services provide stable network endpoints (like VIPs)
- Namespaces provide isolation (like VLANs/VRFs)
- Single clusters work within low-latency regions (< 10ms)
- Multi-cluster is required for geographic distribution
- DNS and service discovery are built-in
- Declarative configuration means you specify desired state, not procedural steps

Start with simple deployments and gradually move to complex multi-tier and multi-cluster scenarios as you build confidence.

---

**Version**: 1.0
**Last Updated**: 2025-11-20
**Target Audience**: Network Engineers learning Kubernetes
