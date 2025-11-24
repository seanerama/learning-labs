# Ansible Network Automation Guide

## Introduction

Network automation with Ansible enables you to automate configuration, deployment, and management of network devices. This guide covers essential concepts, modules, and best practices for network automation.

## Network Modules Overview

### Connection Methods

Ansible supports multiple connection methods for network devices:

- **network_cli**: SSH-based connection for CLI configuration
- **netconf**: NETCONF protocol for devices supporting it
- **httpapi**: REST API based connection
- **local**: Runs on control node (legacy, deprecated)

### Common Network Platforms

- Cisco IOS/IOS-XE
- Cisco NX-OS
- Arista EOS
- Juniper Junos
- Palo Alto PAN-OS
- F5 BIG-IP

## Basic Network Playbook Structure

```yaml
---
- name: Network Configuration Example
  hosts: network_devices
  gather_facts: no
  connection: network_cli

  tasks:
    - name: Configure interface
      ios_interface:
        name: GigabitEthernet0/1
        description: "Uplink to Core"
        enabled: true
```

## Inventory Configuration

### Host Variables for Network Devices

```ini
[routers]
router1 ansible_host=192.168.1.1
router2 ansible_host=192.168.1.2

[routers:vars]
ansible_connection=network_cli
ansible_network_os=ios
ansible_user=admin
ansible_password="{{ vault_network_password }}"
ansible_become=yes
ansible_become_method=enable
```

### Using Group Variables

```yaml
# group_vars/routers.yml
---
ansible_connection: network_cli
ansible_network_os: ios
ansible_user: admin
ansible_become: yes
ansible_become_method: enable
```

## Common Network Tasks

### 1. Gathering Facts

```yaml
- name: Gather device facts
  ios_facts:
    gather_subset:
      - hardware
      - interfaces

- name: Display facts
  debug:
    var: ansible_net_version
```

### 2. Configuring Interfaces

```yaml
- name: Configure interface settings
  ios_interface:
    name: GigabitEthernet0/1
    description: "Uplink Interface"
    enabled: true
    speed: 1000
    duplex: full
    mtu: 1500
    state: present

- name: Configure IP address
  ios_l3_interface:
    name: GigabitEthernet0/1
    ipv4: 192.168.1.1/24
    state: present
```

### 3. Managing VLANs

```yaml
- name: Create VLAN
  ios_vlan:
    vlan_id: 100
    name: "Production VLAN"
    state: present

- name: Configure trunk port
  ios_l2_interface:
    name: GigabitEthernet0/2
    mode: trunk
    trunk_allowed_vlans: 10,20,30,100
```

### 4. Static Routing

```yaml
- name: Configure static route
  ios_static_route:
    prefix: 10.0.0.0
    mask: 255.255.255.0
    next_hop: 192.168.1.254
    state: present
```

### 5. Using Config Module

```yaml
- name: Configure using raw commands
  ios_config:
    lines:
      - ip domain-name example.com
      - ip name-server 8.8.8.8
      - ip name-server 8.8.4.4
    save_when: changed

- name: Configure with parent context
  ios_config:
    lines:
      - description Configured by Ansible
      - ip address 192.168.1.1 255.255.255.0
      - no shutdown
    parents: interface GigabitEthernet0/1
```

### 6. Backup Configurations

```yaml
- name: Backup device configuration
  ios_config:
    backup: yes
    backup_options:
      filename: "{{ inventory_hostname }}_config.txt"
      dir_path: ./backups/

- name: Save running config
  ios_command:
    commands:
      - write memory
```

## Advanced Techniques

### Using Templates for Network Configs

```yaml
# playbook
- name: Apply interface configuration from template
  ios_config:
    src: interface_template.j2
  notify: save config

# templates/interface_template.j2
{% for interface in interfaces %}
interface {{ interface.name }}
 description {{ interface.description }}
 ip address {{ interface.ip }} {{ interface.mask }}
 no shutdown
{% endfor %}
```

### Conditional Configuration

```yaml
- name: Configure OSPF on routers
  ios_config:
    lines:
      - network {{ item.network }} {{ item.wildcard }} area {{ item.area }}
    parents: router ospf {{ ospf_process_id }}
  loop: "{{ ospf_networks }}"
  when: routing_protocol == "ospf"
```

