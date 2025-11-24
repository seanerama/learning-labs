# Lesson 4: Networking

Master container networking and enable container-to-container communication!

## 🎯 Objective

Learn how Docker networking works, create custom networks, and enable containers to communicate with each other using DNS resolution.

## 📝 What You'll Learn

- Understanding Docker network drivers
- Creating custom networks
- Connecting containers to networks
- Container DNS resolution
- Port publishing vs network communication
- Network isolation and security

## 🚀 Steps

### Step 1: Default Bridge Network

```bash
# Run container without specifying network (uses default bridge)
docker run -d --name web1 nginx

# Inspect its network
docker inspect -f '{{.NetworkSettings.Networks}}' web1

# Check container IP
docker inspect -f '{{.NetworkSettings.IPAddress}}' web1
```

Output shows IP like `172.17.0.2`

```bash
# Run another container
docker run -d --name web2 nginx

# Get its IP
docker inspect -f '{{.NetworkSettings.IPAddress}}' web2
```

Try to ping by name:
```bash
# This FAILS on default bridge
docker exec web1 ping web2
```

Output:
```
ping: bad address 'web2'
```

**Problem:** Default bridge doesn't support DNS resolution between containers!

```bash
# Clean up
docker rm -f web1 web2
```

### Step 2: Create Custom Network

```bash
# Create a custom bridge network
docker network create my-network

# List networks
docker network ls

# Inspect the network
docker network inspect my-network
```

Output shows network details:
```json
{
    "Name": "my-network",
    "Driver": "bridge",
    "Scope": "local",
    "Subnet": "172.18.0.0/16",
    "Gateway": "172.18.0.1"
}
```

### Step 3: Run Containers on Custom Network

```bash
# Run containers on custom network
docker run -d --name web1 --network my-network nginx
docker run -d --name web2 --network my-network nginx

# Now ping by NAME works!
docker exec web1 ping -c 3 web2
```

Output:
```
PING web2 (172.18.0.3): 56 data bytes
64 bytes from 172.18.0.3: seq=0 ttl=64 time=0.123 ms
64 bytes from 172.18.0.3: seq=1 ttl=64 time=0.098 ms
64 bytes from 172.18.0.3: seq=2 ttl=64 time=0.091 ms
```

**Key feature:** Custom networks provide automatic DNS resolution!

```bash
# Test the other direction
docker exec web2 ping -c 3 web1
```

Works perfectly!

### Step 4: Connect Existing Container to Network

```bash
# Run container on default network
docker run -d --name web3 nginx

# Try to ping web1 - fails (different networks)
docker exec web3 ping -c 1 web1 || echo "Failed: Not on same network"

# Connect web3 to my-network
docker network connect my-network web3

# Now it works!
docker exec web3 ping -c 3 web1
```

**Result:** Container can be on multiple networks simultaneously!

```bash
# List container's networks
docker inspect -f '{{range $net,$v := .NetworkSettings.Networks}}{{$net}} {{end}}' web3
```

Output:
```
bridge my-network
```

### Step 5: Network Isolation

```bash
# Create two separate networks
docker network create team-a
docker network create team-b

# Team A containers
docker run -d --name app-a1 --network team-a alpine sleep 1000
docker run -d --name app-a2 --network team-a alpine sleep 1000

# Team B containers
docker run -d --name app-b1 --network team-b alpine sleep 1000
docker run -d --name app-b2 --network team-b alpine sleep 1000

# Team A can communicate within team
docker exec app-a1 ping -c 2 app-a2  # ✅ Works

# Team B can communicate within team
docker exec app-b1 ping -c 2 app-b2  # ✅ Works

# Teams CANNOT communicate across networks
docker exec app-a1 ping -c 2 app-b1 || echo "Isolated!"  # ❌ Fails
```

**Result:** Networks provide isolation between container groups!

### Step 6: Practical Example - Web App with Database

```bash
# Create application network
docker network create app-net

# Run database
docker run -d \
  --name database \
  --network app-net \
  -e POSTGRES_PASSWORD=secret \
  postgres:alpine

# Wait for database to start
sleep 10

# Run application that connects to database by NAME
docker run -it --rm \
  --network app-net \
  postgres:alpine \
  psql -h database -U postgres
```

