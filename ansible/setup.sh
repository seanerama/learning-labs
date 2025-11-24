#!/bin/bash
# Ansible Network Lab Setup Script

set -e

echo "================================================"
echo "Ansible Network Automation Lab Setup"
echo "================================================"
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check for pip
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed"
    exit 1
fi

echo "✓ pip3 found"

# Install Python requirements
echo ""
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Check for ansible
if ! command -v ansible &> /dev/null; then
    echo "Error: Ansible installation failed"
    exit 1
fi

echo "✓ Ansible installed: $(ansible --version | head -n1)"

# Install Ansible collections
echo ""
echo "Installing Ansible collections..."
ansible-galaxy collection install -r collections/requirements.yml

# Create necessary directories
echo ""
echo "Creating working directories..."
mkdir -p logs backups facts audit compliance

echo "✓ Directories created"

# Create placeholder files to track directories in git
touch logs/.gitkeep
touch backups/.gitkeep
touch facts/.gitkeep
touch audit/.gitkeep
touch compliance/.gitkeep

# Set up vault password file prompt
echo ""
echo "================================================"
echo "Vault Configuration"
echo "================================================"
read -p "Do you want to set up Ansible Vault? (y/n): " setup_vault

if [[ $setup_vault == "y" || $setup_vault == "Y" ]]; then
    read -sp "Enter vault password: " vault_password
    echo ""
    echo "$vault_password" > .vault_pass
    chmod 600 .vault_pass
    echo "✓ Vault password file created"

    read -p "Do you want to encrypt the vault.yml file now? (y/n): " encrypt_vault
    if [[ $encrypt_vault == "y" || $encrypt_vault == "Y" ]]; then
        ansible-vault encrypt inventory/group_vars/vault.yml
        echo "✓ vault.yml encrypted"
    fi
fi

# Verify setup
echo ""
echo "================================================"
echo "Verifying Installation"
echo "================================================"

# Test ansible-playbook
echo "Testing ansible-playbook..."
ansible-playbook playbooks/01-gather-facts.yml --syntax-check
echo "✓ Playbook syntax check passed"

# Display installed collections
echo ""
echo "Installed Collections:"
ansible-galaxy collection list | grep -E "(cisco|arista|juniper|netcommon)"

# Setup complete
echo ""
echo "================================================"
echo "Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Edit inventory/hosts.ini with your device information"
echo "2. Update inventory/group_vars/ with your environment variables"
echo "3. Run 'ansible-playbook playbooks/01-gather-facts.yml' to test"
echo ""
echo "Quick reference:"
echo "  - Quick Start: cat QUICKSTART.md"
echo "  - Main README: cat README.md"
echo "  - Network Guide: cat ansible-network-guide.md"
echo ""
echo "Happy automating! 🚀"
