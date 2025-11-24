# Lesson 4: Shell Access

Get inside your containers and explore them from within!

## 🎯 Objective

Learn how to access a container's shell to explore files, run commands, and troubleshoot issues. This is essential for debugging and understanding what's inside containers.

## 📝 What You'll Learn

- Getting a shell in a running container (`docker exec`)
- Running interactive containers (`docker run -it`)
- Exploring container filesystems
- Understanding container isolation
- When and why to access container shells

## 🚀 Steps

### Step 1: Start a Container

First, let's run an Nginx container:

```bash
docker run -d --name web nginx
```

### Step 2: Get a Shell in the Running Container

```bash
docker exec -it web bash
```

**Breakdown:**
- `docker exec` = Execute a command in running container
- `-it` = Interactive terminal (lets you type commands)
- `web` = Container name
- `bash` = Command to run (bash shell)

You should now see a prompt like:
```
root@abc123def456:/#
```

You're inside the container!

### Step 3: Explore the Container

Try these commands inside the container:

```bash
# Where am I?
pwd
# Output: /

# What files are here?
ls
# Output: bin  boot  dev  etc  home  lib  ...

# What Linux distribution?
cat /etc/os-release
# Shows Debian (Nginx uses Debian base)

# What processes are running?
ps aux
# Shows nginx processes

# Where is nginx config?
ls /etc/nginx/

# View nginx config
cat /etc/nginx/nginx.conf

# Check nginx files
ls /usr/share/nginx/html/
# This is where the welcome page is!

# View the welcome page
cat /usr/share/nginx/html/index.html
```

### Step 4: Try to Run Commands

```bash
# Some commands work
ls
pwd
cat

# Some might not be installed
curl
# bash: curl: command not found

# Why? Container has minimal tools!
```

### Step 5: Exit the Container

```bash
exit
```

You're back on your host machine!

**Important:** The container is still running. Check:
```bash
docker ps
```

## 🧪 Experiments

### Experiment 1: Modify Container Content

```bash
# Start Nginx
docker run -d -p 8080:80 --name custom-web nginx

# Check the default page
curl http://localhost:8080

# Get shell in container
docker exec -it custom-web bash

# Inside container: Create custom page
echo "<h1>Hello from inside the container!</h1>" > /usr/share/nginx/html/index.html

# Exit
exit

# Check the page now
curl http://localhost:8080
# You see your custom content!

# Clean up
docker rm -f custom-web
```

**Note:** Changes are lost when container is removed!

### Experiment 2: Alpine vs Debian Shells

Different base images use different shells:

```bash
# Ubuntu/Debian uses bash
docker run -it --rm ubuntu bash

# Alpine uses sh (smaller, minimal)
docker run -it --rm alpine sh

# Inside Alpine:
ls
pwd
cat /etc/os-release
exit
```

### Experiment 3: Run Container Directly with Shell

Instead of starting detached then exec-ing, run interactively:

```bash
# Run Ubuntu with bash
docker run -it --rm --name explore ubuntu bash

# You're immediately in the container
# Try commands:
apt update
apt install -y curl
curl --version

# Exit (container auto-removes due to --rm)
exit
```

### Experiment 4: Check Container vs Host Isolation

```bash
# On host, check hostname
hostname

# Run container
docker run -it --rm ubuntu bash

# Inside container, check hostname
hostname
# Different! Each container has its own hostname

# Check network interfaces
ip addr
# Different from host!

exit
```

## 💡 Key Concepts

### exec vs run -it

**docker exec -it (attach to running container):**
```
1. Container already running
2. Execute bash in that container
3. Exit doesn't stop container
```

**docker run -it (start new container):**
```
1. Start new container with bash
2. Container's main process IS bash
3. Exit stops the container
```

### When to Use Shell Access

✅ **Good reasons:**
- Debugging issues
- Checking logs
- Viewing configuration
- Quick testing
- Learning what's inside

❌ **Don't use for:**
- Regular operations (automate instead)
- Permanent changes (use Dockerfile)
- Production containers (use logging/monitoring)

### Container Filesystem

```
Container Filesystem
┌─────────────────────┐
│ /                   │
│ ├── bin/           │ ◄─ Binary executables
│ ├── etc/           │ ◄─ Configuration files
│ ├── usr/           │ ◄─ Application files
│ ├── var/           │ ◄─ Variable data, logs
│ └── ...            │
└─────────────────────┘
     ↕
Host Filesystem
(Isolated!)
```