Enter password `secret` and you're connected!

Inside PostgreSQL:
```sql
-- You're connected to the database using DNS name "database"!
\l
\q
```

### Step 7: Network Aliases

```bash
# Run container with network alias
docker run -d \
  --name db \
  --network app-net \
  --network-alias database \
  --network-alias db-server \
  postgres:alpine

# Now reachable by multiple names!
docker run --rm --network app-net alpine ping -c 2 database  # Works
docker run --rm --network app-net alpine ping -c 2 db-server  # Works
docker run --rm --network app-net alpine ping -c 2 db  # Works
```

**Use case:** Different apps use different names for the same service!

### Step 8: Port Publishing vs Network Communication

```bash
# Run web server WITHOUT publishing ports
docker run -d \
  --name backend \
  --network app-net \
  nginx

# Cannot access from host
curl http://localhost:80 || echo "Not accessible from host"

# But other containers on same network CAN access it
docker run --rm \
  --network app-net \
  alpine \
  wget -qO- http://backend
```

Output shows Nginx welcome page!

```bash
# Run another web server WITH published ports
docker run -d \
  --name frontend \
  --network app-net \
  -p 8080:80 \
  nginx

# Accessible from host
curl http://localhost:8080

# Also accessible from other containers
docker run --rm \
  --network app-net \
  alpine \
  wget -qO- http://frontend
```

**Key concept:**
- `-p 8080:80` = Host access
- `--network` = Container-to-container access

## 🧪 Practical Scenarios

### Scenario 1: Multi-Tier Application

```bash
# Create network
docker network create webapp-net

# Database tier
docker run -d \
  --name db \
  --network webapp-net \
  -e POSTGRES_PASSWORD=dbpass \
  postgres:alpine

# Wait for database
sleep 10

# Backend API tier (connects to db by name)
docker run -d \
  --name api \
  --network webapp-net \
  -e DATABASE_URL=postgresql://postgres:dbpass@db:5432/postgres \
  alpine sh -c 'echo "API would connect to database at: $DATABASE_URL"; sleep infinity'

# Frontend tier (connects to api by name, exposed to host)
docker run -d \
  --name frontend \
  --network webapp-net \
  -p 8080:80 \
  nginx

# Verify connectivity
echo "=== Backend can reach database ==="
docker exec api ping -c 2 db

echo "=== Frontend can reach backend ==="
docker exec frontend curl -s http://api || echo "API not running HTTP, but network works"

echo "=== Host can reach frontend ==="
curl -s http://localhost:8080 | head -n 5

# Clean up
docker rm -f db api frontend
docker network rm webapp-net
```

### Scenario 2: Microservices with Service Discovery

```bash
# Create microservices network
docker network create microservices

# Service 1: User service
docker run -d \
  --name user-service \
  --network microservices \
  alpine sh -c 'echo "User Service Running"; sleep infinity'

# Service 2: Order service
docker run -d \
  --name order-service \
  --network microservices \
  alpine sh -c 'echo "Order Service Running"; sleep infinity'

# Service 3: Payment service
docker run -d \
  --name payment-service \
  --network microservices \
  alpine sh -c 'echo "Payment Service Running"; sleep infinity'

# API Gateway can reach all services by name
docker run --rm \
  --network microservices \
  alpine sh -c '
    echo "Testing service discovery..."
    ping -c 1 user-service && echo "✓ User service found"
    ping -c 1 order-service && echo "✓ Order service found"
    ping -c 1 payment-service && echo "✓ Payment service found"
  '

# Clean up
docker rm -f user-service order-service payment-service
docker network rm microservices
```

### Scenario 3: Development and Production Networks