### Configuration Validation

```yaml
- name: Configure interface and verify
  block:
    - name: Apply configuration
      ios_config:
        lines:
          - ip address 192.168.1.1 255.255.255.0
          - no shutdown
        parents: interface GigabitEthernet0/1

    - name: Verify interface is up
      ios_command:
        commands:
          - show interface GigabitEthernet0/1 | include line protocol
      register: interface_status

    - name: Assert interface is operational
      assert:
        that:
          - "'line protocol is up' in interface_status.stdout[0]"
        fail_msg: "Interface did not come up"
  rescue:
    - name: Rollback configuration
      ios_config:
        lines:
          - shutdown
        parents: interface GigabitEthernet0/1
```

## Network-Specific Collections

### Installing Network Collections

```bash
ansible-galaxy collection install cisco.ios
ansible-galaxy collection install cisco.nxos
ansible-galaxy collection install arista.eos
ansible-galaxy collection install junipernetworks.junos
```

### Using Collection Modules

```yaml
---
- name: Using Cisco IOS Collection
  hosts: ios_devices
  gather_facts: no

  collections:
    - cisco.ios

  tasks:
    - name: Configure interface using collection
      ios_interfaces:
        config:
          - name: GigabitEthernet0/1
            description: "Managed by Ansible"
            enabled: true
```

## Multi-Vendor Playbooks

```yaml
---
- name: Configure all network devices
  hosts: network
  gather_facts: no

  tasks:
    - name: Configure Cisco IOS devices
      cisco.ios.ios_interface:
        name: "{{ interface_name }}"
        description: "{{ interface_description }}"
      when: ansible_network_os == 'ios'

    - name: Configure Arista EOS devices
      arista.eos.eos_interfaces:
        config:
          - name: "{{ interface_name }}"
            description: "{{ interface_description }}"
      when: ansible_network_os == 'eos'
```

## Error Handling and Debugging

### Enable Debugging

```bash
ansible-playbook -vvv network_playbook.yml
```

### Handling Connection Errors

```yaml
- name: Attempt configuration with retry
  ios_config:
    lines:
      - ip domain-name example.com
  retries: 3
  delay: 10
  register: result
  until: result is succeeded
```

### Using Wait_for for Device Reachability

```yaml
- name: Wait for device to be reachable
  wait_for:
    host: "{{ ansible_host }}"
    port: 22
    delay: 10
    timeout: 300
  delegate_to: localhost
```

## Security Best Practices

### 1. Use Ansible Vault for Credentials

```bash
# Create encrypted file
ansible-vault create group_vars/network/vault.yml

# Content of vault.yml
vault_network_password: secretpassword
vault_enable_password: enablesecret
```

### 2. Reference Vault Variables

```yaml
# group_vars/network/vars.yml
ansible_password: "{{ vault_network_password }}"
ansible_become_password: "{{ vault_enable_password }}"
```

### 3. Limit Privilege Escalation

```yaml
- name: Tasks that don't need privilege
  ios_facts:
    gather_subset: min

- name: Task requiring privilege
  ios_config:
    lines:
      - username ansible privilege 15 secret ansible123
  become: yes
```

## Performance Optimization

### 1. Disable Fact Gathering

```yaml
---
- name: Network Playbook
  hosts: network
  gather_facts: no  # Network devices don't support setup module
```

### 2. Use Strategy Plugins

```yaml
---
- name: Parallel network configuration
  hosts: network
  strategy: free
  gather_facts: no
```

### 3. Async Tasks for Long Operations

```yaml
- name: Upgrade IOS image
  ios_command:
    commands:
      - archive download-sw /overwrite /reload tftp://server/image.bin
  async: 3600
  poll: 0
  register: upgrade_job

- name: Check upgrade status
  async_status:
    jid: "{{ upgrade_job.ansible_job_id }}"
  register: job_result
  until: job_result.finished
  retries: 360
  delay: 10
```

## Common Patterns and Examples

### Network Audit Playbook

