# Lesson 3: Speedtest Server

Deploy a real-world application - a network speedtest server!

## 🎯 Objective

Run a speedtest server in a Docker container. This is a practical example of deploying a real application that network engineers actually use.

## 📝 What You'll Learn

- Deploying real-world applications
- Working with different Docker images
- Accessing web-based applications
- Understanding why containers are useful for tools

## 🚀 Steps

### Step 1: Find the Image on Docker Hub

First, let's find the speedtest image:

1. Go to [hub.docker.com](https://hub.docker.com)
2. Search for "speedtest"
3. Look for `adolfintel/speedtest` (popular speedtest server)

Or just trust the command below!

### Step 2: Pull the Speedtest Image

```bash
docker pull adolfintel/speedtest
```

This downloads the speedtest server image.

### Step 3: Run the Speedtest Server

```bash
docker run -d \
  -p 8080:80 \
  --name speedtest \
  adolfintel/speedtest
```

**Breakdown:**
- `-d` = Run in background
- `-p 8080:80` = Map port 8080 (your computer) to 80 (container)
- `--name speedtest` = Name it "speedtest"
- `adolfintel/speedtest` = The image to use

### Step 4: Verify It's Running

```bash
docker ps
```

You should see:
```
CONTAINER ID   IMAGE                   COMMAND                  PORTS                  NAMES
abc123...      adolfintel/speedtest    "/init"                 0.0.0.0:8080->80/tcp   speedtest
```

### Step 5: Access the Speedtest Server

Open your browser and go to:
```
http://localhost:8080
```

You should see a speedtest interface with a "Start" button!

### Step 6: Run a Speed Test

1. Click the "Start" button
2. Watch it test your download speed
3. See upload speed
4. View ping/jitter measurements

**Cool, right?** You just deployed a complete web application with one command!

### Step 7: Check the Logs

```bash
docker logs speedtest
```

You'll see the web server logs and any speedtest requests.

### Step 8: Keep It Running or Stop It

**Option A: Keep it running** for later use
```bash
# Just leave it running
docker ps  # Confirm it's still there
```

**Option B: Stop and remove it**
```bash
docker stop speedtest
docker rm speedtest
```

## 🧪 Experiments

### Experiment 1: Run on a Different Port

```bash
# Maybe 8080 is in use, try 9000
docker run -d -p 9000:80 --name speedtest2 adolfintel/speedtest

# Access at http://localhost:9000
```

### Experiment 2: Run Multiple Speedtest Servers

```bash
# Why? Maybe for different network segments
docker run -d -p 8081:80 --name speedtest-net1 adolfintel/speedtest
docker run -d -p 8082:80 --name speedtest-net2 adolfintel/speedtest
docker run -d -p 8083:80 --name speedtest-net3 adolfintel/speedtest

# Access each:
# http://localhost:8081
# http://localhost:8082
# http://localhost:8083

# Clean up
docker stop speedtest-net1 speedtest-net2 speedtest-net3
docker rm speedtest-net1 speedtest-net2 speedtest-net3
```

### Experiment 3: Run Without Naming

```bash
# Let Docker generate a random name
docker run -d -p 7777:80 adolfintel/speedtest

# Check what name it got
docker ps

# You'll see something like "hungry_tesla" or "epic_darwin"
```

## 💡 Key Concepts

### Why Use Docker for This?

**Traditional Setup:**
```
1. Install web server (Apache/Nginx)
2. Install PHP or Node.js
3. Download speedtest code
4. Configure web server
5. Set permissions
6. Troubleshoot errors
7. Update manually
```

**Docker Setup:**
```
1. docker run...
2. Done!
```

### Real-World Use Cases

Network engineers use containers for:
- **Speedtest servers** - Test network performance
- **TFTP servers** - Network device backups
- **Syslog servers** - Log collection
- **SNMP monitors** - Network monitoring
- **NetBox** - Network documentation
- **Ansible AWX** - Automation platform

All of these can run in containers!

### Container Benefits

| Benefit | Explanation |
|---------|-------------|
| **Isolated** | Doesn't mess with your system |
| **Portable** | Runs anywhere Docker runs |
| **Consistent** | Works the same on all machines |
| **Easy updates** | Just pull new image |
| **Quick cleanup** | `docker rm` and it's gone |

## 📊 Comparing Different Images

Let's look at image sizes:

```bash
docker images
```

You might see:
```
REPOSITORY              SIZE
adolfintel/speedtest    ~50MB
nginx                   ~140MB
hello-world             ~13KB
ubuntu                  ~70MB
```

**Smaller = faster to download and deploy!**

## ✅ Real-World Scenario

Imagine you need to troubleshoot network speed between sites:

```bash
# Site A - Deploy speedtest server
ssh user@site-a
docker run -d -p 80:80 --name speedtest adolfintel/speedtest

# Site B - Run speed test
# Open browser: http://site-a-ip

# Done with testing? Remove it
docker rm -f speedtest
```

No installation, no cleanup needed on the server!

## 🎯 Practice Challenges

### Challenge 1: Deploy and Test

1. Run speedtest on port 5555
2. Access it and run a speed test
3. Check the logs
4. Stop and remove

<details>
<summary>Solution</summary>

```bash
# Run it
docker run -d -p 5555:80 --name my-speedtest adolfintel/speedtest

# Test in browser
# http://localhost:5555

# Check logs
docker logs my-speedtest

# Stop and remove
docker stop my-speedtest && docker rm my-speedtest
```
</details>

### Challenge 2: Compare Performance

Run speedtest and nginx side by side, compare memory usage

<details>
<summary>Solution</summary>

```bash
# Run both
docker run -d -p 8080:80 --name speedtest adolfintel/speedtest
docker run -d -p 8081:80 --name nginx nginx

# Check resource usage
docker stats --no-stream

# Clean up
docker stop speedtest nginx
docker rm speedtest nginx
```
</details>

### Challenge 3: Quick Deploy and Test

Run speedtest, test it once, then immediately remove (all in one line)

<details>
<summary>Solution</summary>

```bash
# Run with --rm flag
docker run -d -p 8080:80 --name temp-speedtest --rm adolfintel/speedtest

# Test in browser...

# Stop (this also removes due to --rm)
docker stop temp-speedtest

# Verify it's gone
docker ps -a
```
</details>

## ❓ Common Issues

### Issue: "Port 8080 is already allocated"

**Solution:**
```bash
# Check what's using it
docker ps

# Stop the container
docker stop <container-name>

# Or use different port
docker run -d -p 8888:80 --name speedtest adolfintel/speedtest
```

### Issue: "Can't access http://localhost:8080"

**Troubleshooting checklist:**
```bash
# 1. Is container running?
docker ps

# 2. Check logs for errors
docker logs speedtest

# 3. Verify port mapping
docker ps  # Look at PORTS column

# 4. Try different browser or curl
curl http://localhost:8080

# 5. Check firewall (less likely on localhost)
```

### Issue: Speedtest loads but doesn't work

**Usually a browser issue:**
- Try clearing cache
- Try different browser
- Check browser console for JavaScript errors
- Ensure JavaScript is enabled

## 🔗 Other Useful Network Tools

Try these other network-related containers:

```bash
# TFTP Server
docker run -d -p 69:69/udp --name tftp-server pghalliday/tftp

# Simple HTTP Server
docker run -d -p 8000:80 --name httpd httpd

# Iperf3 (network performance)
docker run -d -p 5201:5201 --name iperf3 networkstatic/iperf3 -s
```

## 📚 What's Next?

You've now:
- Deployed a real application
- Understood practical use cases
- Seen why containers are useful

**Next Lesson:** [04 - Shell Access →](04-shell-access.md)

In the next lesson, you'll learn how to get inside a running container and explore it from the inside!

---

**Lesson Duration:** 15 minutes
**Difficulty:** Beginner
**Prerequisites:** Lessons 1-2 completed
**Skills:** Real-world deployment, network tools