```bash
# Development network - less isolated
docker network create dev-net

# Production network - more isolated
docker network create prod-net

# Dev services
docker run -d --name dev-api --network dev-net alpine sleep 1000
docker run -d --name dev-db --network dev-net alpine sleep 1000

# Prod services
docker run -d --name prod-api --network prod-net alpine sleep 1000
docker run -d --name prod-db --network prod-net alpine sleep 1000

# Dev containers can talk to each other
docker exec dev-api ping -c 2 dev-db  # ✅ Works

# Prod containers can talk to each other
docker exec prod-api ping -c 2 prod-db  # ✅ Works

# Dev and Prod are ISOLATED
docker exec dev-api ping -c 2 prod-db 2>&1 || echo "✓ Isolated!"

# List networks with containers
docker network inspect dev-net --format '{{.Name}}: {{range .Containers}}{{.Name}} {{end}}'
docker network inspect prod-net --format '{{.Name}}: {{range .Containers}}{{.Name}} {{end}}'

# Clean up
docker rm -f dev-api dev-db prod-api prod-db
docker network rm dev-net prod-net
```

### Scenario 4: Connect to External Network

```bash
# Create network with specific subnet
docker network create \
  --subnet=172.20.0.0/16 \
  --gateway=172.20.0.1 \
  custom-subnet

# Run container with specific IP
docker run -d \
  --name fixed-ip \
  --network custom-subnet \
  --ip 172.20.0.100 \
  alpine sleep 1000

# Verify IP
docker inspect -f '{{.NetworkSettings.Networks.custom_subnet.IPAddress}}' fixed-ip

# Clean up
docker rm -f fixed-ip
docker network rm custom-subnet
```

## 💡 Key Concepts

### Docker Network Drivers

```
┌─────────────────────────────────────────────────┐
│         Network Drivers                         │
├─────────────────────────────────────────────────┤
│                                                 │
│  bridge (default)                               │
│    └─ Isolated network on single host          │
│    └─ Most common for single-host apps         │
│                                                 │
│  host                                           │
│    └─ Container uses host's network directly   │
│    └─ No network isolation                     │
│                                                 │
│  none                                           │
│    └─ No networking at all                     │
│    └─ Completely isolated                      │
│                                                 │
│  overlay                                        │
│    └─ Multi-host networking (Swarm)            │
│    └─ For distributed applications             │
│                                                 │
│  macvlan                                        │
│    └─ Assign MAC address to container          │
│    └─ Appears as physical device on network    │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Network Communication Patterns

```
Pattern 1: Published Ports
┌────────┐         ┌──────────────┐
│  Host  │  :8080  │  Container   │
│        ├────────>│  port 80     │
└────────┘         └──────────────┘
Use: External access from host/internet

Pattern 2: Same Network
┌──────────────┐   network    ┌──────────────┐
│ Container A  ├──────────────>│ Container B  │
│  (frontend)  │   DNS name   │  (backend)   │
└──────────────┘              └──────────────┘
Use: Internal service communication

Pattern 3: Multiple Networks
┌──────────────┐
│  Container   │
├──────────────┤
│ Network A    │ ← Public services
│ Network B    │ ← Private services
└──────────────┘
Use: Segmentation and security
```

### DNS Resolution Rules

| Network Type | DNS Resolution | Container Name Access |
|--------------|----------------|----------------------|
| Default bridge | ❌ No | ❌ No |
| Custom bridge | ✅ Yes | ✅ Yes |
| Host | N/A | N/A |
| None | N/A | N/A |

### Network Isolation Benefits

```
Security Benefits:
├─ Database not exposed to internet
├─ Internal services not accessible externally
├─ Segment production from development
└─ Reduce attack surface

Organizational Benefits:
├─ Logical separation of services
├─ Easier to manage permissions
├─ Clear service boundaries
└─ Simplified troubleshooting
```

## ✅ Practice Exercises

### Exercise 1: WordPress with MySQL

Create a WordPress site with database on custom network:

<details>
<summary>Solution</summary>

```bash
# Create network
docker network create wordpress-net

# Run MySQL database
docker run -d \
  --name wordpress-db \
  --network wordpress-net \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -e MYSQL_DATABASE=wordpress \
  -e MYSQL_USER=wpuser \
  -e MYSQL_PASSWORD=wppass \
  mysql:8.0

# Wait for MySQL to be ready
sleep 20

