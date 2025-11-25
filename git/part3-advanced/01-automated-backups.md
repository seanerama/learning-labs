# Lesson 1: Automated Configuration Backups

Build a Python-based automation system that backs up network device configurations and commits changes to Git automatically.

## 🎯 Objectives

By the end of this lesson, you'll be able to:
- Create a Python script that backs up device configurations
- Automatically commit changes to Git
- Detect and report configuration changes
- Schedule automated backups
- Send email notifications on changes
- Handle errors gracefully

## 📝 What You'll Learn

- Python + Git integration using subprocess
- Connecting to network devices (simulated)
- Automatic change detection
- Scheduling with cron
- Error handling and logging
- Email notifications

## 🐍 Part 1: Basic Python-Git Integration

### Understanding the Workflow

```
Script runs → Connect to devices → Retrieve configs → Save to files
    ↓
Check for changes (git status)
    ↓
If changes: commit + push
    ↓
Send notification (optional)
```

### Simple Example: Manual Backup

Let's start with a basic script:

```bash
cd ~/network-configs
```

Create `backup_simple.py`:

```python
#!/usr/bin/env python3
"""
Simple configuration backup script
Demonstrates basic Git integration
"""

import subprocess
import sys
from datetime import datetime

def run_git_command(command):
    """Run a git command and return the result"""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(command)}")
        print(f"Error: {e.stderr}")
        return None

def check_for_changes():
    """Check if there are any changes to commit"""
    result = run_git_command(['git', 'status', '--porcelain'])
    return bool(result)  # Returns True if there are changes

def commit_changes(message):
    """Add all changes and commit"""
    # Add all files
    run_git_command(['git', 'add', 'configs/'])

    # Commit with message
    run_git_command(['git', 'commit', '-m', message])

    # Push to remote
    run_git_command(['git', 'push'])

    print(f"✓ Changes committed: {message}")

def main():
    """Main backup function"""
    print("=" * 60)
    print("Network Configuration Backup")
    print("=" * 60)

    # In real scenario, you'd retrieve configs from devices here
    # For this example, we'll simulate by having you manually update configs

    # Check if there are any changes
    if check_for_changes():
        # Create timestamped commit message
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"Automated backup: {timestamp}"

        print(f"✓ Configuration changes detected")
        commit_changes(message)
    else:
        print("○ No configuration changes detected")

    print("=" * 60)

if __name__ == '__main__':
    main()
```

Make it executable and test:

```bash
chmod +x backup_simple.py

# Create a test change
mkdir -p configs
echo "test config change" >> configs/test-device.cfg

# Run the script
./backup_simple.py
```

**Output:**
```
============================================================
Network Configuration Backup
============================================================
✓ Configuration changes detected
✓ Changes committed: Automated backup: 2024-01-15 14:30:00
============================================================
```

## 📡 Part 2: Device Connection (Simulated)

For this lab, we'll simulate device backups using sample configurations. In production, you'd use libraries like Netmiko, NAPALM, or Paramiko.

### Production-Style Backup Script

Create `backup_configs.py`:

