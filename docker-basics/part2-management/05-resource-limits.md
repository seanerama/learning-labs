# Lesson 5: Resource Limits

Control CPU and memory usage to prevent runaway containers!

## 🎯 Objective

Learn how to set resource constraints on containers to prevent them from consuming all available system resources and affecting other containers or the host.

## 📝 What You'll Learn

- Setting memory limits
- Configuring CPU limits
- Monitoring resource usage
- Understanding resource reservation vs limits
- Handling out-of-memory (OOM) scenarios
- Best practices for production deployments

## 🚀 Steps

### Step 1: Default Behavior (No Limits)

```bash
# Run container without limits - can use ALL available resources
docker run -d --name unlimited nginx

# Check resources (no limits set)
docker inspect unlimited | grep -A 5 "Memory\|Cpu"
```

Output shows `0` for limits, meaning unlimited access.

```bash
# Clean up
docker rm -f unlimited
```

### Step 2: Set Memory Limit

```bash
# Limit container to 512MB of memory
docker run -d \
  --name limited-mem \
  --memory="512m" \
  nginx

# Verify limit
docker inspect limited-mem | grep Memory

# Or use stats
docker stats limited-mem --no-stream
```

Output shows memory limit:
```
CONTAINER ID   NAME          MEM USAGE / LIMIT     MEM %
abc123...      limited-mem   5.5MiB / 512MiB      1.07%
```

### Step 3: Test Memory Limit

```bash
# Run container that tries to allocate too much memory
docker run --rm \
  --memory="100m" \
  --name mem-test \
  alpine sh -c '
    echo "Trying to allocate 200MB (limit is 100MB)..."
    # This will be killed by OOM
    dd if=/dev/zero of=/tmp/test bs=1M count=200 2>&1 || echo "Killed by OOM!"
  '
```

The container is killed when it exceeds memory limit.

```bash
# Check what happened
docker inspect mem-test --format '{{.State.OOMKilled}}'  # Shows "true" if OOM killed
```

### Step 4: Memory with Swap

```bash
# Memory + swap limit
docker run -d \
  --name mem-swap \
  --memory="512m" \
  --memory-swap="1g" \
  alpine sleep 1000

# This means:
# - 512MB RAM
# - 512MB swap (1g total - 512m memory = 512m swap)

# Check limits
docker stats mem-swap --no-stream

# Clean up
docker rm -f mem-swap
```

### Step 5: Disable Swap

```bash
# Set memory and swap to same value = no swap
docker run -d \
  --name no-swap \
  --memory="512m" \
  --memory-swap="512m" \
  alpine sleep 1000

# This gives 512MB RAM and 0 swap

docker rm -f no-swap
```

### Step 6: CPU Limits

```bash
# Limit to 50% of one CPU core (0.5 CPUs)
docker run -d \
  --name cpu-limited \
  --cpus="0.5" \
  alpine sh -c 'while true; do :; done'

# Monitor CPU usage
docker stats cpu-limited --no-stream
```

Output shows CPU usage capped around 50%:
```
CONTAINER ID   NAME          CPU %     MEM USAGE / LIMIT
abc123...      cpu-limited   50.00%    1.2MiB / unlimited
```

```bash
# Stop the CPU hog
docker rm -f cpu-limited
```

### Step 7: CPU Shares (Relative Weight)

```bash
# Default CPU shares is 1024
# Higher shares = more CPU priority

# Container with default shares
docker run -d --name normal-priority alpine sh -c 'while true; do :; done'

# Container with double priority
docker run -d \
  --name high-priority \
  --cpu-shares=2048 \
  alpine sh -c 'while true; do :; done'

# Monitor both
docker stats normal-priority high-priority --no-stream

# High-priority gets roughly 2x CPU time when both compete

# Clean up
docker rm -f normal-priority high-priority
```

### Step 8: Monitoring All Containers

```bash
# Start several containers with different limits
docker run -d --name web --memory="256m" --cpus="0.5" nginx
docker run -d --name db --memory="1g" --cpus="1.0" postgres:alpine -c shared_buffers=256MB
docker run -d --name cache --memory="128m" --cpus="0.25" redis:alpine

# Monitor all in real-time
docker stats

# Press Ctrl+C to stop monitoring

# Get one-time snapshot
docker stats --no-stream
```