```yaml
---
- name: Network Device Audit
  hosts: network
  gather_facts: no

  tasks:
    - name: Gather device information
      ios_facts:
        gather_subset: all

    - name: Create audit report
      template:
        src: audit_report.j2
        dest: "./reports/{{ inventory_hostname }}_audit.txt"
      delegate_to: localhost

    - name: Check NTP configuration
      ios_command:
        commands: show ntp status
      register: ntp_status

    - name: Verify DNS servers
      ios_command:
        commands: show run | include name-server
      register: dns_config
```

### Configuration Compliance Check

```yaml
---
- name: Check Configuration Compliance
  hosts: network
  gather_facts: no

  tasks:
    - name: Check if logging is configured
      ios_command:
        commands: show run | include logging
      register: logging_config

    - name: Verify required logging
      assert:
        that:
          - "'logging {{ syslog_server }}' in logging_config.stdout[0]"
        fail_msg: "Logging not properly configured"

    - name: Check AAA configuration
      ios_command:
        commands: show run | section aaa
      register: aaa_config

    - name: Create compliance report
      copy:
        content: |
          Device: {{ inventory_hostname }}
          Compliance Status: {{ 'PASS' if aaa_config.stdout[0] else 'FAIL' }}
          Logging: {{ logging_config.stdout[0] }}
          AAA: {{ aaa_config.stdout[0] }}
        dest: "./compliance/{{ inventory_hostname }}.txt"
      delegate_to: localhost
```

### Rolling Update Pattern

```yaml
---
- name: Rolling Network Update
  hosts: network
  gather_facts: no
  serial: 1  # Update one device at a time
  max_fail_percentage: 0

  tasks:
    - name: Backup current configuration
      ios_config:
        backup: yes

    - name: Apply new configuration
      ios_config:
        src: new_config.j2

    - name: Verify device is operational
      ios_command:
        commands:
          - show version
          - show ip interface brief
      register: health_check

    - name: Wait for device stability
      pause:
        seconds: 30

    - name: Verify connectivity to upstream
      ios_command:
        commands: ping {{ upstream_device }}
      register: ping_result
      failed_when: "'Success rate is 0' in ping_result.stdout[0]"
```

## Troubleshooting Common Issues

### Issue: Connection Timeout

```yaml
# Solution: Increase timeout values
- name: Configure with longer timeout
  ios_config:
    lines:
      - ip domain-name example.com
    timeout: 60
```

### Issue: Authentication Failure

```yaml
# Solution: Verify credentials and connection parameters
- name: Test connection
  ios_command:
    commands: show version
  vars:
    ansible_command_timeout: 30
```

### Issue: Configuration Not Saved

```yaml
# Solution: Explicitly save configuration
- name: Ensure config is saved
  ios_config:
    save_when: modified

# Or use command
- name: Save configuration
  ios_command:
    commands: write memory
```

## Testing Network Playbooks

### Using Check Mode

```bash
ansible-playbook network_playbook.yml --check
```

### Diff Mode for Configuration Changes

```bash
ansible-playbook network_playbook.yml --check --diff
```

### Test Playbook

```yaml
---
- name: Test Network Connectivity
  hosts: network
  gather_facts: no

  tasks:
    - name: Verify device reachable
      wait_for:
        host: "{{ ansible_host }}"
        port: 22
        timeout: 10
      delegate_to: localhost

    - name: Verify authentication
      ios_command:
        commands: show version
      register: version_output

    - name: Display test results
      debug:
        msg: "Device {{ inventory_hostname }} is reachable and authenticated"
```

## Resources and Further Reading

- [Ansible Network Automation Documentation](https://docs.ansible.com/ansible/latest/network/index.html)
- [Cisco IOS Collection](https://galaxy.ansible.com/cisco/ios)
- [Network Debug and Troubleshooting Guide](https://docs.ansible.com/ansible/latest/network/user_guide/network_debug_troubleshooting.html)
- [Best Practices for Network Automation](https://docs.ansible.com/ansible/latest/network/user_guide/network_best_practices_2.5.html)

## Next Steps

1. Set up a test lab environment with network devices or simulators
2. Practice basic configuration tasks
3. Implement configuration backups
4. Create compliance checking playbooks
5. Explore advanced features like NETCONF and REST APIs
6. Build a complete network automation workflow
