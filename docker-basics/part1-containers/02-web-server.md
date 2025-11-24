# Lesson 2: Web Server

Run your first real application - an Nginx web server!

## 🎯 Objective

Run an Nginx web server in a Docker container and access it from your browser. Learn about port mapping and detached mode.

## 📝 What You'll Learn

- Running containers in detached mode (`-d`)
- Port mapping (`-p`)
- Accessing containerized services
- Stopping and removing running containers
- Understanding foreground vs background execution

## 🚀 Steps

### Step 1: Pull the Nginx Image

```bash
docker pull nginx
```

This downloads the official Nginx image from Docker Hub.

### Step 2: Run Nginx in Foreground (Don't Do This!)

First, let's see what happens without detached mode:

```bash
docker run -p 8080:80 nginx
```

**What happens:**
- Your terminal is blocked
- You see Nginx access logs
- You can't type new commands
- Press `Ctrl+C` to stop (this stops the container)

**This is NOT what we want for a web server!**

### Step 3: Run Nginx in Detached Mode (The Right Way)

```bash
docker run -d -p 8080:80 --name my-nginx nginx
```

**Breakdown:**
- `-d` = Detached mode (runs in background)
- `-p 8080:80` = Map port 8080 on host to port 80 in container
- `--name my-nginx` = Give it a friendly name
- `nginx` = The image to use

Output:
```
abc123def456...
```

That long string is the container ID!

### Step 4: Verify It's Running

```bash
docker ps
```

Output:
```
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS                  NAMES
abc123def456   nginx     "/docker-entrypoint.…"   10 seconds ago   Up 9 seconds    0.0.0.0:8080->80/tcp   my-nginx
```

