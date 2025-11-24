# Ansible Network Automation Lab - Structure Overview

This document provides a complete overview of the lab structure and how all components fit together.

## Directory Structure

```
ansible/
├── README.md                      # Main documentation
├── QUICKSTART.md                  # Quick start guide
├── LAB-STRUCTURE.md              # This file
├── ansible-network-guide.md       # Comprehensive network automation guide
├── setup.sh                       # Automated setup script
├── requirements.txt               # Python dependencies
├── ansible.cfg                    # Ansible configuration
├── .gitignore                     # Git ignore patterns
│
├── inventory/                     # Inventory and variables
│   ├── hosts.ini                 # Main inventory file
│   ├── group_vars/               # Group-specific variables
│   │   ├── all.yml              # Variables for all hosts
│   │   ├── routers.yml          # Router-specific variables
│   │   ├── switches.yml         # Switch-specific variables
│   │   └── vault.yml            # Encrypted credentials
│   └── host_vars/                # Host-specific variables
│       └── core-rtr-01.yml      # Example host variables
│
├── playbooks/                     # Ansible playbooks
│   ├── 01-gather-facts.yml       # Gather device information
│   ├── 02-backup-configs.yml     # Backup configurations
│   ├── 03-configure-vlans.yml    # Configure VLANs
│   ├── 04-base-config.yml        # Apply base configuration
│   ├── 05-compliance-check.yml   # Check compliance
│   ├── 06-interface-audit.yml    # Audit interfaces
│   ├── use-backup-role.yml       # Use backup role
│   ├── use-vlan-role.yml         # Use VLAN role
│   ├── use-compliance-role.yml   # Use compliance role
│   └── full-deployment.yml       # Complete deployment workflow
│
├── roles/                         # Ansible roles
│   ├── config-backup/            # Configuration backup role
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   ├── defaults/
│   │   │   └── main.yml
│   │   ├── templates/
│   │   ├── vars/
│   │   ├── handlers/
│   │   └── meta/
│   │       └── main.yml
│   │
│   ├── vlan-provisioning/        # VLAN provisioning role
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   ├── defaults/
│   │   │   └── main.yml
│   │   ├── templates/
│   │   ├── vars/
│   │   ├── handlers/
│   │   └── meta/
│   │       └── main.yml
│   │
│   └── compliance-check/         # Compliance checking role
│       ├── tasks/
│       │   └── main.yml
│       ├── defaults/
│       │   └── main.yml
│       ├── templates/
│       ├── vars/
│       ├── handlers/
│       └── meta/
│           └── main.yml
│
├── templates/                     # Jinja2 templates
│   ├── base-config.j2            # Base configuration template
│   ├── interface-config.j2       # Interface configuration template
│   ├── vlan-config.j2            # VLAN configuration template
│   └── compliance-report.j2      # Compliance report template
│
├── collections/                   # Ansible collections
│   └── requirements.yml          # Collection requirements
│
├── test-environment/             # Test environment
│   ├── docker-compose.yml        # Docker compose configuration
│   ├── Dockerfile.netauto        # Network automation container
│   └── README.md                 # Test environment guide
│
├── logs/                          # Log files
│   └── .gitkeep
│
├── backups/                       # Configuration backups
│   └── .gitkeep
│
├── facts/                         # Device facts
│   └── .gitkeep
│
├── audit/                         # Audit reports
│   └── .gitkeep
│
└── compliance/                    # Compliance reports
    └── .gitkeep
```

## Component Overview

### 1. Configuration Files

#### ansible.cfg
- Main Ansible configuration
- Sets inventory location, connection settings, logging
- Configures SSH parameters for network devices
- Defines privilege escalation settings

#### requirements.txt
- Python package dependencies
- Includes Ansible, network libraries (netmiko, napalm)
- Testing and linting tools

### 2. Inventory

#### hosts.ini
- Defines network device groups (routers, switches, firewalls)
- Contains device IP addresses
- Sets connection parameters

#### group_vars/
- **all.yml**: Variables for all devices (DNS, NTP, domain)
- **routers.yml**: Router-specific variables (routing, interfaces)
- **switches.yml**: Switch-specific variables (VLANs, ports)
- **vault.yml**: Encrypted credentials

#### host_vars/
- Device-specific variables
- Override group variables when needed

### 3. Playbooks

Playbooks are organized by function:

1. **Gather Facts** (`01-gather-facts.yml`)
   - Collects device information
   - Saves facts to JSON files

2. **Backup Configs** (`02-backup-configs.yml`)
   - Creates timestamped backups
   - Saves running and startup configs

3. **Configure VLANs** (`03-configure-vlans.yml`)
   - Creates VLANs on switches
   - Configures trunk and access ports

4. **Base Config** (`04-base-config.yml`)
   - Applies common settings (hostname, DNS, NTP, SSH)
   - Configures logging and banners

5. **Compliance Check** (`05-compliance-check.yml`)
   - Validates configuration compliance
   - Generates compliance reports

6. **Interface Audit** (`06-interface-audit.yml`)
   - Audits interface status
   - Identifies down interfaces

7. **Role-based Playbooks** (`use-*-role.yml`)
   - Demonstrate role usage
   - Simplified playbook syntax

8. **Full Deployment** (`full-deployment.yml`)
   - Complete workflow example
   - Uses multiple roles and tasks

