# Simple Containerlab Lab - Getting Started

A beginner-friendly containerlab topology for learning container-based networking fundamentals.

## Overview

This lab creates a simple 3-node network topology to help you get familiar with containerlab. The topology consists of:

```
┌──────────┐                ┌──────────┐                ┌──────────┐
│ client1  │────────────────│  router  │────────────────│ server1  │
│192.168.1.10│             │192.168.1.1│              │192.168.2.10│
└──────────┘   192.168.1.0/24 │192.168.2.1│ 192.168.2.0/24 └──────────┘
                              └──────────┘
```

## Learning Objectives

After completing this lab, you will understand:
- How to define network topologies using containerlab
- How to deploy and manage containerized network labs
- Basic Linux routing and networking concepts
- How to connect and test network connectivity between containers

## Prerequisites

- Linux system (Ubuntu, Debian, RHEL, etc.)
- Docker installed and running
- Root/sudo access
- Basic understanding of networking concepts (IP addresses, routing)

## Installation

### Install Docker (if not already installed)

```bash
# For Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker
```

### Install Containerlab

```bash
# Download and install the latest version
bash -c "$(curl -sL https://get.containerlab.dev)"

# Verify installation
containerlab version
```

## Lab Topology

The lab consists of three Alpine Linux containers:

| Node    | Role   | IP Address(es)                    | Description                          |
|---------|--------|-----------------------------------|--------------------------------------|
| client1 | Client | 192.168.1.10/24                   | Simulates a client machine           |
| router  | Router | 192.168.1.1/24, 192.168.2.1/24    | Routes traffic between networks      |
| server1 | Server | 192.168.2.10/24                   | Simulates a server machine           |

## Quick Start

### 1. Deploy the Lab

```bash
sudo containerlab deploy -t simple-lab.clab.yml
```

You should see output indicating the containers are being created and connected.

### 2. Verify Deployment

```bash
# View lab status
sudo containerlab inspect -t simple-lab.clab.yml

# List running containers
sudo docker ps
```

### 3. Access Nodes

You can access any node using docker exec:

```bash
# Access client1
sudo docker exec -it clab-simple-lab-client1 sh

# Access router
sudo docker exec -it clab-simple-lab-router sh

# Access server1
sudo docker exec -it clab-simple-lab-server1 sh
```

## Testing and Verification

### Test Basic Connectivity

**From client1 to router:**

```bash
sudo docker exec -it clab-simple-lab-client1 sh
# Inside the container:
ping -c 4 192.168.1.1
ip route
exit
```

**From client1 to server1 (through router):**

```bash
sudo docker exec -it clab-simple-lab-client1 sh
# Inside the container:
ping -c 4 192.168.2.10
traceroute 192.168.2.10
exit
```

### Verify Routing

**Check router's IP forwarding:**

```bash
sudo docker exec -it clab-simple-lab-router sh
# Inside the container:
cat /proc/sys/net/ipv4/ip_forward  # Should return 1
ip addr  # Should show both eth1 and eth2 with IPs
ip route
exit
```

### Test Bidirectional Communication

**From server1 to client1:**

```bash
sudo docker exec -it clab-simple-lab-server1 sh
# Inside the container:
ping -c 4 192.168.1.10
exit
```

## Visualize Your Topology

Containerlab can generate a visual graph of your topology:

```bash
sudo containerlab graph -t simple-lab.clab.yml
```

This will start a web server (usually on http://localhost:50080) where you can see your topology visualized.

## Common Tasks

### View Logs

```bash
# View container logs
sudo docker logs clab-simple-lab-client1
sudo docker logs clab-simple-lab-router
sudo docker logs clab-simple-lab-server1
```

### Save Configuration

```bash
# Save the current state of the lab
sudo containerlab save -t simple-lab.clab.yml
```

### Restart a Single Node

```bash
# Restart just one container
sudo docker restart clab-simple-lab-router
```

### View Network Interfaces

```bash
# Inside any container
ip addr show
ip link show
```

## Experiments to Try

### 1. Install and Test Services

**Run a web server on server1:**

```bash
sudo docker exec -it clab-simple-lab-server1 sh
# Inside server1:
apk add python3
python3 -m http.server 8080 &
exit

# From client1, test the web server
sudo docker exec -it clab-simple-lab-client1 sh
apk add curl
curl http://192.168.2.10:8080
exit
```

### 2. Add Firewall Rules

**Block ICMP (ping) on the router:**

```bash
sudo docker exec -it clab-simple-lab-router sh
# Inside router:
apk add iptables
iptables -A FORWARD -p icmp -j DROP
exit

# Now try pinging from client1 to server1 - it should fail
```

### 3. Monitor Traffic

**Capture packets on the router:**

```bash
sudo docker exec -it clab-simple-lab-router sh
# Inside router:
apk add tcpdump
tcpdump -i eth1 -n
# In another terminal, generate traffic from client1
exit
```

### 4. Test Connectivity Issues

**Simulate a network failure:**

```bash
# Disconnect server1 from the network
sudo docker network disconnect clab clab-simple-lab-server1

# Try pinging from client1 - should fail
# Reconnect it
sudo docker network connect clab clab-simple-lab-server1
```

## Cleanup

### Destroy the Lab

When you're done, destroy the lab to remove all containers and networks:

```bash
sudo containerlab destroy -t simple-lab.clab.yml
```

This will:
- Stop all containers
- Remove all containers
- Clean up the network connections

## Troubleshooting

### Issue: Cannot ping between nodes

**Solution:**
- Verify IP addresses are configured: `ip addr`
- Check routing tables: `ip route`
- Ensure IP forwarding is enabled on router: `cat /proc/sys/net/ipv4/ip_forward`

### Issue: Containers won't start

**Solution:**
- Check Docker is running: `sudo systemctl status docker`
- Verify images are pulled: `sudo docker images`
- Check for port conflicts or naming conflicts

### Issue: "Permission denied" errors

**Solution:**
- Containerlab requires root privileges
- Always use `sudo` with containerlab commands

### Issue: Cannot access containers

**Solution:**
- Verify containers are running: `sudo docker ps`
- Check container names match the expected format: `clab-simple-lab-<nodename>`

## Understanding the Topology File

The `simple-lab.clab.yml` file defines your entire lab. Here's what each section does:

```yaml
name: simple-lab           # Lab name (used as prefix for containers)

topology:
  nodes:                   # Define all nodes in the lab
    client1:
      kind: linux          # Type of node (linux, ceos, srl, etc.)
      image: alpine:latest # Docker image to use
      exec:                # Commands to run at startup
        - ip addr add ...  # Configure IP address
        - ip route add ... # Add routing entry

  links:                   # Define connections between nodes
    - endpoints: ["client1:eth1", "router:eth1"]
```

## Next Steps

Once you're comfortable with this lab, try:

1. **Add More Nodes**: Create a 4-node topology with multiple clients
2. **Use Different Images**: Try Ubuntu, Debian, or network OS containers
3. **Complex Topologies**: Build a multi-tier network with DMZ
4. **Network OS Labs**: Explore Nokia SR Linux, Arista cEOS, or other network operating systems
5. **Automation**: Write scripts to automatically configure and test your labs

## Resources

- [Containerlab Official Documentation](https://containerlab.dev/)
- [Containerlab GitHub](https://github.com/srl-labs/containerlab)
- [Lab Examples](https://containerlab.dev/lab-examples/lab-examples/)
- [Discord Community](https://discord.gg/vAyddtaEV9)

## License

This lab is provided as-is for educational purposes.

## Contributing

Feel free to modify and extend this lab for your learning needs!
