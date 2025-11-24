# Lesson 1: Restart Policies

Make your containers resilient and production-ready with restart policies!

## 🎯 Objective

Learn how to configure containers to automatically restart on boot, recover from failures, and behave correctly in production environments.

## 📝 What You'll Learn

- Understanding the 4 restart policies
- Configuring containers to start on boot
- Preventing unwanted auto-restarts
- Updating restart policies on running containers
- Best practices for production deployments

## 🚀 Steps

### Step 1: The Default Behavior (No Restart)

```bash
# Run without restart policy (default: no)
docker run -d --name no-restart nginx

# Check it's running
docker ps

# Stop it
docker stop no-restart

# Check status - it stays stopped
docker ps -a
```

**Result:** Container stays stopped. Won't restart on boot or after crashes.

### Step 2: Always Restart

```bash
# Run with always restart
docker run -d --restart always --name always-restart nginx

# Stop it
docker stop always-restart

# Wait 10 seconds and check
sleep 10
docker ps
```

**Result:** Container automatically restarts even after manual stop!

```bash
# Check how many times it restarted
docker inspect -f '{{.RestartCount}}' always-restart

# Clean up
docker rm -f always-restart
```

### Step 3: Unless Stopped (Recommended for Services)

```bash
# Run with unless-stopped restart policy
docker run -d --restart unless-stopped --name web nginx

# Stop it manually
docker stop web

# Check - it stays stopped
docker ps -a

# Start it again
docker start web

# Now simulate a crash by killing it
docker kill web

# Wait and check - it auto-restarts from the crash!
sleep 3
docker ps
```

**Key difference:** Respects manual stops, but recovers from crashes.

### Step 4: On Failure Only

```bash
# Run with on-failure restart
docker run -d --restart on-failure --name failing-app nginx

# Stop normally (exit code 0) - no restart
docker stop failing-app
docker ps -a  # Shows exited

# Kill it (simulates crash, exit code != 0)
docker start failing-app
docker kill failing-app

# Wait and check - it restarts!
sleep 3
docker ps
```

Clean up:
```bash
docker rm -f failing-app
```

### Step 5: On Failure with Max Retries

```bash
# Create a container that will fail
docker run -d \
  --restart on-failure:3 \
  --name retry-demo \
  alpine sh -c 'exit 1'

# Watch it try to restart 3 times
docker ps -a

# Check restart count
docker inspect -f '{{.RestartCount}}' retry-demo

# After 3 attempts, it gives up
# Clean up
docker rm retry-demo
```

### Step 6: Testing System Reboot Behavior

**Without actual reboot:**

```bash
# Create a service with unless-stopped
docker run -d \
  --restart unless-stopped \
  --name boot-test \
  -p 8080:80 \
  nginx

# Verify it's set correctly
docker inspect -f '{{.HostConfig.RestartPolicy.Name}}' boot-test

# This will start automatically after system reboot
# To test without rebooting:

# Stop Docker daemon
sudo systemctl stop docker

# Start Docker daemon
sudo systemctl start docker

# Check if container auto-started
docker ps | grep boot-test
```

**Result:** Container is running! It survived the Docker daemon restart.

### Step 7: Update Restart Policy on Running Container

```bash
# Create container with no restart
docker run -d --name update-demo nginx

# Check current policy
docker inspect -f '{{.HostConfig.RestartPolicy.Name}}' update-demo

# Update to unless-stopped WITHOUT recreating container
docker update --restart unless-stopped update-demo

# Verify the change
docker inspect -f '{{.HostConfig.RestartPolicy.Name}}' update-demo

# Clean up
docker rm -f update-demo
```

### Step 8: Multiple Containers with Different Policies

```bash
# Production web server - always available
docker run -d \
  --restart unless-stopped \
  --name prod-web \
  -p 8080:80 \
  nginx

# Development container - don't auto-restart
docker run -d \
  --restart no \
  --name dev-web \
  -p 8081:80 \
  nginx

# Background worker - restart on failure, max 5 times
docker run -d \
  --restart on-failure:5 \
  --name worker \
  nginx

# List with restart policies
docker inspect \
  -f '{{.Name}}: {{.HostConfig.RestartPolicy.Name}}' \
  prod-web dev-web worker
```

## 🧪 Practical Scenarios

### Scenario 1: Production Web Server

For a production web server that should always be available:

```bash
docker run -d \
  --name production-web \
  --restart unless-stopped \
  -p 80:80 \
  nginx

# Benefits:
# - Starts on system boot
# - Recovers from crashes
# - Respects manual maintenance stops
```

### Scenario 2: Database Container