**Key information:**
- **STATUS:** Up 9 seconds (it's running!)
- **PORTS:** 0.0.0.0:8080->80/tcp (port mapping)
- **NAMES:** my-nginx (the name we gave it)

### Step 5: Access the Web Server

#### Option A: Using a Browser

Open your browser and go to:
```
http://localhost:8080
```

You should see the Nginx welcome page!

#### Option B: Using curl

```bash
curl http://localhost:8080
```

You'll see the HTML of the welcome page.

### Step 6: View Real-Time Logs

```bash
docker logs -f my-nginx
```

- `-f` = Follow (like `tail -f`)
- Now refresh your browser
- You'll see access logs appear in real-time!
- Press `Ctrl+C` to stop following (container keeps running)

### Step 7: Stop the Container

```bash
docker stop my-nginx
```

### Step 8: Verify It Stopped

```bash
docker ps        # Not in running containers
docker ps -a     # Shows in all containers with "Exited" status
```

### Step 9: Start It Again

```bash
docker start my-nginx
```

Check if it's running:
```bash
docker ps
curl http://localhost:8080
```

It's back!

### Step 10: Stop and Remove

```bash
# Stop it
docker stop my-nginx

# Remove it
docker rm my-nginx

# Verify it's gone
docker ps -a
```

## 🧪 Experiments

### Experiment 1: Run on Different Port

```bash
# Run on port 9000
docker run -d -p 9000:80 --name nginx-9000 nginx

# Access it
curl http://localhost:9000

# Clean up
docker stop nginx-9000 && docker rm nginx-9000
```

### Experiment 2: Run Multiple Nginx Containers

```bash
# Run three on different ports
docker run -d -p 8080:80 --name web1 nginx
docker run -d -p 8081:80 --name web2 nginx
docker run -d -p 8082:80 --name web3 nginx

# Test all three
curl http://localhost:8080
curl http://localhost:8081
curl http://localhost:8082

# List them
docker ps

# Clean up
docker stop web1 web2 web3
docker rm web1 web2 web3
```

### Experiment 3: One-liner Run and Remove

```bash
# The --rm flag automatically removes container when stopped
docker run -d -p 8080:80 --name temp-nginx --rm nginx

# Stop it (this also removes it due to --rm)
docker stop temp-nginx

# Check - it's already gone!
docker ps -a
```

## 💡 Key Concepts

### Port Mapping Explained

```
Your Computer                     Container
┌─────────────┐                 ┌──────────┐
│             │                 │          │
│  Port 8080  │ ◄────────────► │  Port 80 │
│  (Host)     │                 │          │
└─────────────┘                 └──────────┘

Command: -p 8080:80
         └┬─┘ └─┬┘
          │     └─ Container port (Nginx listens on 80)
          └─────── Host port (You access via 8080)
```

### Foreground vs Detached

**Foreground (`docker run`):**
```
Terminal ──► Container
  (blocked, shows output)
```

**Detached (`docker run -d`):**
```
Terminal           Container
  (free)    ◄────►  (background)
                    Use docker logs
```

### Container Lifecycle

```
Run (-d)
   │
   ▼
Running ──stop──► Stopped ──start──► Running
   │                  │
   └──────────────────┴─────rm─────► Removed
```

## 📊 Command Reference

```bash
# Run in detached mode with port mapping
docker run -d -p 8080:80 --name my-nginx nginx

# View running containers
docker ps

# View all containers
docker ps -a

# Stop a container
docker stop my-nginx

# Start a stopped container
docker start my-nginx

# Restart a container
docker restart my-nginx

# View logs
docker logs my-nginx

# Follow logs in real-time
docker logs -f my-nginx

# Remove a stopped container
docker rm my-nginx

# Stop and remove in one command
docker rm -f my-nginx
```

## ✅ Verification

Test your understanding:

```bash
# 1. Run Nginx on port 7777
docker run -d -p 7777:80 --name test-nginx nginx

# 2. Access it in browser
# http://localhost:7777

# 3. View logs
docker logs test-nginx

# 4. Stop it
docker stop test-nginx

# 5. Remove it
docker rm test-nginx
```

## ❓ Common Issues

### Issue: "Port is already allocated"

**Cause:** Another container (or process) is using that port.

**Solution:**
```bash
# Find what's using the port
docker ps

# Stop the container using that port
docker stop <container-name>

# Or use a different port
docker run -d -p 8081:80 nginx
```

### Issue: "Cannot access http://localhost:8080"

**Checklist:**
1. Is container running? `docker ps`
2. Is port mapping correct? Check PORTS column
3. Using correct port in URL?
4. Firewall blocking the port?

**Debug:**
```bash
# Check if container is running
docker ps

# Check logs for errors
docker logs my-nginx

# Try curl instead of browser
curl http://localhost:8080
```

### Issue: Container stops immediately

**Check logs:**
```bash
docker logs my-nginx
```

Usually shows the error message.

## 🎯 Practice Challenges

### Challenge 1: Custom Port Setup

Run Nginx on port 3333 with name "challenge1"

<details>
<summary>Solution</summary>

```bash
docker run -d -p 3333:80 --name challenge1 nginx
curl http://localhost:3333
docker stop challenge1 && docker rm challenge1
```
</details>

### Challenge 2: Multiple Servers

Run 5 Nginx containers on ports 8081-8085

<details>
<summary>Solution</summary>

```bash
for port in {8081..8085}; do
  docker run -d -p ${port}:80 --name nginx-${port} nginx
done

# Test
for port in {8081..8085}; do
  curl http://localhost:${port}
done

# Clean up
for port in {8081..8085}; do
  docker stop nginx-${port} && docker rm nginx-${port}
done
```
</details>

### Challenge 3: Log Monitoring

Run Nginx and watch logs while you access it

<details>
<summary>Solution</summary>

```bash
# Terminal 1
docker run -d -p 8080:80 --name log-test nginx
docker logs -f log-test

# Terminal 2
for i in {1..10}; do
  curl http://localhost:8080 > /dev/null
  sleep 1
done

# Clean up
docker stop log-test && docker rm log-test
```
</details>

## 📚 What's Next?

You can now:
- Run containers in detached mode
- Map ports to access services
- Manage container lifecycle
- View logs

**Next Lesson:** [03 - Speedtest Server →](03-speedtest.md)

In the next lesson, you'll deploy a real-world application - a network speedtest server!

---

**Lesson Duration:** 15 minutes
**Difficulty:** Beginner
**Prerequisites:** Lesson 1 completed
