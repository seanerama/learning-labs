# Lesson 3: Volumes

Persist data beyond container lifecycle with Docker volumes!

## 🎯 Objective

Learn how to store data that survives container deletion. Essential for databases, user uploads, logs, and any stateful applications.

## 📝 What You'll Learn

- Understanding ephemeral vs persistent storage
- Creating and managing named volumes
- Using bind mounts for development
- Volume drivers and options
- Backing up and restoring volume data
- Best practices for data persistence

## 🚀 Steps

### Step 1: The Problem - Data Loss

```bash
# Run Nginx and create custom content
docker run -d --name temp-web -p 8080:80 nginx

# Add custom content
docker exec temp-web sh -c 'echo "My custom page" > /usr/share/nginx/html/index.html'

# Verify it works
curl http://localhost:8080

# Remove container
docker rm -f temp-web

# Run new container - data is GONE!
docker run -d --name temp-web -p 8080:80 nginx
curl http://localhost:8080  # Shows default Nginx page

# Clean up
docker rm -f temp-web
```

**Problem:** Container filesystem is ephemeral - data disappears when container is removed!

### Step 2: Solution - Named Volumes

```bash
# Create a named volume
docker volume create web-data

# List volumes
docker volume ls

# Inspect the volume
docker volume inspect web-data
```

Output shows volume location:
```json
[
    {
        "CreatedAt": "2024-01-15T10:30:00Z",
        "Driver": "local",
        "Labels": {},
        "Mountpoint": "/var/lib/docker/volumes/web-data/_data",
        "Name": "web-data",
        "Options": {},
        "Scope": "local"
    }
]
```

### Step 3: Using Named Volumes

```bash
# Run container with volume mounted
docker run -d \
  --name persistent-web \
  -p 8080:80 \
  -v web-data:/usr/share/nginx/html \
  nginx

# Add custom content
docker exec persistent-web sh -c 'echo "Persistent page!" > /usr/share/nginx/html/index.html'

# Verify
curl http://localhost:8080

# Remove container
docker rm -f persistent-web

# Create new container with SAME volume
docker run -d \
  --name persistent-web \
  -p 8080:80 \
  -v web-data:/usr/share/nginx/html \
  nginx

# Data persists!
curl http://localhost:8080
```

**Result:** Data survives container recreation!

### Step 4: Volume Mount Syntax

```bash
# Named volume syntax: volume-name:/container/path
docker run -v myvolume:/data alpine

# Bind mount syntax: /host/path:/container/path
docker run -v /host/dir:/data alpine

# The difference:
# Named volumes: Docker manages location
# Bind mounts: You specify exact host path
```

### Step 5: Bind Mounts (Development)

```bash
# Create a local directory
mkdir -p ~/my-website
echo "<h1>Hello from bind mount!</h1>" > ~/my-website/index.html

# Mount local directory into container
docker run -d \
  --name dev-web \
  -p 8080:80 \
  -v ~/my-website:/usr/share/nginx/html \
  nginx

# Test it
curl http://localhost:8080

# Edit file on host
echo "<h1>Updated from host!</h1>" > ~/my-website/index.html

# Immediately reflected in container!
curl http://localhost:8080

# Clean up
docker rm -f dev-web
```

**Key benefit:** Edit files on your computer, changes appear instantly in container!

### Step 6: Read-Only Volumes

```bash
# Mount volume as read-only
docker run -d \
  --name readonly-web \
  -p 8080:80 \
  -v web-data:/usr/share/nginx/html:ro \
  nginx

# Try to modify - fails!
docker exec readonly-web sh -c 'echo "test" > /usr/share/nginx/html/test.txt'
```

Output:
```
sh: can't create /usr/share/nginx/html/test.txt: Read-only file system
```

```bash
# Clean up
docker rm -f readonly-web
```

### Step 7: Multiple Containers Sharing Volume

```bash
# Create shared volume
docker volume create shared-data

# Container 1 writes data
docker run --rm \
  -v shared-data:/data \
  alpine sh -c 'echo "Data from container 1" > /data/file.txt'

# Container 2 reads data
docker run --rm \
  -v shared-data:/data \
  alpine cat /data/file.txt
```