# Run WordPress
docker run -d \
  --name wordpress-app \
  --network wordpress-net \
  -e WORDPRESS_DB_HOST=wordpress-db \
  -e WORDPRESS_DB_USER=wpuser \
  -e WORDPRESS_DB_PASSWORD=wppass \
  -e WORDPRESS_DB_NAME=wordpress \
  -p 8080:80 \
  wordpress:latest

# Wait for WordPress to start
sleep 10

# Access WordPress setup
echo "Visit http://localhost:8080 to set up WordPress!"

# Clean up when done
docker rm -f wordpress-app wordpress-db
docker network rm wordpress-net
```
</details>

### Exercise 2: Isolated Test Environment

Create isolated frontend and backend networks:

<details>
<summary>Solution</summary>

```bash
# Create two networks
docker network create frontend-net
docker network create backend-net

# Backend services (database, cache)
docker run -d --name database --network backend-net postgres:alpine \
  -e POSTGRES_PASSWORD=secret

docker run -d --name cache --network backend-net redis:alpine

# API server - on BOTH networks
docker run -d --name api --network backend-net alpine sleep 1000
docker network connect frontend-net api

# Frontend - only on frontend network
docker run -d --name web --network frontend-net alpine sleep 1000

# Test connectivity
echo "=== API can reach backend services ==="
docker exec api ping -c 2 database
docker exec api ping -c 2 cache

echo "=== Web can reach API ==="
docker exec web ping -c 2 api

echo "=== Web CANNOT reach backend directly (isolated) ==="
docker exec web ping -c 2 database 2>&1 || echo "✓ Properly isolated!"

# Clean up
docker rm -f database cache api web
docker network rm frontend-net backend-net
```
</details>

### Exercise 3: Network Troubleshooting

Practice diagnosing network issues:

<details>
<summary>Solution</summary>

```bash
# Create test network
docker network create test-net

# Run containers
docker run -d --name app1 --network test-net alpine sleep 1000
docker run -d --name app2 --network test-net alpine sleep 1000

# Troubleshooting commands
echo "=== Check if containers are on same network ==="
docker network inspect test-net --format '{{range .Containers}}{{.Name}} {{end}}'

echo "=== Get container IPs ==="
docker inspect -f '{{.Name}} - {{.NetworkSettings.Networks.test_net.IPAddress}}' app1 app2

echo "=== Test DNS resolution ==="
docker exec app1 nslookup app2 2>/dev/null || docker exec app1 ping -c 1 app2

echo "=== Check network connectivity ==="
docker exec app1 ping -c 3 app2

echo "=== List all networks ==="
docker network ls

echo "=== Show container's networks ==="
docker inspect -f '{{range $net,$v := .NetworkSettings.Networks}}{{$net}} {{end}}' app1

# Clean up
docker rm -f app1 app2
docker network rm test-net
```
</details>

## 🔧 Advanced Usage

### Host Network Mode

```bash
# Use host's network directly (no isolation)
docker run --rm --network host alpine ip addr

# Shows host's network interfaces!

# Run service on host's port
docker run -d --network host --name host-nginx nginx

# Accessible directly on port 80 (no port mapping needed)
curl http://localhost:80

# Clean up
docker rm -f host-nginx
```

**Warning:** Less secure, container has full network access!

### None Network Mode

```bash
# No networking at all
docker run --rm --network none alpine ip addr

# Shows only loopback interface

# Use case: Security-sensitive containers that don't need network
docker run -d --network none --name isolated alpine sleep 1000
docker exec isolated ping google.com  # Fails - no network!

docker rm -f isolated
```

### Network with Custom DNS

```bash
# Create network with custom DNS servers
docker network create \
  --dns 8.8.8.8 \
  --dns 8.8.4.4 \
  custom-dns-net

# Run container using custom DNS
docker run --rm --network custom-dns-net alpine cat /etc/resolv.conf

docker network rm custom-dns-net
```

### Container Linking (Legacy - Avoid)

```bash
# OLD WAY (deprecated, don't use)
docker run -d --name db postgres
docker run --link db:database my-app

