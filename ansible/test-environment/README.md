# Ansible Network Lab Test Environment

This directory contains Docker-based test environment configurations for practicing Ansible network automation.

## Prerequisites

- Docker and Docker Compose installed
- At least 8GB of RAM available
- 20GB of free disk space

## Environment Options

### Option 1: Using vrnetlab (Recommended for Real Device Simulation)

1. Build vrnetlab images following the [vrnetlab documentation](https://github.com/vrnetlab/vrnetlab)
2. Update the image names in docker-compose.yml to match your built images
3. Start the environment:

```bash
cd test-environment
docker-compose up -d router1 router2
```

### Option 2: Using GNS3

1. Start GNS3 server:

```bash
docker-compose up -d gns3
```

2. Access GNS3 Web UI at http://localhost:3080
3. Import network device images and create your topology

### Option 3: Using Cisco Modeling Labs (CML)

If you have access to CML (formerly VIRL), you can use it instead of the Docker-based solutions.

## Ansible Control Node

Start the Ansible control container:

```bash
docker-compose up -d ansible-control
```

Access the container:

```bash
docker exec -it lab-ansible-control /bin/bash
```

## Network Automation Development Container

This container includes all necessary tools for network automation:

```bash
docker-compose up -d netauto-dev
docker exec -it lab-netauto-dev /bin/bash
```

### Features:
- Python 3.11
- Ansible and collections
- Network automation libraries (netmiko, napalm, ncclient)
- Jupyter Lab for interactive development
- Common network troubleshooting tools

## Testing Without Real Devices

If you don't have access to real network devices or simulators, you can:

1. Use the playbooks in check mode:
```bash
ansible-playbook playbooks/01-gather-facts.yml --check
```

2. Use mock data for testing templates:
```bash
ansible-playbook playbooks/test-templates.yml --extra-vars "@test-vars.yml"
```

3. Practice with the inventory and variable structure

## Network Topology

```
                    [ansible-control]
                           |
              192.168.1.0/24 Network
                           |
        +------------------+------------------+
        |                  |                  |
   [router1]          [router2]         [netauto-dev]
  192.168.1.1       192.168.1.2         192.168.1.20
```

## Starting the Lab

1. Start all services:
```bash
docker-compose up -d
```

2. Check service status:
```bash
docker-compose ps
```

3. View logs:
```bash
docker-compose logs -f
```

4. Stop the lab:
```bash
docker-compose down
```

## Cleanup

Remove all containers and volumes:
```bash
docker-compose down -v
```

## Troubleshooting

### Containers won't start
- Check Docker resources (CPU/Memory)
- Verify image availability
- Check logs: `docker-compose logs`

### Cannot connect to devices
- Verify device SSH is enabled
- Check network connectivity
- Verify credentials in inventory

### Permission issues
- Ensure Docker has proper privileges
- Check volume mount permissions

## Additional Resources

- [vrnetlab GitHub](https://github.com/vrnetlab/vrnetlab)
- [GNS3 Documentation](https://docs.gns3.com/)
- [Cisco DevNet Sandbox](https://developer.cisco.com/site/sandbox/)
