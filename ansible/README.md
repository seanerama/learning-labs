# Ansible Network Automation Learning Lab

## Overview

This learning lab introduces network engineers to Ansible automation with a focus on network device management, configuration deployment, and operational tasks. You'll learn how to automate common network operations using Ansible's powerful yet simple YAML-based playbooks.

## What You'll Learn

- Ansible fundamentals tailored for network automation
- Network device connection methods (SSH, NETCONF, APIs)
- Configuration management (backups, deployments, rollbacks)
- Template-driven configuration using Jinja2
- Multi-vendor automation (Cisco IOS, NXOS, Arista EOS)
- Compliance checking and auditing workflows
- Best practices for network automation

## Prerequisites

**Required Knowledge:**
- Basic networking concepts (VLANs, routing protocols, ACLs)
- Command-line interface experience
- Basic YAML syntax (we'll cover this)
- SSH connectivity to network devices

**Software Requirements:**
- Linux/WSL2 or macOS environment
- Python 3.8 or higher
- SSH client
- Git (for version control)
- Docker and Docker Compose (optional, for testing environment)

## Quick Start (15 Minutes)

### 1. Install Dependencies

```bash
# Navigate to the ansible lab directory
cd learning-labs/ansible

# Install Python dependencies
pip install -r requirements.txt

# Verify Ansible installation
ansible --version
```

### 2. Configure Your Inventory

Edit the inventory file with your device details:

```bash
# Edit the inventory file
nano inventory/hosts.ini
```

Update with your device IP addresses, usernames, and connection details.

### 3. Test Connectivity

```bash
# Test connection to your devices
ansible routers -m ping -i inventory/hosts.ini

# Gather facts from a device
ansible routers -m cisco.ios.ios_facts -i inventory/hosts.ini
```

### 4. Run Your First Playbook

```bash
# Backup device configurations
ansible-playbook network-demo/playbooks/01-backup-configs.yml

# Check what configurations will be backed up
ls -la network-demo/backups/
```

## Lab Structure

```
ansible/
├── README.md                          # This file
├── ansible-network-guide.md           # Comprehensive guide (start here!)
├── requirements.txt                   # Python dependencies
├── ansible.cfg                        # Ansible configuration
├── inventory/                         # Device inventory files
│   ├── hosts.ini                      # Static inventory (INI format)
│   ├── hosts.yaml                     # Static inventory (YAML format)
│   └── group_vars/                    # Group-specific variables
│       ├── routers.yml
│       └── switches.yml
├── network-demo/                      # Hands-on examples
│   ├── playbooks/                     # Example playbooks
│   │   ├── 01-backup-configs.yml      # Configuration backup
│   │   ├── 02-deploy-vlans.yml        # VLAN provisioning
│   │   ├── 03-update-acls.yml         # ACL deployment
│   │   └── 04-compliance-check.yml    # Compliance auditing
│   ├── roles/                         # Reusable automation roles
│   │   ├── config-backup/
│   │   ├── vlan-provisioning/
│   │   └── compliance/
│   ├── templates/                     # Jinja2 configuration templates
│   │   ├── ios-interface.j2
│   │   ├── ios-vlan.j2
│   │   └── nxos-vlan.j2
│   └── backups/                       # Configuration backup storage
└── test-environment/                  # Containerized test environment
    ├── docker-compose.yml
    └── README.md
```

## Learning Path

We recommend following this progression:

1. **Read the Comprehensive Guide** - Start with [ansible-network-guide.md](ansible-network-guide.md)
2. **Set Up Your Environment** - Install Ansible and configure inventory
3. **Example 1: Backup Configs** - Learn basic playbook structure
4. **Example 2: Deploy VLANs** - Work with templates and variables
5. **Example 3: Update ACLs** - Understand idempotency and change management
6. **Example 4: Compliance Checks** - Build audit and reporting workflows
7. **Build Your Own** - Apply concepts to your real-world scenarios

## Why Ansible for Network Automation?

### Key Benefits

- **Agentless**: No software to install on network devices
- **Simple Syntax**: YAML-based playbooks are human-readable
- **Idempotent**: Safe to re-run without unintended changes
- **Multi-Vendor**: Support for Cisco, Arista, Juniper, and more
- **Version Control**: Infrastructure as Code approach
- **Community**: Large ecosystem of modules and roles

### Common Use Cases

- **Configuration Management**: Standardize device configurations
- **Automated Backups**: Scheduled configuration backups
- **Compliance Checking**: Audit devices against security policies
- **Mass Updates**: Deploy changes across hundreds of devices
- **Provisioning**: Zero-touch deployment of new devices
- **Disaster Recovery**: Rapid device rebuilds from templates

## Getting Help

### Documentation Resources

- [Ansible Network Automation Guide](https://docs.ansible.com/ansible/latest/network/index.html)
- [Cisco IOS Collection](https://galaxy.ansible.com/cisco/ios)
- [Cisco NXOS Collection](https://galaxy.ansible.com/cisco/nxos)
- [Arista EOS Collection](https://galaxy.ansible.com/arista/eos)

### Troubleshooting

**Connection Issues:**
```bash
# Test SSH connectivity manually
ssh admin@192.168.1.1

# Enable verbose mode for debugging
ansible-playbook playbook.yml -vvv
```

**Module Not Found:**
```bash
# Install specific collections
ansible-galaxy collection install cisco.ios
ansible-galaxy collection install cisco.nxos
```

**Authentication Failures:**
- Verify credentials in inventory
- Check that `host_key_checking = False` is set in ansible.cfg
- Ensure device has SSH enabled and accessible

## Next Steps

After completing this lab, explore:

- **Dynamic Inventory**: Integrate with NetBox or other IPAM systems
- **Ansible Tower/AWX**: Web-based UI and API for Ansible
- **CI/CD Integration**: Automated testing with GitLab/GitHub Actions
- **Advanced Error Handling**: Rescue, always, and retry logic
- **Custom Modules**: Write your own Ansible modules in Python

## Contributing

Found an issue or have suggestions? This lab is part of the learning-labs repository. Feel free to submit issues or pull requests.

## License

This learning lab is provided for educational purposes. Refer to the main repository license for details.

---

**Ready to start?** Head over to [ansible-network-guide.md](ansible-network-guide.md) for the comprehensive step-by-step guide!
