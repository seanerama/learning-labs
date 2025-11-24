# Lesson 5: Logs & Inspect

Master container debugging with logs and inspect commands!

## 🎯 Objective

Learn the proper ways to debug and monitor containers using Docker's built-in commands. Understanding logs and inspect is crucial for troubleshooting production issues.

## 📝 What You'll Learn

- Viewing container logs (`docker logs`)
- Following logs in real-time
- Inspecting container details (`docker inspect`)
- Monitoring container stats (`docker stats`)
- Debugging common container issues
- Best practices for logging

## 🚀 Steps

### Step 1: Viewing Basic Logs

```bash
# Start Nginx
docker run -d -p 8080:80 --name log-demo nginx

# View logs
docker logs log-demo
```

You'll see Nginx startup messages.

### Step 2: Generate Some Activity

```bash
# Make some requests
curl http://localhost:8080
curl http://localhost:8080
curl http://localhost:8080

# View logs again
docker logs log-demo
```

Now you see access logs!

### Step 3: Follow Logs in Real-Time

```bash
# Follow logs (like tail -f)
docker logs -f log-demo
```

The terminal is now waiting for new log entries.

In another terminal:
```bash
# Generate traffic
for i in {1..5}; do
  curl http://localhost:8080
  sleep 1
done
```

Watch the logs appear in real-time! Press `Ctrl+C` to stop following.

### Step 4: View Last N Lines

```bash
# See last 10 lines
docker logs --tail 10 log-demo

# See last 3 lines
docker logs --tail 3 log-demo
```

### Step 5: View Logs with Timestamps

```bash
# Add timestamps to each log line
docker logs -t log-demo
```

Output:
```
2025-01-15T10:30:45.123456789Z /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
2025-01-15T10:30:45.234567890Z 10.0.0.1 - - [15/Jan/2025:10:30:45 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.68.0"
```

### Step 6: Combine Options

```bash
# Last 5 lines with timestamps, then follow
docker logs -t --tail 5 -f log-demo

# Ctrl+C to stop
```

## 🔍 Inspecting Containers

### Step 7: Basic Inspect

```bash
docker inspect log-demo
```

This returns a HUGE JSON with ALL container details!

### Step 8: Extract Specific Information

```bash
# Get IP address
docker inspect -f '{{.NetworkSettings.IPAddress}}' log-demo

# Get status
docker inspect -f '{{.State.Status}}' log-demo

# Get image
docker inspect -f '{{.Config.Image}}' log-demo

# Get port mappings
docker inspect -f '{{.NetworkSettings.Ports}}' log-demo
```

### Step 9: View Formatted Inspect

```bash
# Pretty print with jq (if installed)
docker inspect log-demo | jq '.[0].State'

# Or use Python
docker inspect log-demo | python3 -m json.tool | less
```

## 📊 Monitoring Resources

### Step 10: Check Resource Usage

```bash
# Real-time stats (like top)
docker stats log-demo

# Or all running containers
docker stats
```

You'll see:
- CPU usage
- Memory usage
- Network I/O
- Disk I/O

Press `Ctrl+C` to exit.

### Step 11: One-Time Stats

```bash
# Get stats once without streaming
docker stats --no-stream log-demo
```

## 🧪 Practical Scenarios

### Scenario 1: Debugging Startup Failures

```bash
# Start a container that might fail
docker run -d --name broken-app nginx

# If it stops immediately, check logs
docker logs broken-app

# Check why it stopped
docker inspect -f '{{.State.Status}}' broken-app
docker inspect -f '{{.State.ExitCode}}' broken-app
```

### Scenario 2: Finding Container IP

```bash
# Get container IP (useful for networking)
docker inspect -f '{{.NetworkSettings.IPAddress}}' log-demo

# Or all network settings
docker inspect -f '{{json .NetworkSettings}}' log-demo | jq
```

### Scenario 3: Monitor Multiple Containers

```bash
# Start several containers
docker run -d --name web1 -p 8081:80 nginx
docker run -d --name web2 -p 8082:80 nginx
docker run -d --name web3 -p 8083:80 nginx

# Monitor all at once
docker stats

# Press Ctrl+C when done

# Clean up
docker rm -f web1 web2 web3
```

### Scenario 4: Search Logs for Errors

```bash
# Generate some 404 errors
curl http://localhost:8080/notfound
curl http://localhost:8080/missing

# Search logs for errors
docker logs log-demo | grep "404"

# Count errors
docker logs log-demo | grep -c "404"

# Show errors with context
docker logs log-demo | grep -A 2 -B 2 "404"
```

## 💡 Key Concepts

### Log Drivers

Docker supports different log drivers:

```bash
# Check what log driver a container uses
docker inspect -f '{{.HostConfig.LogConfig.Type}}' log-demo
```

Common drivers:
- `json-file` (default) - Logs to JSON files
- `syslog` - Forward to syslog
- `journald` - Use systemd journal
- `none` - No logs

### Inspect Output Structure

```json
{
  "Id": "abc123...",
  "Created": "2025-01-15T...",
  "State": {
    "Status": "running",
    "Running": true,
    "ExitCode": 0
  },
  "Config": {
    "Image": "nginx",
    "Cmd": [...]
  },
  "NetworkSettings": {
    "IPAddress": "172.17.0.2",
    "Ports": {...}
  }
}
```

### Useful Inspect Paths