Output:
```
CONTAINER ID   NAME    CPU %   MEM USAGE / LIMIT   MEM %   NET I/O       BLOCK I/O
abc123...      web     0.01%   5.5MiB / 256MiB     2.15%   1.2kB / 0B    0B / 0B
def456...      db      0.05%   45.2MiB / 1GiB      4.41%   2.5kB / 0B    8MB / 0B
ghi789...      cache   0.02%   3.1MiB / 128MiB     2.42%   800B / 0B     0B / 0B
```

### Step 9: Update Resource Limits

```bash
# You can change limits without recreating container!

# Check current memory limit
docker inspect -f '{{.HostConfig.Memory}}' web

# Update to 512MB
docker update --memory="512m" web

# Verify change
docker inspect -f '{{.HostConfig.Memory}}' web

# Update CPU limit
docker update --cpus="1.0" web

# Check new stats
docker stats web --no-stream
```

### Step 10: Memory Reservations

```bash
# Set soft limit (reservation) and hard limit
docker run -d \
  --name reserved \
  --memory-reservation="256m" \
  --memory="512m" \
  alpine sleep 1000

# Container should stay within 256MB
# But can burst up to 512MB if host has available memory

docker stats reserved --no-stream

docker rm -f reserved
```

## 🧪 Practical Scenarios

### Scenario 1: Production Web Server

```bash
# Typical production web server with reasonable limits
docker run -d \
  --name production-web \
  --restart unless-stopped \
  --memory="1g" \
  --memory-reservation="512m" \
  --cpus="2.0" \
  --memory-swap="2g" \
  -p 80:80 \
  nginx

# Monitor it
docker stats production-web --no-stream

# Clean up
docker rm -f production-web
```

### Scenario 2: Resource-Constrained Environment

```bash
# Multiple services on small VPS (4GB RAM total)

# Web server - 512MB, 0.5 CPU
docker run -d \
  --name web \
  --memory="512m" \
  --cpus="0.5" \
  -p 80:80 \
  nginx

# Database - 2GB, 1.5 CPU
docker run -d \
  --name db \
  --memory="2g" \
  --cpus="1.5" \
  -e POSTGRES_PASSWORD=secret \
  postgres:alpine

# Cache - 512MB, 0.25 CPU
docker run -d \
  --name cache \
  --memory="512m" \
  --cpus="0.25" \
  redis:alpine

# Background worker - 512MB, 0.5 CPU
docker run -d \
  --name worker \
  --memory="512m" \
  --cpus="0.5" \
  alpine sleep 1000

# Total: 3.5GB RAM (leaving 512MB for host), 2.75 CPUs

# Monitor all
docker stats --no-stream

# Clean up
docker rm -f web db cache worker
```

### Scenario 3: Preventing Memory Leaks

```bash
# App with potential memory leak - strict limit
docker run -d \
  --name leaky-app \
  --memory="256m" \
  --memory-swap="256m" \
  --oom-kill-disable=false \
  alpine sh -c '
    # Simulate slow memory leak
    while true; do
      dd if=/dev/zero of=/tmp/leak_$RANDOM bs=1M count=1 2>/dev/null
      sleep 1
    done
  '

# Monitor until OOM kill
watch -n 1 docker stats leaky-app --no-stream

# Container will be killed when it hits 256MB
# Check OOM status
docker inspect -f '{{.State.OOMKilled}}' leaky-app

# Clean up
docker rm -f leaky-app
```

### Scenario 4: CI/CD Build Container

```bash
# Build job with time limit and resource constraints
docker run --rm \
  --name build-job \
  --memory="2g" \
  --cpus="2.0" \
  --memory-swap="2g" \
  node:alpine sh -c '
    echo "Running build..."
    # Simulate build process
    npm install --quiet 2>/dev/null || echo "Build completed"
  '

# Resources freed automatically when done (--rm flag)
```

## 💡 Key Concepts

### Memory Limit Options

