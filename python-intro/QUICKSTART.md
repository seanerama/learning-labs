# Quick Start Guide - Python Network Automation

Get up and running with Python network automation in 15 minutes!

> **Note:** This lab focuses on **Cisco IOS/IOS-XE devices**. Future labs for Juniper Junos, Aruba, and Arista are planned.

## Prerequisites

Before you begin, ensure you have:

- ✅ Python 3.8 or higher
- ✅ pip (Python package manager)
- ✅ Git (for version control)
- ✅ Access to a Cisco IOS device (physical, GNS3, EVE-NG, or DevNet Sandbox)
- ✅ SSH credentials for the device

### Check Your Python Version

```bash
python3 --version
# Should show Python 3.8 or higher
```

If Python is not installed, download it from [python.org](https://www.python.org/downloads/)

## Installation Steps

### 1. Clone and Navigate to the Lab Directory

```bash
# Clone the repository
git clone <repository-url>
cd learning-labs/python-intro
```

### 2. Run the Setup Script (Easiest Method)

```bash
./setup.sh
```

This script will:
- Check Python version
- Create a virtual environment
- Install all dependencies
- Set up your .env file

### 3. Manual Setup (Alternative)

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Device Credentials

```bash
# Copy the example file
cp .env-example .env

# Edit with your credentials
nano .env
```

Update the `.env` file:
```
USERNAME=your_cisco_username
PASSWORD=your_cisco_password
```

**Security Note:** The `.env` file is in `.gitignore` and won't be committed to version control.

## Running Your First Script

### Part 1: Basic Connection

Update the IP address in the script:

```bash
# Edit the script
nano scripts/01_netmiko_basics.py

# Change this line to your device IP:
# host="192.168.1.1"  # Replace with your router's IP
```

Run the script:

```bash
python scripts/01_netmiko_basics.py
```

**Expected Output:**
```
*14:23:45.123 UTC Mon Nov 24 2025
```

✅ **Success!** You've just automated your first network command!

## Quick Test Script

Create a quick test to verify everything works:

```bash
python3 << 'EOF'
import sys
print(f"✓ Python version: {sys.version}")

try:
    import netmiko
    print("✓ Netmiko installed")
except:
    print("✗ Netmiko not found")

try:
    from dotenv import load_dotenv
    print("✓ python-dotenv installed")
except:
    print("✗ python-dotenv not found")

print("\nReady to start! Run: python scripts/01_netmiko_basics.py")
EOF
```

## Learning Progression

Follow these scripts in order:

### Beginner (Parts 1-3)
```bash
python scripts/01_netmiko_basics.py      # Your first connection
python scripts/02_env_variables.py       # Secure credentials
python scripts/03_for_loops.py           # Multiple commands
```

### Intermediate (Parts 4-6)
```bash
python scripts/04_nested_loops.py        # Multiple devices
python scripts/05_read_write_files.py    # File operations
python scripts/06_csv_operations.py      # CSV input/output
```

### Advanced (Parts 7-9)
```bash
python scripts/07_error_handling.py      # Error handling
python scripts/08_functions.py           # Modular code
python scripts/09_concurrent.py          # Concurrent execution
```

## Troubleshooting

### Issue: "command not found: ./setup.sh"

**Solution:**
```bash
chmod +x setup.sh
./setup.sh
```

### Issue: "Module not found: netmiko"

**Solution:**
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Issue: "Connection timeout" or "Authentication failed"

**Solution:**
1. Verify device is reachable:
   ```bash
   ping 192.168.1.1
   ```

2. Test SSH manually:
   ```bash
   ssh admin@192.168.1.1
   ```

3. Check credentials in `.env` file
4. Verify SSH is enabled on device:
   ```
   conf t
   ip ssh version 2
   line vty 0 4
   transport input ssh
   ```

### Issue: "No such file or directory: .env"

**Solution:**
```bash
cp .env-example .env
nano .env  # Add your credentials
```

### Issue: Virtual environment not activating

**Solution:**
```bash
# Linux/macOS
source venv/bin/activate

# Windows Command Prompt
venv\Scripts\activate.bat

# Windows PowerShell
venv\Scripts\Activate.ps1
```

### Issue: Scripts show "Permission denied"

**Solution:**
```bash
chmod +x scripts/*.py
```

## Using Cisco DevNet Sandbox

Don't have a lab device? Use Cisco's free sandbox:

1. Visit [Cisco DevNet Sandbox](https://developer.cisco.com/site/sandbox/)
2. Reserve an "IOS XE on CSR" sandbox (free)
3. Use the provided credentials in your `.env` file
4. Update script IP addresses to the sandbox device

**Example DevNet Sandbox Credentials:**
```
host="sandbox-iosxe-latest-1.cisco.com"
port=22
```

## Testing Each Part

### Part 1 Test
```bash
python scripts/01_netmiko_basics.py
# Should show device clock
```

### Part 2 Test
```bash
python scripts/02_env_variables.py
# Should connect using .env credentials
```

### Part 3 Test
```bash
python scripts/03_for_loops.py
# Should show multiple command outputs
```

### Part 5 Test
```bash
# Create ips.txt first
echo "192.168.1.1" > examples/ips.txt
python scripts/05_read_write_files.py
# Check outputs/ for CSV file
```

## Directory Structure After Setup

```
python-intro/
├── venv/                  # Virtual environment (created by setup)
├── scripts/               # Python scripts
├── examples/              # Sample data files
├── outputs/               # Script outputs (created automatically)
├── .env                   # Your credentials (not in git)
├── requirements.txt       # Dependencies
└── *.md                   # Documentation
```

## Next Steps

Once you've successfully run Part 1:

1. ✅ Complete all 9 parts in order
2. 📖 Read script comments to understand each line
3. 🔧 Modify scripts for your network
4. 🚀 Build your own automation tools
5. 📚 Read [README.md](README.md) for deeper understanding

## Quick Command Reference

```bash
# Activate virtual environment
source venv/bin/activate

# Run a script
python scripts/01_netmiko_basics.py

# Check installed packages
pip list

# Update dependencies
pip install -r requirements.txt --upgrade

# Deactivate virtual environment
deactivate
```

## Platform-Specific Notes

### Cisco IOS/IOS-XE (This Lab)
- Device type: `cisco_ios`
- SSH must be enabled
- Privilege 15 or enable password required for config commands

### Future Labs (Coming Soon)
- **Juniper Junos** - Similar structure, Junos-specific modules
- **Aruba AOS-CX** - REST API and CLI automation
- **Arista EOS** - eAPI and Netmiko support

## Getting Help

### Documentation
- [START-HERE.md](START-HERE.md) - Overview and navigation
- [README.md](README.md) - Complete learning path
- Script comments - Detailed explanations

### Resources
- [Netmiko GitHub](https://github.com/ktbyers/netmiko)
- [Python Dotenv](https://github.com/theskumar/python-dotenv)
- [Cisco DevNet](https://developer.cisco.com/)

### Common Commands
```bash
# Check if device is reachable
ping <device-ip>

# Test SSH access
ssh <username>@<device-ip>

# View Python path
which python

# Check pip packages
pip list | grep netmiko
```

## Success Checklist

Before moving forward, ensure:

- ✅ Virtual environment is created and activated
- ✅ All dependencies are installed
- ✅ .env file is configured with credentials
- ✅ Part 1 script runs successfully
- ✅ Device is reachable via SSH
- ✅ You understand the output

## Time Estimate

- **Setup:** 10-15 minutes
- **Part 1:** 15 minutes
- **Parts 2-9:** 3-5 hours total
- **Building your own tools:** Ongoing!

---

**You're now ready to start your Python network automation journey!**

Run Part 1 and let's begin:
```bash
python scripts/01_netmiko_basics.py
```

**Happy Automating! 🚀**
