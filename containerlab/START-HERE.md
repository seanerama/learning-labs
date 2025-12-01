# Containerlab - Start Here

Welcome to the Containerlab learning lab! This lab teaches you how to build and manage container-based network topologies.

## What is Containerlab?

Containerlab is a powerful tool for creating network lab environments using containers. Instead of spinning up heavy virtual machines, you can define entire network topologies in simple YAML files and deploy them in seconds.

**Why Containerlab?**
- Fast deployment (seconds vs. minutes for VMs)
- Low resource usage
- Easy topology definition with YAML
- Supports real network operating systems (Arista cEOS, Nokia SR Linux, etc.)
- Perfect for learning, testing, and CI/CD

## What You'll Learn

In this lab, you'll:
1. Install and configure Containerlab
2. Deploy a simple 3-node network topology
3. Configure IP addressing and routing
4. Test connectivity between containers
5. Experiment with network services and troubleshooting

## Lab Overview

```
┌──────────┐                ┌──────────┐                ┌──────────┐
│ client1  │────────────────│  router  │────────────────│ server1  │
│192.168.1.10│             │192.168.1.1│              │192.168.2.10│
└──────────┘   192.168.1.0/24 │192.168.2.1│ 192.168.2.0/24 └──────────┘
                              └──────────┘
```

You'll build this simple network:
- **client1** - A client machine on the 192.168.1.0/24 network
- **router** - Routes traffic between both networks
- **server1** - A server on the 192.168.2.0/24 network

## Time Estimate

| Section | Duration |
|---------|----------|
| Installation | 15 minutes |
| Deploy & Explore | 30 minutes |
| Testing & Verification | 30 minutes |
| Experiments | 45 minutes |
| **Total** | **~2 hours** |

## Prerequisites

Before starting, ensure you have:
- [ ] Linux system (Ubuntu, Debian, RHEL, or similar)
- [ ] Root/sudo access
- [ ] Basic networking knowledge (IP addresses, subnets, routing)
- [ ] Completed the Docker Basics lab (recommended)

## Files in This Lab

```
containerlab/
├── START-HERE.md           ← You are here
├── QUICKSTART.md           ← Installation guide
├── README.md               ← Full lab instructions
└── simple-lab.clab.yml     ← Topology definition file
```

## Getting Started

1. **Read QUICKSTART.md** - Install Docker and Containerlab
2. **Follow README.md** - Step-by-step lab instructions
3. **Experiment** - Try the suggested exercises

## Quick Commands

```bash
# Deploy the lab
sudo containerlab deploy -t simple-lab.clab.yml

# Check lab status
sudo containerlab inspect -t simple-lab.clab.yml

# Access a node
sudo docker exec -it clab-simple-lab-client1 sh

# Destroy the lab
sudo containerlab destroy -t simple-lab.clab.yml
```

## Learning Outcomes

After completing this lab, you will be able to:
- ✅ Define network topologies using YAML
- ✅ Deploy containerized network environments
- ✅ Configure IP addressing and routing in containers
- ✅ Test and troubleshoot network connectivity
- ✅ Use tcpdump and other network tools in containers
- ✅ Build more complex lab environments

## Next Steps

After this lab, consider:
- Building more complex multi-tier topologies
- Using network OS containers (Arista cEOS, Nokia SR Linux)
- Integrating with the Ansible lab for automation
- Creating CI/CD pipelines for network testing

---

**Ready to begin?** Start with [QUICKSTART.md](QUICKSTART.md) to install the prerequisites!