```python
#!/usr/bin/env python3
"""
Automated network device configuration backup to Git

Features:
- Backs up multiple devices
- Automatic Git commits on changes
- Error handling per device
- Summary reporting
"""

import os
import subprocess
from datetime import datetime
from pathlib import Path

# Configuration
DEVICES = [
    {
        'hostname': 'SW-CORE-01',
        'ip': '192.168.1.10',
        'type': 'cisco_ios',
        'config_file': 'SW-CORE-01.cfg'
    },
    {
        'hostname': 'SW-ACCESS-01',
        'ip': '192.168.1.11',
        'type': 'cisco_ios',
        'config_file': 'SW-ACCESS-01.cfg'
    },
    {
        'hostname': 'SW-ACCESS-02',
        'ip': '192.168.1.12',
        'type': 'cisco_ios',
        'config_file': 'SW-ACCESS-02.cfg'
    }
]

CONFIG_DIR = 'configs'

class BackupError(Exception):
    """Custom exception for backup errors"""
    pass

def ensure_config_directory():
    """Create configs directory if it doesn't exist"""
    Path(CONFIG_DIR).mkdir(exist_ok=True)
    print(f"✓ Configuration directory ready: {CONFIG_DIR}/")

def backup_device_config(device):
    """
    Retrieve configuration from device and save to file

    In production, this would use Netmiko or similar:

    from netmiko import ConnectHandler
    connection = ConnectHandler(**device_params)
    config = connection.send_command('show running-config')
    connection.disconnect()

    For this lab, we'll simulate by reading from sample configs
    or prompting user to update files manually.
    """
    hostname = device['hostname']
    config_file = os.path.join(CONFIG_DIR, device['config_file'])

    try:
        # SIMULATION: In real scenario, connect and retrieve config
        # For now, we'll just check if file exists and report

        if os.path.exists(config_file):
            # File exists - in production, would overwrite with fresh backup
            print(f"  ✓ {hostname}: Configuration backed up")
            return True
        else:
            # Create sample config for first run
            sample_config = f"""hostname {hostname}
!
vlan 10
 name DATA
vlan 20
 name VOICE
vlan 99
 name MANAGEMENT
!
interface GigabitEthernet0/1
 description UPLINK
 switchport mode trunk
!
line vty 0 4
 transport input ssh
!
end
"""
            with open(config_file, 'w') as f:
                f.write(sample_config)
            print(f"  ✓ {hostname}: Initial configuration created")
            return True

    except Exception as e:
        print(f"  ✗ {hostname}: Backup failed - {e}")
        return False

def run_git_command(command, capture_output=True):
    """Execute a git command"""
    try:
        if capture_output:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        else:
            subprocess.run(command, check=True)
            return None
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if hasattr(e, 'stderr') else str(e)
        raise BackupError(f"Git command failed: {error_msg}")

def check_git_changes():
    """Check if there are uncommitted changes"""
    result = run_git_command(['git', 'status', '--porcelain'])
    return bool(result)

def get_changed_files():
    """Get list of changed files"""
    result = run_git_command(['git', 'status', '--porcelain'])
    if not result:
        return []

    # Parse git status output
    changed = []
    for line in result.split('\n'):
        if line:
            # Format: "XY filename"
            filename = line[3:].strip()
            changed.append(filename)

    return changed

def commit_and_push_changes():
    """Commit changes and push to remote"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        # Stage all changes in configs directory
        run_git_command(['git', 'add', f'{CONFIG_DIR}/'])

        # Get list of changed files for commit message
        changed_files = get_changed_files()

        # Create detailed commit message
        if len(changed_files) == 1:
            commit_msg = f"Automated backup: {changed_files[0]} updated - {timestamp}"
        else:
            commit_msg = f"Automated backup: {len(changed_files)} configs updated - {timestamp}"

        # Commit
        run_git_command(['git', 'commit', '-m', commit_msg])

        # Push to remote
        run_git_command(['git', 'push'])

        print(f"\n✓ Changes committed and pushed to remote")
        print(f"  Commit: {commit_msg}")

        return True

    except BackupError as e:
        print(f"\n✗ Failed to commit changes: {e}")
        return False

def generate_backup_report(successful, failed, changes_detected):
    """Generate summary report"""
    print("\n" + "=" * 60)
    print("BACKUP SUMMARY")
    print("=" * 60)
    print(f"Successful backups: {successful}")
    print(f"Failed backups: {failed}")
    print(f"Configuration changes: {'Yes' if changes_detected else 'No'}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

def main():
    """Main backup workflow"""
    print("=" * 60)
    print("AUTOMATED NETWORK CONFIGURATION BACKUP")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Devices to backup: {len(DEVICES)}")
    print()

    # Ensure config directory exists
    ensure_config_directory()

    # Backup each device
    print(f"\nBacking up devices:")
    successful = 0
    failed = 0

    for device in DEVICES:
        if backup_device_config(device):
            successful += 1
        else:
            failed += 1

    # Check for changes
    print(f"\nChecking for configuration changes...")

    if check_git_changes():
        print(f"✓ Configuration changes detected")

        # Show what changed
        changed_files = get_changed_files()
        print(f"\nChanged files:")
        for file in changed_files:
            print(f"  - {file}")

        # Commit and push
        commit_and_push_changes()
    else:
        print(f"○ No configuration changes detected")

    # Generate report
    generate_backup_report(successful, failed, check_git_changes())

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Backup interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n✗ Backup failed with error: {e}")
        exit(1)
```