Output:
```
Data from container 1
```

**Use case:** Multiple containers accessing same data (logs, shared files, etc.)

### Step 8: Database with Persistent Storage

```bash
# Create volume for database
docker volume create postgres-data

# Run PostgreSQL with volume
docker run -d \
  --name postgres-db \
  -e POSTGRES_PASSWORD=secret \
  -v postgres-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:alpine

# Wait for startup
sleep 10

# Create a table and insert data
docker exec postgres-db psql -U postgres -c "
  CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
  );
  INSERT INTO users (name) VALUES ('Alice'), ('Bob'), ('Charlie');
"

# Query data
docker exec postgres-db psql -U postgres -c "SELECT * FROM users;"

# Remove container
docker rm -f postgres-db

# Create new container with SAME volume
docker run -d \
  --name postgres-db \
  -e POSTGRES_PASSWORD=secret \
  -v postgres-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:alpine

sleep 10

# Data is still there!
docker exec postgres-db psql -U postgres -c "SELECT * FROM users;"
```

**Result:** Database survives container recreation!

### Step 9: Volume Management Commands

```bash
# List all volumes
docker volume ls

# Inspect volume details
docker volume inspect postgres-data

# Remove unused volumes
docker volume prune

# Remove specific volume (container must be stopped/removed first)
docker rm -f postgres-db
docker volume rm postgres-data

# Create volume with labels
docker volume create \
  --label environment=production \
  --label app=myapp \
  prod-data

# List volumes by label
docker volume ls --filter label=environment=production
```

## 🧪 Practical Scenarios

### Scenario 1: Development Environment

```bash
# Create project directory
mkdir -p ~/projects/myapp
cd ~/projects/myapp
echo "console.log('Hello from Node.js!');" > app.js

# Run Node.js with bind mount
docker run -it --rm \
  -v "$(pwd):/app" \
  -w /app \
  node:alpine \
  node app.js

# Output: Hello from Node.js!

# Edit app.js on your computer, run again to see changes
echo "console.log('Updated!');" > app.js

docker run -it --rm \
  -v "$(pwd):/app" \
  -w /app \
  node:alpine \
  node app.js

# Output: Updated!
```

### Scenario 2: Backup and Restore

```bash
# Create volume with data
docker volume create backup-demo
docker run --rm \
  -v backup-demo:/data \
  alpine sh -c 'echo "Important data" > /data/important.txt'

# Backup volume to tar file
docker run --rm \
  -v backup-demo:/data \
  -v $(pwd):/backup \
  alpine \
  tar czf /backup/backup.tar.gz -C /data .

# Verify backup exists
ls -lh backup.tar.gz

# Delete volume
docker volume rm backup-demo

# Restore from backup
docker volume create backup-demo
docker run --rm \
  -v backup-demo:/data \
  -v $(pwd):/backup \
  alpine \
  tar xzf /backup/backup.tar.gz -C /data

# Verify data restored
docker run --rm \
  -v backup-demo:/data \
  alpine cat /data/important.txt

# Clean up
docker volume rm backup-demo
rm backup.tar.gz
```

### Scenario 3: Log Aggregation

```bash
# Create logs volume
docker volume create app-logs

# Multiple containers write to same log volume
docker run -d \
  --name app1 \
  -v app-logs:/logs \
  alpine sh -c 'while true; do echo "App1: $(date)" >> /logs/app1.log; sleep 5; done'

docker run -d \
  --name app2 \
  -v app-logs:/logs \
  alpine sh -c 'while true; do echo "App2: $(date)" >> /logs/app2.log; sleep 5; done'

# Wait for logs
sleep 10

# Read logs from separate container
docker run --rm \
  -v app-logs:/logs \
  alpine sh -c 'tail -n 5 /logs/*.log'

# Clean up
docker rm -f app1 app2
docker volume rm app-logs
```

### Scenario 4: Configuration Management