```
┌─────────────────────────────────────────────────┐
│         Memory Limit Options                    │
├─────────────────────────────────────────────────┤
│                                                 │
│  --memory (-m)                                  │
│    └─ Maximum memory (RAM + swap)              │
│    └─ Example: --memory="512m"                 │
│                                                 │
│  --memory-swap                                  │
│    └─ Total memory (RAM + swap limit)          │
│    └─ Example: --memory-swap="1g"              │
│    └─ Set equal to --memory to disable swap    │
│                                                 │
│  --memory-reservation                           │
│    └─ Soft limit (can exceed if available)     │
│    └─ Example: --memory-reservation="256m"     │
│                                                 │
│  --oom-kill-disable                             │
│    └─ Prevent OOM killer (use with care!)      │
│    └─ Example: --oom-kill-disable=true         │
│                                                 │
└─────────────────────────────────────────────────┘
```

### CPU Limit Options

```
┌─────────────────────────────────────────────────┐
│         CPU Limit Options                       │
├─────────────────────────────────────────────────┤
│                                                 │
│  --cpus                                         │
│    └─ Number of CPUs (fractional allowed)      │
│    └─ Example: --cpus="1.5" = 1.5 CPU cores    │
│                                                 │
│  --cpu-shares                                   │
│    └─ Relative weight (default: 1024)          │
│    └─ Example: --cpu-shares=512 (half weight)  │
│    └─ Only matters under CPU contention        │
│                                                 │
│  --cpuset-cpus                                  │
│    └─ Specific CPU cores to use                │
│    └─ Example: --cpuset-cpus="0,1"             │
│                                                 │
│  --cpu-period / --cpu-quota                     │
│    └─ Advanced CPU scheduling                  │
│    └─ Usually use --cpus instead               │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Memory Units

```bash
# Supported units
-m 512b    # bytes
-m 512k    # kilobytes
-m 512m    # megabytes
-m 512g    # gigabytes

# Examples
--memory="100m"      # 100 megabytes
--memory="1.5g"      # 1.5 gigabytes
--memory="524288k"   # 512 megabytes (in kilobytes)
```

### Resource Guarantees vs Limits

```
Reservation (Soft Limit):
├─ Guaranteed minimum when resources are scarce
├─ Can use more if available
└─ Example: --memory-reservation="256m"

Limit (Hard Limit):
├─ Maximum allowed usage
├─ Container killed/throttled if exceeded
└─ Example: --memory="512m"

Best Practice:
├─ Set reservation for guaranteed baseline
├─ Set limit to prevent runaway usage
└─ Example: --memory-reservation="256m" --memory="512m"
```

### OOM Killer Behavior

```
What happens when container exceeds memory limit?

1. Kernel's OOM killer activates
2. Selects process to kill (usually highest memory user)
3. Kills the process
4. Container may exit if main process killed
5. Restart policy determines what happens next

Prevent OOM kills:
├─ Set appropriate memory limits
├─ Monitor memory usage
├─ Fix memory leaks in applications
└─ Use swap for burst capacity
```

## ✅ Practice Exercises

### Exercise 1: Find Optimal Limits

Determine appropriate resource limits for an application:

<details>
<summary>Solution</summary>

```bash
# Step 1: Run without limits and monitor
docker run -d --name test-app nginx
docker stats test-app --no-stream

# Step 2: Generate load
for i in {1..100}; do
  curl -s http://localhost:80 > /dev/null
done

# Step 3: Check peak usage
docker stats test-app --no-stream

# Step 4: Set limits with 20% buffer
# If peak was 50MB, set limit to 60-70MB
docker rm -f test-app

docker run -d \
  --name test-app \
  --memory="70m" \
  --cpus="0.5" \
  nginx

# Step 5: Test with limits
for i in {1..100}; do
  curl -s http://localhost:80 > /dev/null
done

docker stats test-app --no-stream

# Clean up
docker rm -f test-app
```
</details>

### Exercise 2: Prevent Resource Exhaustion

Multiple containers competing for resources:

<details>
<summary>Solution</summary>

```bash
# Start containers without limits
docker run -d --name greedy1 alpine sh -c 'while :; do :; done'
docker run -d --name greedy2 alpine sh -c 'while :; do :; done'
docker run -d --name greedy3 alpine sh -c 'while :; done'