### Test the Script

```bash
chmod +x backup_configs.py

# Run it
./backup_configs.py
```

**Expected Output:**
```
============================================================
AUTOMATED NETWORK CONFIGURATION BACKUP
============================================================
Started: 2024-01-15 14:45:00
Devices to backup: 3

✓ Configuration directory ready: configs/
  ✓ SW-CORE-01: Initial configuration created
  ✓ SW-ACCESS-01: Initial configuration created
  ✓ SW-ACCESS-02: Initial configuration created

Checking for configuration changes...
✓ Configuration changes detected

Changed files:
  - configs/SW-CORE-01.cfg
  - configs/SW-ACCESS-01.cfg
  - configs/SW-ACCESS-02.cfg

✓ Changes committed and pushed to remote
  Commit: Automated backup: 3 configs updated - 2024-01-15 14:45:00

============================================================
BACKUP SUMMARY
============================================================
Successful backups: 3
Failed backups: 0
Configuration changes: Yes
Timestamp: 2024-01-15 14:45:00
============================================================
```

### Test Change Detection

```bash
# Modify a config
echo "! Added comment" >> configs/SW-CORE-01.cfg

# Run backup again
./backup_configs.py
```

**Output:**
```
...
✓ Configuration changes detected

Changed files:
  - configs/SW-CORE-01.cfg

✓ Changes committed and pushed to remote
  Commit: Automated backup: configs/SW-CORE-01.cfg updated - 2024-01-15 14:47:00
...
```

## 🔔 Part 3: Adding Email Notifications

Create `backup_with_notifications.py`:

```python
#!/usr/bin/env python3
"""
Backup script with email notifications
"""

import os
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path

# Email configuration
EMAIL_ENABLED = os.getenv('EMAIL_ENABLED', 'false').lower() == 'true'
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER = os.getenv('SMTP_USER', 'your-email@example.com')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', 'your-app-password')
EMAIL_TO = os.getenv('EMAIL_TO', 'network-team@example.com')

def send_email_notification(subject, body):
    """Send email notification"""
    if not EMAIL_ENABLED:
        print("  ℹ Email notifications disabled (set EMAIL_ENABLED=true to enable)")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = EMAIL_TO
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"  ✓ Email notification sent to {EMAIL_TO}")

    except Exception as e:
        print(f"  ✗ Failed to send email: {e}")

def get_diff_summary():
    """Get summary of what changed"""
    try:
        result = subprocess.run(
            ['git', 'diff', 'HEAD~1', 'HEAD', '--stat'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except:
        return "Unable to generate diff"

def notify_on_changes(changed_files):
    """Send notification about configuration changes"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    subject = f"Network Config Changes Detected - {timestamp}"

    body = f"""Configuration changes detected and backed up to Git.

Time: {timestamp}
Number of changed files: {len(changed_files)}

Changed configurations:
"""

    for file in changed_files:
        body += f"  - {file}\n"

    body += f"\n\nDiff Summary:\n{get_diff_summary()}"

    body += f"""

View changes: [Your GitHub/GitLab URL]

This is an automated notification from the network backup system.
"""

    send_email_notification(subject, body)

# Add this to your main backup script after committing changes:
# if changes_detected:
#     notify_on_changes(changed_files)
```

### Email Configuration

**For testing without real email:**

```bash
# Disable email
export EMAIL_ENABLED=false
```

**For Gmail (with App Password):**

```bash
export EMAIL_ENABLED=true
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=your-email@gmail.com
export SMTP_PASSWORD=your-app-password
export EMAIL_TO=network-team@example.com
```

**For company SMTP server:**