```bash
# Create config directory
mkdir -p ~/my-configs
cat > ~/my-configs/nginx.conf << 'EOF'
server {
    listen 80;
    location / {
        return 200 "Custom Nginx Config!";
        add_header Content-Type text/plain;
    }
}
EOF

# Run Nginx with custom config via bind mount
docker run -d \
  --name custom-nginx \
  -p 8080:80 \
  -v ~/my-configs/nginx.conf:/etc/nginx/conf.d/default.conf:ro \
  nginx

# Test custom config
curl http://localhost:8080

# Clean up
docker rm -f custom-nginx
```

## 💡 Key Concepts

### Volume Types Comparison

| Feature | Named Volume | Bind Mount | tmpfs Mount |
|---------|-------------|------------|-------------|
| **Managed by** | Docker | User | Docker |
| **Location** | /var/lib/docker/volumes/ | Anywhere on host | Memory (RAM) |
| **Syntax** | `-v myvolume:/path` | `-v /host:/path` | `--tmpfs /path` |
| **Portable** | ✅ Yes | ❌ No | N/A |
| **Best for** | Production data | Development | Temp/sensitive data |
| **Survives** | Container deletion | Everything | Container stop |
| **Backup** | Easy with Docker | Manual host backup | Not persistent |

### Volume Lifecycle

```
┌──────────────────────────────────────────────┐
│         Volume Lifecycle                     │
├──────────────────────────────────────────────┤
│                                              │
│  Create → Mount → Use → Unmount → Remove   │
│    │       │       │       │         │      │
│    │       │       │       │         └──→ docker volume rm
│    │       │       │       └─→ docker rm container
│    │       │       └─→ Container reads/writes
│    │       └─→ docker run -v
│    └─→ docker volume create                 │
│                                              │
│  Note: Volume persists after unmount!       │
└──────────────────────────────────────────────┘
```

### When to Use Each Type

```
Named Volumes:
├─ ✅ Production databases
├─ ✅ User uploads
├─ ✅ Application state
└─ ✅ When Docker manages location

Bind Mounts:
├─ ✅ Development (live code reload)
├─ ✅ Config files from host
├─ ✅ Sharing host data
└─ ✅ When you control exact path

tmpfs Mounts:
├─ ✅ Temporary processing
├─ ✅ Sensitive data (not saved to disk)
├─ ✅ High-performance temp storage
└─ ✅ Data that shouldn't persist
```

### Volume Mount Syntax

```bash
# Named volume
-v volume-name:/container/path

# Bind mount (absolute path)
-v /absolute/host/path:/container/path

# Bind mount (relative to current dir)
-v $(pwd)/relative:/container/path

# Read-only
-v volume-name:/container/path:ro

# With options
-v volume-name:/container/path:rw,z

# tmpfs (not a volume, but related)
--tmpfs /container/path

# New syntax (--mount) - more explicit
--mount type=volume,source=myvolume,target=/data
--mount type=bind,source=/host/path,target=/data
--mount type=tmpfs,target=/data
```

## ✅ Practice Exercises

### Exercise 1: Persistent To-Do List

Create a simple persistent to-do list:

<details>
<summary>Solution</summary>

```bash
# Create volume
docker volume create todos

# Add tasks
docker run --rm -v todos:/data alpine sh -c 'echo "Buy milk" >> /data/todos.txt'
docker run --rm -v todos:/data alpine sh -c 'echo "Call mom" >> /data/todos.txt'
docker run --rm -v todos:/data alpine sh -c 'echo "Learn Docker" >> /data/todos.txt'

# Read tasks
docker run --rm -v todos:/data alpine cat /data/todos.txt

# Add more tasks later
docker run --rm -v todos:/data alpine sh -c 'echo "Master volumes" >> /data/todos.txt'

# Tasks persist!
docker run --rm -v todos:/data alpine cat /data/todos.txt

# Clean up
docker volume rm todos
```
</details>

### Exercise 2: MySQL Database with Persistence

Create a MySQL database that survives container recreation:

<details>
<summary>Solution</summary>

