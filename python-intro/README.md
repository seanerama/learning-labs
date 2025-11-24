# Python Network Automation Lab - Cisco IOS Focus

A hands-on, progressive learning journey teaching Python programming through network automation with **Cisco IOS/IOS-XE devices**.

> **Platform Focus:** This lab is specifically designed for Cisco IOS/IOS-XE environments. Similar labs for Juniper Junos, Aruba AOS-CX, and Arista EOS are planned for future release.

## 🎯 Lab Overview

This repository provides a step-by-step guide for network engineers to learn Python by building scripts that interact with Cisco network devices. Each part introduces new programming concepts and tools, gradually building toward a powerful and efficient network automation toolkit.

### What You'll Build

By the end of this lab, you'll have created a production-ready Python script that can:
- ✅ Connect to multiple Cisco IOS devices simultaneously
- ✅ Execute commands across your network
- ✅ Handle errors gracefully
- ✅ Parse and store outputs in CSV format
- ✅ Run efficiently using concurrent connections
- ✅ Follow security best practices

### Who This Lab Is For

- **Network Engineers** wanting to learn Python
- **DevOps professionals** working with Cisco infrastructure
- **Students** learning network automation
- **Anyone** wanting practical Python skills

**No prior Python experience required!** We teach everything from scratch.

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Access to Cisco IOS/IOS-XE device(s) - can be:
  - Physical devices
  - GNS3 or EVE-NG virtual devices
  - Cisco DevNet Sandbox (free)

### Get Started in 3 Steps

```bash
# 1. Clone the repository
git clone <repository-url>
cd learning-labs/python-intro

# 2. Run setup
./setup.sh

# 3. Start learning
cat START-HERE.md
```

📖 **New to this lab?** Read [START-HERE.md](START-HERE.md) first!

⚡ **Want to jump right in?** Follow [QUICKSTART.md](QUICKSTART.md)

## 📚 Learning Path

This lab consists of 9 progressive parts, each building on the previous one:

### Part 1: Introduction to Netmiko
**Concepts:** Importing libraries, SSH connections
- Connect to a Cisco router
- Send your first command (`show clock`)
- Understand basic Python syntax

**What you'll learn:**
- How to import Python libraries
- What Netmiko is and why it's useful
- Basic device connection patterns

```bash
python scripts/01_netmiko_basics.py
```

---

### Part 2: Using `dotenv` and `os` Libraries
**Concepts:** Environment variables, secure credential management
- Remove hardcoded passwords
- Use `.env` files for credentials
- Follow security best practices

**What you'll learn:**
- Why hardcoding credentials is dangerous
- How to use environment variables
- The `python-dotenv` library

```bash
python scripts/02_env_variables.py
```

---

### Part 3: Sending Multiple Commands with a For Loop
**Concepts:** Loops, iteration, lists
- Send multiple commands to a single device
- Use Python lists
- Automate repetitive tasks

**What you'll learn:**
- What a `for` loop is
- How to iterate over lists
- Basic automation patterns

```bash
python scripts/03_for_loops.py
```

---

### Part 4: Nested For Loops for Multiple Devices
**Concepts:** Nested loops, multi-device automation
- Connect to multiple devices
- Execute multiple commands per device
- Structure complex automation

**What you'll learn:**
- Nested loop patterns
- Multi-device orchestration
- Scaling your scripts

```bash
python scripts/04_nested_loops.py
```

---

### Part 5: Reading from Text and Writing to CSV
**Concepts:** File I/O, CSV operations
- Read device IPs from a text file
- Save command outputs to CSV
- Work with structured data

**What you'll learn:**
- File reading and writing
- The `csv` module
- Data persistence patterns

```bash
python scripts/05_read_write_files.py
```

---

### Part 6: Input and Output via CSV Files
**Concepts:** Advanced CSV operations, data structures
- Use CSV for both input and output
- Manage complex device/command combinations
- Structure data efficiently

**What you'll learn:**
- CSV dictionaries
- Structured input/output
- Data organization best practices

```bash
python scripts/06_csv_operations.py
```

---

### Part 7: Error Handling with Try-Except-Finally
**Concepts:** Exception handling, robustness
- Handle connection failures gracefully
- Log errors without stopping execution
- Make production-ready scripts