# Check CPU usage - all at 100%!
docker stats --no-stream

# Stop them
docker rm -f greedy1 greedy2 greedy3

# Start with CPU limits
docker run -d --name limited1 --cpus="0.33" alpine sh -c 'while :; do :; done'
docker run -d --name limited2 --cpus="0.33" alpine sh -c 'while :; do :; done'
docker run -d --name limited3 --cpus="0.33" alpine sh -c 'while :; do :; done'

# Check CPU usage - each limited to 33%
docker stats --no-stream

# Clean up
docker rm -f limited1 limited2 limited3
```
</details>

### Exercise 3: Memory Pressure Testing

Test how container handles memory pressure:

<details>
<summary>Solution</summary>

```bash
# Run container with strict memory limit
docker run -d \
  --name mem-pressure \
  --memory="256m" \
  --memory-swap="256m" \
  alpine sleep 1000

# Check baseline
docker stats mem-pressure --no-stream

# Gradually allocate memory
docker exec mem-pressure sh -c 'dd if=/dev/zero of=/tmp/test1 bs=1M count=50'
docker stats mem-pressure --no-stream

docker exec mem-pressure sh -c 'dd if=/dev/zero of=/tmp/test2 bs=1M count=50'
docker stats mem-pressure --no-stream

docker exec mem-pressure sh -c 'dd if=/dev/zero of=/tmp/test3 bs=1M count=50'
docker stats mem-pressure --no-stream

# Try to exceed limit - this will fail
docker exec mem-pressure sh -c 'dd if=/dev/zero of=/tmp/test4 bs=1M count=200' || echo "Memory limit enforced!"

# Check if OOM killed
docker inspect -f '{{.State.Status}} - OOMKilled: {{.State.OOMKilled}}' mem-pressure

# Clean up
docker rm -f mem-pressure
```
</details>

## 🔧 Advanced Usage

### CPU Pinning

```bash
# Pin container to specific CPU cores
# Useful for isolating workloads

# Use only cores 0 and 1
docker run -d \
  --name pinned \
  --cpuset-cpus="0,1" \
  alpine sh -c 'while :; do :; done'

# Check which cores it's using
docker exec pinned grep Cpus_allowed_list /proc/self/status

docker rm -f pinned
```

### Memory Swappiness

```bash
# Control swap tendency (0-100)
# 0 = avoid swap, 100 = prefer swap

docker run -d \
  --name low-swap \
  --memory="512m" \
  --memory-swappiness=10 \
  alpine sleep 1000

# Check setting
docker inspect -f '{{.HostConfig.MemorySwappiness}}' low-swap

docker rm -f low-swap
```

### Block I/O Limits

```bash
# Limit disk read/write speed

# Limit to 10 MB/s reads
docker run -d \
  --name io-limited \
  --device-read-bps /dev/sda:10mb \
  alpine sleep 1000

# Test read speed
docker exec io-limited dd if=/dev/zero of=/tmp/test bs=1M count=100

docker rm -f io-limited
```

### PID Limit

```bash
# Limit number of processes in container
docker run -d \
  --name pid-limited \
  --pids-limit 10 \
  alpine sleep 1000

# Try to create too many processes - fails
docker exec pid-limited sh -c '
  for i in $(seq 1 20); do
    sleep 1000 &
  done
' || echo "PID limit enforced!"

docker rm -f pid-limited
```

## 📊 Useful One-Liners

```bash
# Show resource usage for all containers
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}"

# Find containers using most memory
docker stats --no-stream --format "table {{.Name}}\t{{.MemPerc}}" | sort -k2 -rn

# Find containers using most CPU
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}" | sort -k2 -rn

# Show memory limits for all containers
docker ps -q | xargs docker inspect -f '{{.Name}}: {{.HostConfig.Memory}}' | sed 's/:/: /' | column -t

# Total memory used by all containers
docker stats --no-stream --format "{{.MemUsage}}" | awk '{sum += $1} END {print sum " MB"}'

# Update all running containers to use max 50% CPU
docker ps -q | xargs -I {} docker update --cpus="0.5" {}

