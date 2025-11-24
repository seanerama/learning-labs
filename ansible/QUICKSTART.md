# Quick Start Guide

This guide will help you get started with the Ansible Network Automation Lab quickly.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Access to network devices (or use the test environment)

## Installation Steps

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Ansible Collections

```bash
ansible-galaxy collection install -r collections/requirements.yml
```

### 3. Configure Credentials

#### Option A: Using Ansible Vault (Recommended)

```bash
# Create vault password file (keep this secure!)
echo "your-vault-password" > .vault_pass
chmod 600 .vault_pass

# Encrypt the vault file
ansible-vault encrypt inventory/group_vars/vault.yml
```

#### Option B: Environment Variables

```bash
export ANSIBLE_NET_USERNAME=admin
export ANSIBLE_NET_PASSWORD=cisco123
```

### 4. Update Inventory

Edit `inventory/hosts.ini` with your actual device IP addresses:

```ini
[routers]
my-router-1 ansible_host=10.0.0.1
my-router-2 ansible_host=10.0.0.2
```

### 5. Test Connectivity

```bash
# Ping test
ansible network -m ping -i inventory/hosts.ini

# Or run the gather facts playbook
ansible-playbook playbooks/01-gather-facts.yml
```

## Running Your First Playbook

### Gather Device Facts

```bash
ansible-playbook playbooks/01-gather-facts.yml
```

### Backup Configurations

```bash
ansible-playbook playbooks/02-backup-configs.yml
```

### Apply Base Configuration

```bash
ansible-playbook playbooks/04-base-config.yml
```

### Configure VLANs (Switches Only)

```bash
ansible-playbook playbooks/03-configure-vlans.yml
```

### Run Compliance Check

```bash
ansible-playbook playbooks/05-compliance-check.yml
```

## Using Roles

Roles provide reusable configuration patterns:

### Backup Configurations

```bash
ansible-playbook playbooks/use-backup-role.yml
```

### Provision VLANs

```bash
ansible-playbook playbooks/use-vlan-role.yml
```

### Check Compliance

```bash
ansible-playbook playbooks/use-compliance-role.yml
```

### Full Deployment

```bash
ansible-playbook playbooks/full-deployment.yml
```

## Working with Specific Devices

### Target specific hosts

```bash
ansible-playbook playbooks/01-gather-facts.yml --limit router1
```

### Target specific groups

```bash
ansible-playbook playbooks/03-configure-vlans.yml --limit switches
```

## Check Mode (Dry Run)

Test playbooks without making changes:

```bash
ansible-playbook playbooks/04-base-config.yml --check
```

## Diff Mode

See what changes will be made:

```bash
ansible-playbook playbooks/04-base-config.yml --check --diff
```

## Verbose Output

For debugging:

```bash
ansible-playbook playbooks/01-gather-facts.yml -v    # Verbose
ansible-playbook playbooks/01-gather-facts.yml -vv   # More verbose
ansible-playbook playbooks/01-gather-facts.yml -vvv  # Very verbose
```

## Using the Test Environment

If you don't have physical devices:

```bash
cd test-environment
docker-compose up -d
```

See [test-environment/README.md](test-environment/README.md) for details.

## Common Tasks

### Create a Backup Before Changes

```bash
ansible-playbook playbooks/use-backup-role.yml
```

### View Backup Files

```bash
ls -R backups/
```

### View Compliance Reports

```bash
cat compliance/*_compliance_*.txt
```

### View Audit Reports

```bash
cat audit/*_audit_*.txt
```

## Troubleshooting

### Connection Issues

1. Verify device reachability:
```bash
ping <device-ip>
```

2. Test SSH manually:
```bash
ssh admin@<device-ip>
```

3. Check Ansible connection:
```bash
ansible network -m ping -i inventory/hosts.ini -vvv
```

### Authentication Issues

1. Verify credentials in `inventory/group_vars/vault.yml`
2. Check SSH key authentication
3. Verify enable password if using privilege escalation

### Module Not Found

Install missing collections:
```bash
ansible-galaxy collection install cisco.ios
```

### Playbook Syntax Errors

Validate playbook syntax:
```bash
ansible-playbook playbooks/01-gather-facts.yml --syntax-check
```

## Next Steps

1. Read the [ansible-network-guide.md](ansible-network-guide.md) for detailed information
2. Customize inventory variables for your environment
3. Modify playbooks to match your requirements
4. Create custom roles for your specific use cases
5. Set up scheduled backups using cron or CI/CD

## Getting Help

- Check the main [README.md](README.md)
- Review the [ansible-network-guide.md](ansible-network-guide.md)
- Ansible Documentation: https://docs.ansible.com/
- Ansible Network Automation: https://docs.ansible.com/ansible/latest/network/index.html

## Best Practices

1. Always backup configurations before making changes
2. Test in check mode first
3. Use version control for your playbooks
4. Keep credentials encrypted with Ansible Vault
5. Document your changes
6. Start with small, incremental changes
7. Verify changes after applying them