### 4. Roles

#### config-backup
**Purpose**: Backup network device configurations

**Tasks**:
- Create timestamped backup directories
- Backup running and startup configs
- Generate metadata files
- Maintain backup index

**Variables**:
- `backup_root_dir`: Root directory for backups
- `backup_retention_days`: How long to keep backups
- `include_startup_config`: Whether to backup startup config

#### vlan-provisioning
**Purpose**: Provision VLANs on switches

**Tasks**:
- Create VLANs
- Configure trunk interfaces
- Configure access interfaces
- Set spanning-tree parameters
- Verify configuration

**Variables**:
- `vlans`: List of VLANs to create
- `trunk_interfaces`: List of trunk ports
- `access_interfaces`: List of access ports
- `stp_mode`: Spanning tree mode

#### compliance-check
**Purpose**: Verify configuration compliance

**Tasks**:
- Check various configuration aspects
- Calculate compliance score
- Generate detailed reports
- Optionally enforce compliance

**Variables**:
- `compliance_threshold`: Minimum acceptable score
- `enforce_compliance`: Fail if below threshold
- `compliance_dir`: Report output directory

### 5. Templates

#### base-config.j2
- Base device configuration
- Uses variables for DNS, NTP, logging, SSH, banners

#### interface-config.j2
- Interface configuration
- Supports L2 and L3 interfaces
- Dynamic based on inventory variables

#### vlan-config.j2
- VLAN database configuration
- Trunk and access port configuration
- Spanning-tree settings

#### compliance-report.j2
- Formatted compliance report
- Shows pass/fail for each check
- Includes recommendations

### 6. Test Environment

#### docker-compose.yml
- Defines lab network topology
- Includes network device simulators
- Ansible control node
- Development container

#### Dockerfile.netauto
- Network automation development environment
- Pre-installed tools and libraries
- Jupyter Lab for interactive work

## Workflow Examples

### Basic Workflow

1. **Gather Facts**
   ```bash
   ansible-playbook playbooks/01-gather-facts.yml
   ```

2. **Backup Configs**
   ```bash
   ansible-playbook playbooks/02-backup-configs.yml
   ```

3. **Apply Changes**
   ```bash
   ansible-playbook playbooks/04-base-config.yml
   ```

4. **Verify Compliance**
   ```bash
   ansible-playbook playbooks/05-compliance-check.yml
   ```

### Using Roles

```bash
# Backup using role
ansible-playbook playbooks/use-backup-role.yml

# Provision VLANs using role
ansible-playbook playbooks/use-vlan-role.yml --limit switches

# Check compliance using role
ansible-playbook playbooks/use-compliance-role.yml
```

### Complete Deployment

```bash
# Full deployment with all roles
ansible-playbook playbooks/full-deployment.yml
```

## Data Flow

```
Inventory (hosts.ini)
    ↓
Group Variables (group_vars/)
    ↓
Host Variables (host_vars/)
    ↓
Playbook
    ↓
Role Tasks
    ↓
Templates (rendered with variables)
    ↓
Network Device
    ↓
Output (logs, backups, reports)
```

## Best Practices Implemented

1. **Separation of Concerns**
   - Inventory separate from playbooks
   - Variables organized by group/host
   - Roles for reusable functionality

2. **Security**
   - Credentials in vault.yml
   - Vault password file excluded from git
   - SSH keys recommended over passwords

3. **Maintainability**
   - Consistent naming conventions
   - Documentation for all components
   - Modular design with roles

4. **Observability**
   - Logging enabled
   - Backup tracking
   - Compliance reporting
   - Audit trails

5. **Testing**
   - Check mode support
   - Diff mode support
   - Test environment available
   - Syntax validation

## Customization Guide

### Adding a New Device Type

1. Create group in `inventory/hosts.ini`
2. Add group_vars file in `inventory/group_vars/`
3. Create device-specific playbook or update existing
4. Add any required templates

### Creating a New Role

```bash
# Create role structure
mkdir -p roles/my-role/{tasks,defaults,templates,handlers,meta}

# Create main task file
touch roles/my-role/tasks/main.yml

# Create defaults
touch roles/my-role/defaults/main.yml

# Create metadata
touch roles/my-role/meta/main.yml
```

### Adding a New Playbook

1. Create playbook in `playbooks/` directory
2. Define hosts, connection method, and tasks
3. Use roles where appropriate
4. Add to documentation

## Output Locations

- **Logs**: `logs/ansible.log`
- **Backups**: `backups/YYYYMMDD-HHMMSS/`
- **Facts**: `facts/<hostname>_facts.json`
- **Compliance**: `compliance/<hostname>_compliance_<timestamp>.txt`
- **Audit**: `audit/<hostname>_audit_<timestamp>.txt`

## Getting Help

1. Read [README.md](README.md) for overview
2. Follow [QUICKSTART.md](QUICKSTART.md) for setup
3. Study [ansible-network-guide.md](ansible-network-guide.md) for details
4. Examine example playbooks in `playbooks/`
5. Review role documentation in `roles/*/README.md`

## Contributing

To add or improve lab components:

1. Follow existing structure and naming conventions
2. Document all variables and their purposes
3. Include examples in playbooks
4. Test thoroughly before committing
5. Update this document if structure changes