For a database that must survive reboots:

```bash
docker run -d \
  --name postgres-db \
  --restart unless-stopped \
  -e POSTGRES_PASSWORD=secret \
  -v db-data:/var/lib/postgresql/data \
  postgres:alpine

# Why unless-stopped?
# - Starts after server reboot
# - Can manually stop for maintenance
# - Automatically recovers from crashes
```

### Scenario 3: One-Time Job

For a container that should retry on failure but not restart otherwise:

```bash
docker run -d \
  --name backup-job \
  --restart on-failure:3 \
  alpine sh -c '
    echo "Running backup..."
    # If this fails, retry up to 3 times
    sleep 2
    echo "Backup complete"
  '

# Check logs
docker logs backup-job

# Check restart count
docker inspect -f '{{.RestartCount}}' backup-job
```

### Scenario 4: Development Environment

For development containers that shouldn't auto-start:

```bash
# Don't start on boot - developer controls when it runs
docker run -d \
  --name dev-api \
  --restart no \
  -p 3000:3000 \
  node:alpine

# Manually start when needed
docker start dev-api
```

## 💡 Key Concepts

### The Four Restart Policies

```
┌─────────────────────────────────────────────────────────┐
│                  Restart Policies                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  no (default)                                          │
│    └─ Never restart automatically                      │
│                                                         │
│  always                                                │
│    └─ Always restart, even after manual stop          │
│                                                         │
│  unless-stopped  (RECOMMENDED)                         │
│    └─ Restart unless manually stopped                 │
│                                                         │
│  on-failure[:max-retries]                              │
│    └─ Restart only on non-zero exit codes             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Decision Tree

```
Do you want auto-start on boot?
│
├─ YES → Is this a service that should always run?
│         │
│         ├─ YES → Should manual stops be permanent?
│         │         │
│         │         ├─ YES → use: unless-stopped ✅
│         │         └─ NO  → use: always
│         │
│         └─ NO  → Is this a job that might fail?
│                   │
│                   ├─ YES → use: on-failure:N
│                   └─ NO  → use: no
│
└─ NO  → use: no (default)
```

### Restart Policy Behavior Table

| Policy | Manual Stop | Crash | Docker Restart | System Reboot |
|--------|-------------|-------|----------------|---------------|
| `no` | Stays stopped | Stays stopped | Stays stopped | Stays stopped |
| `always` | Restarts | Restarts | Restarts | Restarts |
| `unless-stopped` | Stays stopped | Restarts | Restarts | Restarts |
| `on-failure` | Stays stopped | Restarts (N times) | Stays stopped | Stays stopped |

## ✅ Practice Exercises

### Exercise 1: Simulated Production Service

Create a web service that survives failures:

<details>
<summary>Solution</summary>

```bash
# Deploy production web server
docker run -d \
  --name prod-nginx \
  --restart unless-stopped \
  -p 8080:80 \
  nginx

# Test auto-recovery by killing it
docker kill prod-nginx

# Wait and verify it restarted
sleep 3
docker ps | grep prod-nginx

# Test manual stop behavior
docker stop prod-nginx
sleep 5
docker ps -a | grep prod-nginx  # Should show Exited

# Clean up
docker rm prod-nginx
```
</details>

### Exercise 2: Failing Application

Create a container that fails and retries:

<details>
<summary>Solution</summary>

```bash
# Create app that fails 2 times then succeeds
docker run -d \
  --name flaky-app \
  --restart on-failure:5 \
  alpine sh -c '
    if [ -f /tmp/attempt3 ]; then
      echo "Success on attempt 3!"
      sleep infinity
    elif [ -f /tmp/attempt2 ]; then
      touch /tmp/attempt3
      echo "Failed attempt 2"
      exit 1
    elif [ -f /tmp/attempt1 ]; then
      touch /tmp/attempt2
      echo "Failed attempt 1"
      exit 1
    else
      touch /tmp/attempt1
      echo "Failed attempt 0"
      exit 1
    fi
  '

# Check restart count
sleep 10
docker inspect -f '{{.RestartCount}}' flaky-app

# View logs
docker logs flaky-app

# Clean up
docker rm -f flaky-app
```
</details>

### Exercise 3: Update Policy Without Downtime

Change restart policy on a running container:

<details>
<summary>Solution</summary>

```bash
# Start with no restart
docker run -d --name update-test nginx

# Verify current policy
docker inspect -f 'Policy: {{.HostConfig.RestartPolicy.Name}}' update-test

# Update to unless-stopped
docker update --restart unless-stopped update-test

# Verify change
docker inspect -f 'Policy: {{.HostConfig.RestartPolicy.Name}}' update-test