```bash
export EMAIL_ENABLED=true
export SMTP_SERVER=mail.company.com
export SMTP_PORT=25
export SMTP_USER=backup-system
export SMTP_PASSWORD=secret
export EMAIL_TO=network-ops@company.com
```

## ⏰ Part 4: Scheduling Automated Backups

### Using Cron (Linux/macOS)

```bash
# Edit crontab
crontab -e
```

**Add backup schedules:**

```bash
# Run every day at 2 AM
0 2 * * * cd /home/yourusername/network-configs && /usr/bin/python3 backup_configs.py >> /var/log/network-backup.log 2>&1

# Run every 4 hours
0 */4 * * * cd /home/yourusername/network-configs && /usr/bin/python3 backup_configs.py >> /var/log/network-backup.log 2>&1

# Run every hour during business hours (8 AM - 6 PM, Mon-Fri)
0 8-18 * * 1-5 cd /home/yourusername/network-configs && /usr/bin/python3 backup_configs.py >> /var/log/network-backup.log 2>&1

# Run Monday morning (weekly)
0 6 * * 1 cd /home/yourusername/network-configs && /usr/bin/python3 backup_configs.py >> /var/log/network-backup.log 2>&1
```

**Cron syntax:**
```
* * * * * command
│ │ │ │ │
│ │ │ │ └─ Day of week (0-7, 0 and 7 = Sunday)
│ │ │ └─── Month (1-12)
│ │ └───── Day of month (1-31)
│ └─────── Hour (0-23)
└───────── Minute (0-59)
```

**View scheduled jobs:**
```bash
crontab -l
```

**View cron logs:**
```bash
tail -f /var/log/network-backup.log
```

### Using systemd Timer (Linux)

Create `/etc/systemd/system/network-backup.service`:

```ini
[Unit]
Description=Network Configuration Backup
After=network.target

[Service]
Type=oneshot
User=yourusername
WorkingDirectory=/home/yourusername/network-configs
ExecStart=/usr/bin/python3 /home/yourusername/network-configs/backup_configs.py
StandardOutput=journal
StandardError=journal
```

Create `/etc/systemd/system/network-backup.timer`:

```ini
[Unit]
Description=Run network backup daily at 2 AM
Requires=network-backup.service

[Timer]
OnCalendar=daily
OnCalendar=02:00
Persistent=true

[Install]
WantedBy=timers.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable network-backup.timer
sudo systemctl start network-backup.timer

# Check status
sudo systemctl status network-backup.timer

# View logs
sudo journalctl -u network-backup.service
```

### Using Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. **Name:** "Network Config Backup"
4. **Trigger:** Daily at 2:00 AM
5. **Action:** Start a program
   - Program: `C:\Python39\python.exe`
   - Arguments: `backup_configs.py`
   - Start in: `C:\Users\YourUser\network-configs`
6. Finish

## 🧪 Practice Exercises

### Exercise 1: Test the Backup Script

```bash
cd ~/network-configs

# Create the script
# (Copy backup_configs.py from above)

# Make executable
chmod +x backup_configs.py

# Run initial backup
./backup_configs.py

# Verify files created
ls -la configs/

# Check Git log
git log --oneline
```

### Exercise 2: Simulate Configuration Changes

```bash
# Modify a config
cat >> configs/SW-CORE-01.cfg << 'EOF'
!
vlan 50
 name SERVERS
!
EOF

# Run backup
./backup_configs.py

# Verify commit
git log --oneline -n 1
git show HEAD
```

### Exercise 3: Add More Devices

Edit the `DEVICES` list in `backup_configs.py`:

```python
DEVICES = [
    # ... existing devices ...
    {
        'hostname': 'SW-DIST-01',
        'ip': '192.168.1.20',
        'type': 'cisco_ios',
        'config_file': 'SW-DIST-01.cfg'
    },
    {
        'hostname': 'RTR-WAN-01',
        'ip': '192.168.1.1',
        'type': 'cisco_ios',
        'config_file': 'RTR-WAN-01.cfg'
    }
]
```

Run backup and verify new configs created.

### Exercise 4: Set Up Cron Job