```bash
# Create volume
docker volume create mysql-data

# Run MySQL
docker run -d \
  --name mysql-db \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -e MYSQL_DATABASE=testdb \
  -v mysql-data:/var/lib/mysql \
  -p 3306:3306 \
  mysql:8.0

# Wait for startup
sleep 20

# Create table and data
docker exec mysql-db mysql -uroot -prootpass testdb -e "
  CREATE TABLE items (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100));
  INSERT INTO items (name) VALUES ('Item 1'), ('Item 2'), ('Item 3');
  SELECT * FROM items;
"

# Remove container
docker rm -f mysql-db

# Recreate with same volume
docker run -d \
  --name mysql-db \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -v mysql-data:/var/lib/mysql \
  -p 3306:3306 \
  mysql:8.0

sleep 20

# Data still there!
docker exec mysql-db mysql -uroot -prootpass testdb -e "SELECT * FROM items;"

# Clean up
docker rm -f mysql-db
docker volume rm mysql-data
```
</details>

### Exercise 3: Development Workflow

Simulate a development environment:

<details>
<summary>Solution</summary>

```bash
# Create project
mkdir -p ~/temp-project
cd ~/temp-project

# Create simple Python app
cat > app.py << 'EOF'
import time
import datetime

while True:
    print(f"Current time: {datetime.datetime.now()}")
    time.sleep(3)
EOF

# Run with bind mount
docker run -d \
  --name dev-app \
  -v $(pwd):/app \
  -w /app \
  python:alpine \
  python app.py

# View logs
docker logs -f dev-app &
LOGS_PID=$!

# Wait a bit
sleep 10

# Edit file (on host)
cat > app.py << 'EOF'
import time
import datetime

while True:
    print(f"⏰ Updated time: {datetime.datetime.now()}")
    time.sleep(2)
EOF

# Restart container to see changes
docker restart dev-app

# Logs show updated output
sleep 10

# Clean up
kill $LOGS_PID 2>/dev/null
docker rm -f dev-app
cd ~
rm -rf ~/temp-project
```
</details>

## 🔧 Advanced Usage

### Copying Data Between Volumes

```bash
# Create source and destination volumes
docker volume create source-vol
docker volume create dest-vol

# Add data to source
docker run --rm -v source-vol:/data alpine sh -c 'echo "test data" > /data/file.txt'

# Copy from source to destination
docker run --rm \
  -v source-vol:/source:ro \
  -v dest-vol:/dest \
  alpine cp -r /source/. /dest/

# Verify copy
docker run --rm -v dest-vol:/data alpine ls -la /data
```

### Volume Drivers

```bash
# Create volume with specific driver
docker volume create \
  --driver local \
  --opt type=nfs \
  --opt o=addr=192.168.1.100,rw \
  --opt device=:/path/to/share \
  nfs-volume

# Or create tmpfs volume (stored in RAM)
docker run --rm \
  --mount type=tmpfs,destination=/tmp,tmpfs-size=100m \
  alpine df -h /tmp
```

### Volume Labels and Metadata

```bash
# Create volume with metadata
docker volume create \
  --label environment=production \
  --label team=backend \
  --label app=api \
  prod-api-data

# Query by label
docker volume ls --filter label=environment=production

# Inspect labels
docker volume inspect prod-api-data | grep Labels -A 5
```

### Anonymous Volumes

```bash
# Docker creates anonymous volume if path specified but no volume name
docker run -d --name anon-test -v /data alpine sleep 1000

# Find the anonymous volume
docker inspect -f '{{range .Mounts}}{{.Source}}{{end}}' anon-test

# List anonymous volumes
docker volume ls -qf dangling=true

# Remove container and anonymous volume
docker rm -f anon-test
docker volume prune -f
```

## 📊 Useful One-Liners

```bash
# Show all volume mount points for running containers
docker ps -q | xargs docker inspect -f '{{.Name}}:{{range .Mounts}} {{.Type}}={{.Source}}:{{.Destination}}{{end}}'

# Find volumes not used by any container
docker volume ls -qf dangling=true

# Get size of volume (approximation)
docker system df -v | grep "volume name"

# Remove all volumes (DANGEROUS!)
docker volume rm $(docker volume ls -q)

# Backup all volumes
for vol in $(docker volume ls -q); do
  docker run --rm -v $vol:/data -v $(pwd):/backup alpine tar czf /backup/$vol.tar.gz -C /data .
done

# List volumes by size (requires jq)
docker system df -v --format json | jq '.Volumes[] | {name: .Name, size: .Size}'
```