# Container is still running!
docker ps | grep update-test

# Clean up
docker rm -f update-test
```
</details>

## 🔧 Advanced Usage

### Systemd Integration (Linux)

For even more control, combine with systemd:

```bash
# Create a systemd service file
sudo tee /etc/systemd/system/my-container.service << EOF
[Unit]
Description=My Container
After=docker.service
Requires=docker.service

[Service]
Restart=always
ExecStart=/usr/bin/docker start -a my-container
ExecStop=/usr/bin/docker stop my-container

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
sudo systemctl enable my-container.service
sudo systemctl start my-container.service
```

### Monitoring Restart Events

```bash
# Watch container events in real-time
docker events --filter 'event=restart'

# In another terminal, trigger restarts:
docker kill my-container

# See restart events appear!
```

### Restart Policy with Docker Compose

Preview for Part 4:

```yaml
version: '3.8'
services:
  web:
    image: nginx
    restart: unless-stopped
    ports:
      - "80:80"

  worker:
    image: my-worker
    restart: on-failure:3
```

## 📊 Useful One-Liners

```bash
# Check restart policy of all containers
docker ps -q | xargs docker inspect -f '{{.Name}}: {{.HostConfig.RestartPolicy.Name}}'

# Find containers with always restart
docker ps -a --filter 'restart-policy=always' --format '{{.Names}}'

# Count how many times a container restarted
docker inspect -f '{{.RestartCount}}' <container>

# Change all running containers to unless-stopped
docker ps -q | xargs -I {} docker update --restart unless-stopped {}

# List containers that will start on boot
docker ps -a --filter 'restart-policy=always' --filter 'restart-policy=unless-stopped'
```

## ❓ Common Issues

### Issue: Container keeps restarting in a loop

**Symptom:** Container restarts every few seconds

**Debug:**
```bash
# Check logs for errors
docker logs <container>

# Check restart count
docker inspect -f '{{.RestartCount}}' <container>

# Stop the restart loop
docker update --restart no <container>
docker stop <container>
```

**Common causes:**
1. Application crashes immediately on startup
2. Configuration error
3. Missing dependencies

### Issue: Container doesn't start on boot

**Checklist:**
```bash
# 1. Is Docker daemon enabled?
sudo systemctl status docker
sudo systemctl enable docker

# 2. Check restart policy
docker inspect -f '{{.HostConfig.RestartPolicy.Name}}' <container>

# 3. Was container manually stopped?
# unless-stopped respects manual stops

# 4. Check container status
docker ps -a | grep <container>
```

### Issue: "docker update" doesn't seem to work

**Important:** `docker update` changes the policy, but doesn't change current state.

```bash
# Update policy
docker update --restart unless-stopped my-container

# If container is stopped, you need to start it
docker start my-container

# Now it will auto-restart in the future
```

## 🎯 Best Practices

### 1. Use unless-stopped for Services

```bash
# ✅ GOOD - For production services
docker run -d --restart unless-stopped --name api my-api

# ❌ AVOID - always ignores manual stops
docker run -d --restart always --name api my-api
```

### 2. Use no for Development

```bash
# ✅ GOOD - Developer controls when it runs
docker run -d --restart no --name dev-app my-app

# ❌ AVOID - Annoying in development
docker run -d --restart always --name dev-app my-app
```

### 3. Use on-failure for Jobs

```bash
# ✅ GOOD - Retries on failure, then stops
docker run -d --restart on-failure:3 --name backup backup-script

# ❌ AVOID - Job runs forever
docker run -d --restart always --name backup backup-script
```

### 4. Set Restart Policies at Creation

```bash
# ✅ GOOD - Set at creation
docker run -d --restart unless-stopped nginx

# ⚠️ OKAY - But requires extra command
docker run -d nginx
docker update --restart unless-stopped <container>
```

### 5. Document Your Choice

```bash
# Add labels to explain restart policy choice
docker run -d \
  --restart unless-stopped \
  --label "restart-reason=production-service" \
  --name web \
  nginx
```

## 🎉 Lesson Complete!

You now know:

✅ The 4 restart policies and when to use each
✅ How to make containers start on boot
✅ How to prevent unwanted auto-restarts
✅ How to update policies without recreating containers
✅ Best practices for production deployments

### What's Next?

**Next Lesson:** [02 - Environment Variables →](02-environment-vars.md)

Learn how to configure containers using environment variables instead of hard-coded values!

---

**Lesson Duration:** 15 minutes
**Difficulty:** Beginner
**Prerequisites:** Part 1 completed
**Skills:** Production deployment, container resilience