## 📊 Practical Examples

### Example 1: Troubleshoot Nginx

```bash
# Start nginx
docker run -d --name debug-nginx nginx

# Something's wrong? Check error logs
docker exec debug-nginx cat /var/log/nginx/error.log

# Check if nginx process is running
docker exec debug-nginx ps aux | grep nginx

# Test nginx config
docker exec debug-nginx nginx -t

# Clean up
docker rm -f debug-nginx
```

### Example 2: Install Tools Temporarily

```bash
# Start Ubuntu container
docker run -it --rm ubuntu bash

# Inside container: Install tools
apt update
apt install -y curl vim net-tools

# Use the tools
curl https://api.github.com
ifconfig
vim /tmp/test.txt

# Exit (everything is removed with container)
exit
```

### Example 3: Copy Files Out

```bash
# Start nginx
docker run -d --name copy-test nginx

# View a file
docker exec copy-test cat /etc/nginx/nginx.conf

# Copy file out to host
docker cp copy-test:/etc/nginx/nginx.conf ./nginx.conf

# Now you have it on your host
cat nginx.conf

# Clean up
docker rm -f copy-test
rm nginx.conf
```

## ✅ Practice Challenges

### Challenge 1: Explore Different Images

Get shells in different images and compare:

```bash
# Try each:
docker run -it --rm ubuntu bash
docker run -it --rm alpine sh
docker run -it --rm centos bash
docker run -it --rm debian bash
```

What differences do you notice?

### Challenge 2: Container Forensics

Start a container, make changes, inspect them:

<details>
<summary>Solution</summary>

```bash
# Start container
docker run -d --name forensics nginx

# Create a file
docker exec forensics bash -c "echo 'secret' > /tmp/secret.txt"

# List tmp files
docker exec forensics ls -la /tmp/

# Read the file
docker exec forensics cat /tmp/secret.txt

# Check who created it
docker exec forensics ls -l /tmp/secret.txt

# Clean up
docker rm -f forensics
```
</details>

### Challenge 3: Live Log Watching

Watch nginx logs in real-time:

<details>
<summary>Solution</summary>

```bash
# Terminal 1: Run nginx
docker run -d -p 8080:80 --name live-logs nginx

# Terminal 1: Watch logs
docker exec -it live-logs bash
tail -f /var/log/nginx/access.log

# Terminal 2: Generate traffic
for i in {1..10}; do
  curl http://localhost:8080
  sleep 1
done

# See logs appear in Terminal 1!

# Clean up
docker rm -f live-logs
```
</details>

## 🎯 Common Commands Inside Containers

```bash
# System Information
cat /etc/os-release        # Linux distribution
hostname                   # Container hostname
uname -a                   # Kernel info

# File System
ls -la /                   # List root directory
pwd                        # Current directory
find / -name "*.conf"      # Find config files

# Process Info
ps aux                     # List processes
top                        # Resource usage (if available)

# Networking
ip addr                    # IP addresses (if available)
netstat -tlnp              # Listening ports (if available)

# Logs (common locations)
ls /var/log/
tail -f /var/log/nginx/access.log
```

## ❓ Common Issues

### Issue: "bash: not found"

**Some images use `sh` instead:**
```bash
# Try sh instead of bash
docker exec -it <container> sh

# Or for Alpine-based images:
docker exec -it <container> /bin/sh
```

### Issue: "OCI runtime exec failed"

**Container might not be running:**
```bash
# Check if running
docker ps

# If stopped, start it first
docker start <container>

# Then exec
docker exec -it <container> bash
```

### Issue: Can't install packages

```bash
# Different distros use different package managers:

# Ubuntu/Debian
apt update && apt install <package>

# CentOS/RHEL
yum install <package>

# Alpine
apk add <package>
```

### Issue: Changes disappear after restart

**This is normal!** Changes inside containers are ephemeral.

**Solutions:**
- Use volumes (Part 2)
- Build custom image (Part 3)
- Use Docker Compose with configs (Part 4)

## 📚 What's Next?

You now know how to:
- Get a shell in running containers
- Explore container filesystems
- Run interactive containers
- Debug container issues

**Next Lesson:** [05 - Logs & Inspect →](05-logs-inspect.md)

In the next lesson, you'll learn proper ways to debug containers using logs and inspect commands!

---

**Lesson Duration:** 10 minutes
**Difficulty:** Beginner
**Prerequisites:** Lessons 1-3 completed
**Skills:** Container debugging, exploration