## ❓ Common Issues

### Issue: "No space left on device"

**Cause:** Volume or host filesystem is full

**Debug:**
```bash
# Check Docker disk usage
docker system df -v

# Check specific volume size
docker volume inspect myvolume | grep Mountpoint
# Then check that directory:
sudo du -sh $(docker volume inspect myvolume | grep Mountpoint | cut -d'"' -f4)

# Clean up
docker system prune -a --volumes
```

### Issue: "Volume is in use"

**Can't remove volume:**
```
Error response from daemon: remove myvolume: volume is in use
```

**Solution:**
```bash
# Find which container is using it
docker ps -a --filter volume=myvolume

# Stop and remove the container(s)
docker rm -f <container-name>

# Now remove volume
docker volume rm myvolume
```

### Issue: Bind mount shows empty directory

**Possible causes:**
1. Wrong path syntax
2. Permissions issue
3. Path doesn't exist on host

**Debug:**
```bash
# Check the mount actually worked
docker inspect -f '{{json .Mounts}}' my-container | jq

# Verify host path exists
ls -la /host/path

# Try with absolute path
docker run -v /absolute/path:/data alpine ls /data

# Check permissions
sudo ls -la /host/path
```

### Issue: Volume data disappeared after container restart

**Likely cause:** Used anonymous volume or wrong mount point

**Check:**
```bash
# See actual mounts
docker inspect -f '{{json .Mounts}}' my-container | jq

# If no "Name" field, it's an anonymous volume!
# Create proper named volume instead:
docker volume create mydata
docker run -v mydata:/data my-image
```

## 🎯 Best Practices

### 1. Use Named Volumes for Production

```bash
# ✅ GOOD - Easy to manage and backup
docker volume create prod-db-data
docker run -v prod-db-data:/var/lib/postgresql/data postgres

# ❌ AVOID - Anonymous volumes hard to track
docker run -v /var/lib/postgresql/data postgres
```

### 2. Use Bind Mounts for Development

```bash
# ✅ GOOD - Edit code on host, see changes in container
docker run -v $(pwd):/app -w /app node:alpine npm start

# ❌ AVOID - Bind mounts in production (use named volumes)
```

### 3. Always Specify Volume in Database Containers

```bash
# ✅ GOOD - Data persists
docker run -v pgdata:/var/lib/postgresql/data postgres

# ❌ BAD - Data lost when container removed
docker run postgres
```

### 4. Use Read-Only When Possible

```bash
# ✅ GOOD - Prevents accidental modification
docker run -v config-data:/etc/config:ro my-app

# For configs, secrets, static files
```

### 5. Label Volumes for Organization

```bash
# ✅ GOOD - Easy to find and manage
docker volume create \
  --label app=myapp \
  --label env=prod \
  myapp-prod-data

# Query later:
docker volume ls --filter label=app=myapp
```

### 6. Regular Backups

```bash
# Create backup script
cat > backup-volumes.sh << 'EOF'
#!/bin/bash
BACKUP_DIR=~/backups/docker-volumes
mkdir -p $BACKUP_DIR

for volume in $(docker volume ls -q); do
  echo "Backing up $volume..."
  docker run --rm \
    -v $volume:/source:ro \
    -v $BACKUP_DIR:/backup \
    alpine \
    tar czf /backup/${volume}-$(date +%Y%m%d).tar.gz -C /source .
done
EOF

chmod +x backup-volumes.sh
```

## 🎉 Lesson Complete!

You now know:

✅ How to create and manage named volumes
✅ When to use volumes vs bind mounts
✅ How to persist database data
✅ How to share data between containers
✅ How to backup and restore volumes
✅ Best practices for data persistence

### What's Next?

**Next Lesson:** [04 - Networking →](04-networking.md)

Learn how to create custom networks and enable container-to-container communication!

---

**Lesson Duration:** 25 minutes
**Difficulty:** Intermediate
**Prerequisites:** Lessons 1-2 completed
**Skills:** Data persistence, volume management, backup strategies