```bash
# Test the script runs from cron environment
# (cron has limited PATH)

# Create wrapper script
cat > /home/yourusername/network-configs/backup-wrapper.sh << 'EOF'
#!/bin/bash
cd /home/yourusername/network-configs
/usr/bin/python3 backup_configs.py
EOF

chmod +x backup-wrapper.sh

# Test it
./backup-wrapper.sh

# Add to crontab (test with every 5 minutes first)
crontab -e
# Add: */5 * * * * /home/yourusername/network-configs/backup-wrapper.sh

# Watch it run
tail -f /var/log/syslog | grep CRON
```

## 📊 Commands Reference

```bash
# Run backup manually
./backup_configs.py

# Run with verbose output
python3 -v backup_configs.py

# Cron management
crontab -e          # Edit cron jobs
crontab -l          # List cron jobs
crontab -r          # Remove all cron jobs

# Check Git log for automated commits
git log --oneline --grep="Automated backup"

# View recent changes
git log -p -1       # Last commit with diff
git diff HEAD~1     # Compare to previous commit

# Systemd timer management
sudo systemctl status network-backup.timer
sudo systemctl start network-backup.timer
sudo systemctl stop network-backup.timer
sudo journalctl -u network-backup.service -f
```

## ✅ Verification Checklist

Make sure you can:

- [ ] Run the backup script manually
- [ ] Script detects configuration changes
- [ ] Script creates Git commits automatically
- [ ] Script pushes to remote repository
- [ ] View backup history in Git log
- [ ] Schedule backups with cron or systemd
- [ ] View backup logs
- [ ] Script handles errors gracefully

## ❓ Common Issues

### Issue: "Permission denied" when running script

**Solution:**
```bash
chmod +x backup_configs.py
```

### Issue: Script can't push to remote

**Cause:** Git credentials not configured for automation

**Solution:**
```bash
# Use SSH keys instead of passwords
ssh-keygen -t ed25519
# Add public key to GitHub/GitLab

# Or use credential helper
git config --global credential.helper store
git push  # Enter credentials once, then cached
```

### Issue: Cron job doesn't run

**Check:**
```bash
# Verify cron service running
sudo systemctl status cron

# Check cron logs
grep CRON /var/log/syslog

# Test script with full paths
/usr/bin/python3 /full/path/to/backup_configs.py
```

### Issue: No changes detected but files changed

**Cause:** Files not in Git tracking

**Solution:**
```bash
# Check git status
git status

# Add configs directory
git add configs/
git commit -m "Add configs directory"
```

## 🎯 Best Practices

### Script Design

✅ **DO:**
- Use absolute paths in cron jobs
- Log all output for debugging
- Handle errors gracefully (don't crash on single device failure)
- Use meaningful commit messages with timestamps
- Test scripts manually before scheduling

❌ **DON'T:**
- Commit sensitive data (passwords, keys)
- Run backups too frequently (respect device CPU)
- Ignore errors silently
- Use interactive commands in automated scripts

### Security

✅ **DO:**
- Use SSH keys for Git authentication
- Store device credentials securely (environment variables, vault)
- Restrict script file permissions (chmod 700)
- Use dedicated service account for backups

❌ **DON'T:**
- Hardcode passwords in scripts
- Commit credential files to Git
- Run as root unless necessary
- Share credential files

### Monitoring

✅ **DO:**
- Send notifications on failures
- Monitor for missing backups
- Review backup logs regularly
- Alert on unexpected changes

## 🎉 Lesson Complete!

You've learned:
✅ Python + Git integration
✅ Automated configuration backups
✅ Change detection and committing
✅ Scheduling with cron/systemd
✅ Email notifications
✅ Error handling and logging

### Next Steps

**Ready for Lesson 2?** → [Interactive Rebase](02-interactive-rebase.md)

Learn how to:
- Clean up commit history
- Squash multiple commits
- Reorder and edit commits
- Maintain professional Git history

**Or practice more:**
- Add real device connections (Netmiko)
- Enhance error handling
- Add more notification methods (Slack, Teams)
- Implement configuration validation

---

**Lesson Duration:** 30 minutes
**Difficulty:** Intermediate → Advanced
**Next:** History management and cleanup