**What you'll learn:**
- `try`, `except`, `finally` blocks
- Exception handling patterns
- Production-ready error handling

```bash
python scripts/07_error_handling.py
```

---

### Part 8: Refactoring with Functions
**Concepts:** Functions, modular code, code organization
- Break code into reusable functions
- Improve readability and maintainability
- Follow DRY principles (Don't Repeat Yourself)

**What you'll learn:**
- Defining and calling functions
- Code organization patterns
- Modular programming

```bash
python scripts/08_functions.py
```

---

### Part 9: Efficiency with `concurrent.futures`
**Concepts:** Concurrency, threading, performance
- Connect to multiple devices simultaneously
- Dramatically improve script performance
- Use modern Python patterns

**What you'll learn:**
- `concurrent.futures` module
- Threading vs multiprocessing
- Performance optimization

```bash
python scripts/09_concurrent.py
```

---

## 🎓 What You'll Learn

### Python Fundamentals
- Variables and data types
- Lists and dictionaries
- For loops and nested loops
- Functions and parameters
- File I/O operations
- Error handling
- Modules and imports
- Concurrency basics

### Network Automation Skills
- SSH connections with Netmiko
- Cisco IOS command execution
- Output parsing and storage
- Multi-device orchestration
- Error handling for network operations
- Performance optimization
- Security best practices
- Production-ready patterns

### Best Practices
- Secure credential management
- Code organization and modularity
- Error handling and logging
- Documentation and comments
- Version control integration
- Testing strategies

## 📁 Repository Structure

```
python-intro/
├── scripts/                        # Python learning scripts
│   ├── 01_netmiko_basics.py       # Basic Netmiko connection
│   ├── 02_env_variables.py        # Environment variables
│   ├── 03_for_loops.py            # For loops
│   ├── 04_nested_loops.py         # Nested loops
│   ├── 05_read_write_files.py     # File I/O and CSV
│   ├── 06_csv_operations.py       # CSV input/output
│   ├── 07_error_handling.py       # Error handling
│   ├── 08_functions.py            # Functions and modularity
│   ├── 09_concurrent.py           # Concurrency
│   └── csv-example.py             # CSV operations example
├── examples/                       # Sample data files
│   ├── input_3_devices.csv        # Sample input (3 devices)
│   ├── input_150_devices.csv      # Sample input (150 devices)
│   └── ips.txt                    # Sample IP list
├── outputs/                        # Script output directory
│   └── .gitkeep                   # Keeps directory in git
├── requirements.txt                # Python dependencies
├── .env-example                    # Credentials template
├── .gitignore                     # Git ignore patterns
├── setup.sh                       # Automated setup script
├── START-HERE.md                  # Entry point (read this first!)
├── QUICKSTART.md                  # Fast setup guide
└── README.md                      # This file
```

## 🛠️ Technology Stack

### Core Libraries
- **Netmiko** - SSH connection management for network devices
- **Paramiko** - SSH protocol implementation
- **python-dotenv** - Environment variable management
- **CSV** - Data parsing and storage
- **concurrent.futures** - Concurrent execution

### Supported Platforms
- ✅ **Cisco IOS** (all versions)
- ✅ **Cisco IOS-XE** (CSR1000v, Catalyst 9000, etc.)

### Future Platform Support (Planned)
- 🔄 **Juniper Junos** - Similar progressive lab
- 🔄 **Aruba AOS-CX** - CLI and REST API automation
- 🔄 **Arista EOS** - eAPI and Netmiko support

Each vendor will have its own dedicated lab following this same progressive structure.

## ⚙️ Setup Instructions

### Quick Setup (Recommended)

```bash
# Clone and navigate
git clone <repository-url>
cd learning-labs/python-intro

# Run automated setup
./setup.sh

# Configure credentials
cp .env-example .env
nano .env  # Add your device credentials
```

### Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env-example .env
nano .env
```

### Environment Configuration

Create a `.env` file with your Cisco device credentials:

```env
USERNAME=your_cisco_username
PASSWORD=your_cisco_password
```

**Security Note:** The `.env` file is in `.gitignore` and will not be committed to version control.

## 🎯 Learning Progression

### Beginner Track (Parts 1-3)
Start here if you're new to Python:
1. Basic connection and commands
2. Secure credential management
3. Loops and automation

**Time:** 1-2 hours

### Intermediate Track (Parts 4-6)
Expand your skills:
4. Multi-device automation
5. File operations
6. Structured data handling

**Time:** 2-3 hours

### Advanced Track (Parts 7-9)
Production-ready skills:
7. Error handling
8. Code organization
9. Performance optimization

**Time:** 2-3 hours

**Total Lab Time:** 4-6 hours (self-paced)

## 💡 Usage Examples

### Running a Script

```bash
# Activate virtual environment
source venv/bin/activate

# Run a script
python scripts/01_netmiko_basics.py
```

### Customizing for Your Network

1. Update device IPs in the script or input files
2. Modify commands to suit your needs
3. Adjust error handling as needed

### Building Your Own Tools

After completing all parts, you'll have the skills to:
- Create custom automation scripts
- Build network auditing tools
- Automate configuration tasks
- Generate network reports
- Integrate with other systems

## 🔒 Security Best Practices

This lab teaches secure automation practices:

✅ **Never hardcode credentials** - Use environment variables
✅ **Use `.gitignore`** - Keep credentials out of version control
✅ **Limit permissions** - Use appropriate user privileges
✅ **Validate inputs** - Sanitize user-provided data
✅ **Log appropriately** - Don't log sensitive information
✅ **Use SSH keys** - When possible, prefer key-based auth

## 🧪 Testing Environment Options

### Option 1: Cisco DevNet Sandbox (Free)
- Visit [developer.cisco.com/sandbox](https://developer.cisco.com/site/sandbox/)
- Reserve an "IOS XE on CSR" sandbox
- Use provided credentials in your `.env` file
- No hardware required!

### Option 2: Local Lab
- GNS3 with Cisco IOS images
- EVE-NG virtual lab
- Physical Cisco devices

### Option 3: Cloud Lab
- AWS with Cisco CSR1000v
- Azure with Cisco virtual appliances
- Google Cloud with network virtual appliances

## 📖 Additional Resources

### Official Documentation
- [Netmiko Documentation](https://github.com/ktbyers/netmiko)
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Cisco DevNet](https://developer.cisco.com/)

### Recommended Reading
- "Network Programmability and Automation" (O'Reilly)
- "Automate the Boring Stuff with Python"
- Cisco DevNet Learning Labs

### Community
- [Network to Code Slack](https://networktocode.slack.com)
- [Cisco DevNet Community](https://community.cisco.com/t5/devnet/ct-p/devnet)
- Python Discord servers

## 🤝 Contributing

This lab is part of a larger learning-labs repository. Contributions welcome!

### Future Enhancements
- Additional vendor labs (Junos, Aruba, Arista)
- Advanced topics (YANG, NETCONF, gRPC)
- CI/CD integration examples
- Ansible comparison examples

## 📝 License

[License details to be added]

## 🙏 Acknowledgments

Built for network engineers by network engineers. Special thanks to:
- Kirk Byers (Netmiko creator)
- The Network to Code community
- Cisco DevNet

## ❓ Troubleshooting

### Common Issues

**Virtual environment not activating:**
```bash
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

**Module not found errors:**
```bash
pip install -r requirements.txt
```

**Connection timeouts:**
- Verify device is reachable: `ping <device-ip>`
- Check SSH is enabled on device
- Verify credentials in `.env` file

**Authentication failures:**
- Check username/password in `.env`
- Verify enable password if required
- Check device AAA configuration

For more troubleshooting help, see [QUICKSTART.md](QUICKSTART.md)

## 🎉 Ready to Start?

**Begin your journey:**
1. Read [START-HERE.md](START-HERE.md) for overview
2. Follow [QUICKSTART.md](QUICKSTART.md) for setup
3. Execute Part 1 and start learning!

```bash
./setup.sh
python scripts/01_netmiko_basics.py
```

---

**Platform:** Cisco IOS/IOS-XE
**Level:** Beginner to Intermediate
**Time:** 4-6 hours
**Prerequisites:** None!

**Future Labs:** Juniper Junos, Aruba AOS-CX, Arista EOS

**Happy Automating! 🚀**