# Check which containers are at risk of OOM
docker ps -q | xargs docker inspect -f '{{.Name}} OOMKilled: {{.State.OOMKilled}}'
```

## ❓ Common Issues

### Issue: Container performs poorly

**Check resource limits:**

```bash
# View current limits
docker inspect my-container | grep -E "Memory|Cpu"

# Check actual usage vs limit
docker stats my-container --no-stream

# If usage is at limit, increase:
docker update --memory="1g" --cpus="2.0" my-container
```

### Issue: Container keeps getting OOM killed

**Solutions:**

```bash
# 1. Increase memory limit
docker update --memory="1g" my-container

# 2. Add swap capacity
docker update --memory-swap="2g" my-container

# 3. Check for memory leaks
docker logs my-container | grep -i "memory\|oom"

# 4. Monitor memory usage over time
docker stats my-container
```

### Issue: CPU limit not working as expected

**Understanding CPU shares:**

```bash
# --cpus vs --cpu-shares

# --cpus is an absolute limit
docker run --cpus="0.5" my-app  # Max 50% of 1 core

# --cpu-shares is relative (only matters under contention)
docker run --cpu-shares=512 my-app  # Gets 50% when competing with default (1024)

# Prefer --cpus for predictable limits
```

### Issue: Cannot update resource limits

**Some limits can't be updated:**

```bash
# Can update these:
docker update --memory="1g" my-container      # ✅
docker update --cpus="2.0" my-container       # ✅

# Cannot update these (need to recreate):
--memory-swap                                  # ❌
--cpuset-cpus                                  # ❌

# Solution: Recreate container
docker rm my-container
docker run -d --memory-swap="2g" ...
```

## 🎯 Best Practices

### 1. Always Set Limits in Production

```bash
# ✅ GOOD - Prevents runaway containers
docker run -d \
  --memory="512m" \
  --cpus="1.0" \
  my-app

# ❌ BAD - No limits, could crash host
docker run -d my-app
```

### 2. Monitor Before Setting Limits

```bash
# ✅ GOOD - Base limits on actual usage
# 1. Run without limits
docker run -d --name test my-app

# 2. Generate realistic load
# ... run tests ...

# 3. Check usage
docker stats test --no-stream

# 4. Set limits with buffer (1.5-2x peak)
docker run -d --memory="<peak_x2>" --cpus="<peak_x1.5>" my-app
```

### 3. Use Reservations + Limits

```bash
# ✅ GOOD - Guaranteed minimum, capped maximum
docker run -d \
  --memory-reservation="256m" \
  --memory="512m" \
  my-app

# Container guaranteed 256MB, can burst to 512MB
```

### 4. Set Swap Equal to Memory (No Swap)

```bash
# ✅ GOOD for predictable performance
docker run -d \
  --memory="512m" \
  --memory-swap="512m" \
  my-app

# ⚠️ OKAY for burst capacity
docker run -d \
  --memory="512m" \
  --memory-swap="1g" \
  my-app
```

### 5. Document Resource Requirements

```bash
# Add labels with resource requirements
docker run -d \
  --label "resources.memory.min=256m" \
  --label "resources.memory.max=512m" \
  --label "resources.cpu.min=0.5" \
  --label "resources.cpu.max=1.0" \
  --memory="512m" \
  --cpus="1.0" \
  my-app
```

## 🎉 Part 2 Complete!

You now know:

✅ How to set memory and CPU limits
✅ How to monitor resource usage
✅ How to prevent resource exhaustion
✅ How to update limits on running containers
✅ Best practices for production deployments

You've completed Part 2! You now have the skills to:
- Configure containers to auto-start on boot
- Manage configuration with environment variables
- Persist data with volumes
- Create isolated networks
- Control resource usage

### What's Next?

**Next:** [Part 3 - Building Images →](../part3-building/README.md)

In Part 3, you'll learn:
- Writing Dockerfiles
- Building custom images
- Creating a Streamlit application
- Multi-stage builds
- Publishing to Docker Hub

---

**Lesson Duration:** 10 minutes
**Difficulty:** Intermediate
**Prerequisites:** Lessons 1-4 completed
**Skills:** Resource management, performance tuning, production deployment