# NEW WAY (use custom networks)
docker network create app-net
docker run -d --name db --network app-net postgres
docker run --network app-net my-app
```

## 📊 Useful One-Liners

```bash
# List all networks with their containers
for net in $(docker network ls -q); do
  echo "Network: $(docker network inspect $net --format '{{.Name}}')";
  docker network inspect $net --format '{{range .Containers}}  - {{.Name}}{{end}}';
  echo;
done

# Get container's IP on specific network
docker inspect -f '{{.NetworkSettings.Networks.my_network.IPAddress}}' my-container

# Find which network a container is on
docker inspect -f '{{range $net,$v := .NetworkSettings.Networks}}{{$net}} {{end}}' my-container

# Remove all custom networks
docker network rm $(docker network ls -q --filter type=custom)

# Show network with connected containers in table format
docker network ls --format "table {{.Name}}\t{{.Driver}}\t{{.Scope}}"

# Disconnect container from all networks except default
for net in $(docker inspect -f '{{range $net,$v := .NetworkSettings.Networks}}{{$net}} {{end}}' my-container); do
  [ "$net" != "bridge" ] && docker network disconnect $net my-container
done
```

## ❓ Common Issues

### Issue: "Container name not resolving"

**Problem:** DNS not working between containers

**Check:**
```bash
# Are they on the same custom network?
docker network inspect my-network

# Default bridge doesn't support DNS
# Solution: Create custom network
docker network create my-network
docker network connect my-network container1
docker network connect my-network container2
```

### Issue: "Cannot connect to service on container port"

**Scenarios:**

```bash
# Scenario 1: Trying to access unpublished port from host
docker run -d --name web nginx  # No -p flag
curl localhost:80  # ❌ Fails

# Solution: Publish port
docker run -d --name web -p 8080:80 nginx
curl localhost:8080  # ✅ Works

# Scenario 2: Trying to access between containers on different networks
# Solution: Put on same network

# Scenario 3: Using localhost in container
# Container's localhost is NOT host's localhost!
```

### Issue: "Address already in use"

**Error when publishing ports:**

```bash
# Port 8080 already used
docker run -p 8080:80 nginx
# Error: port is already allocated

# Find what's using it
docker ps | grep 8080

# Use different host port
docker run -p 8081:80 nginx
```

### Issue: Network not found after restart

**Docker networks persist, but:**

```bash
# Custom networks survive daemon restart
docker network ls  # Still there after Docker restart

# But containers must reconnect if network was removed
```

## 🎯 Best Practices

### 1. Use Custom Networks for Applications

```bash
# ✅ GOOD - Custom network with DNS
docker network create my-app
docker run --network my-app --name db postgres
docker run --network my-app --name api my-api

# ❌ AVOID - Default bridge (no DNS)
docker run --name db postgres
docker run --link db my-api  # Legacy linking
```

### 2. Segment by Environment or Function

```bash
# ✅ GOOD - Logical separation
docker network create frontend
docker network create backend
docker network create monitoring

# Frontend tier
docker run --network frontend web

# Backend tier (API on both networks)
docker run --network backend db
docker run --network backend --network frontend api
```

### 3. Don't Publish Database Ports

```bash
# ✅ GOOD - Database not exposed to host
docker run --network backend --name db postgres

# ❌ AVOID - Unnecessary exposure
docker run --network backend --name db -p 5432:5432 postgres
```

### 4. Name Networks Descriptively

```bash
# ✅ GOOD
docker network create myapp-production
docker network create myapp-staging

# ❌ AVOID
docker network create net1
docker network create net2
```

### 5. Clean Up Unused Networks

```bash
# Regular cleanup
docker network prune

# Or during system cleanup
docker system prune -a
```

## 🎉 Lesson Complete!

You now know:

✅ How to create custom Docker networks
✅ Container-to-container communication via DNS
✅ Network isolation and security
✅ Port publishing vs network communication
✅ Multi-tier application networking
✅ Troubleshooting network issues

### What's Next?

**Next Lesson:** [05 - Resource Limits →](05-resource-limits.md)

Learn how to control CPU and memory usage to prevent resource exhaustion!

---

**Lesson Duration:** 20 minutes
**Difficulty:** Intermediate
**Prerequisites:** Lessons 1-3 completed
**Skills:** Container networking, service discovery, isolation