```bash
# Common inspection paths
{{.State.Status}}                    # running, exited, etc.
{{.State.ExitCode}}                  # Exit code if stopped
{{.NetworkSettings.IPAddress}}       # Container IP
{{.NetworkSettings.Ports}}           # Port mappings
{{.Config.Image}}                    # Image used
{{.Config.Env}}                      # Environment variables
{{.HostConfig.RestartPolicy}}        # Restart policy
{{.Mounts}}                          # Volume mounts
```

## ✅ Practice Exercises

### Exercise 1: Log Analysis

```bash
# 1. Start nginx
docker run -d -p 8080:80 --name practice nginx

# 2. Generate different types of requests
curl http://localhost:8080                    # 200 OK
curl http://localhost:8080/notfound          # 404
curl http://localhost:8080/test              # 404

# 3. Analyze logs
docker logs practice | grep "200"
docker logs practice | grep "404"
docker logs practice --tail 5

# 4. Clean up
docker rm -f practice
```

### Exercise 2: Container Investigation

Investigate a container without using `exec`:

<details>
<summary>Solution</summary>

```bash
# Start container
docker run -d --name investigate nginx

# Get all key info
echo "Status: $(docker inspect -f '{{.State.Status}}' investigate)"
echo "IP Address: $(docker inspect -f '{{.NetworkSettings.IPAddress}}' investigate)"
echo "Image: $(docker inspect -f '{{.Config.Image}}' investigate)"
echo "Started: $(docker inspect -f '{{.State.StartedAt}}' investigate)"

# Check resources
docker stats --no-stream investigate

# View logs
docker logs investigate

# Clean up
docker rm -f investigate
```
</details>

### Exercise 3: Multi-Container Monitoring

Monitor multiple containers and find the one using most memory:

<details>
<summary>Solution</summary>

```bash
# Start multiple containers
docker run -d --name mon1 nginx
docker run -d --name mon2 nginx
docker run -d --name mon3 nginx

# Get stats
docker stats --no-stream --format "table {{.Name}}\t{{.MemUsage}}"

# Or sort by memory (requires formatting)
docker stats --no-stream mon1 mon2 mon3

# Clean up
docker rm -f mon1 mon2 mon3
```
</details>

## 🔧 Advanced Log Commands

```bash
# Logs since specific time
docker logs --since 2024-01-15 log-demo

# Logs until specific time
docker logs --until 2024-01-15T12:00:00 log-demo

# Logs since 10 minutes ago
docker logs --since 10m log-demo

# Combine options
docker logs -t --since 5m --tail 20 -f log-demo
```

## 📊 Useful One-Liners

```bash
# Get IPs of all running containers
docker ps -q | xargs docker inspect -f '{{.Name}} - {{.NetworkSettings.IPAddress}}'

# Get port mappings
docker ps --format "table {{.Names}}\t{{.Ports}}"

# Show container sizes
docker ps -s

# Get container memory usage
docker stats --no-stream --format "table {{.Name}}\t{{.MemUsage}}"

# Check if container is healthy
docker inspect -f '{{.State.Health.Status}}' <container>
```

## ❓ Common Issues

### Issue: "docker logs" shows nothing

**Possible reasons:**
1. Application logs to files, not stdout/stderr
2. Container just started (no logs yet)
3. Wrong log driver

**Debug:**
```bash
# Check log driver
docker inspect -f '{{.HostConfig.LogConfig.Type}}' <container>

# If app logs to files, use exec
docker exec <container> cat /var/log/app.log
```

### Issue: Logs are too large

**Solution:**
```bash
# Use --tail to limit
docker logs --tail 100 <container>

# Or configure log rotation
# (requires Docker daemon config)
```

### Issue: Can't find container IP

**If IP is empty:**
```bash
# Check if using custom network
docker inspect -f '{{.NetworkSettings.Networks}}' <container>
```

## 📚 Debugging Checklist

When a container isn't working:

1. **Is it running?**
   ```bash
   docker ps -a
   ```

2. **Check logs for errors:**
   ```bash
   docker logs <container>
   ```

3. **Check exit code (if stopped):**
   ```bash
   docker inspect -f '{{.State.ExitCode}}' <container>
   ```

4. **Check resource usage:**
   ```bash
   docker stats --no-stream <container>
   ```

5. **Verify network/ports:**
   ```bash
   docker inspect -f '{{.NetworkSettings.Ports}}' <container>
   ```

6. **Check configuration:**
   ```bash
   docker inspect <container>
   ```

## 🎉 Part 1 Complete!

Congratulations! You've completed Part 1 and now know:

✅ How to run containers from Docker Hub
✅ Port mapping and accessing services
✅ Getting shell access to containers
✅ Viewing and following logs
✅ Inspecting container details
✅ Monitoring resource usage
✅ Debugging common issues

### Clean Up

```bash
# Remove the practice container
docker rm -f log-demo

# Clean up any other test containers
docker ps -a
docker container prune
```

## 📚 What's Next?

**Next Part:** [Part 2 - Container Management →](../part2-management/README.md)

In Part 2, you'll learn:
- Restart policies (auto-start on boot)
- Environment variables
- Volume mounting (data persistence)
- Network configuration
- Resource limits

---

**Lesson Duration:** 10 minutes
**Difficulty:** Beginner
**Prerequisites:** Lessons 1-4 completed
**Skills:** Debugging, monitoring, troubleshooting
