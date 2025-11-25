# Learning Labs

A collection of hands-on learning labs for DevOps, automation, and infrastructure technologies.

## 📚 Available Labs

| Lab | Description | Duration | Difficulty |
|-----|-------------|----------|------------|
| [🐳 Docker Basics](docker-basics/) | Container fundamentals, image building, and Docker Compose | 5 hours | Beginner → Intermediate |
| [🤖 Ansible](ansible/) | Network automation with Ansible for Cisco IOS devices | 4 hours | Beginner → Advanced |
| [🐍 Python Intro](python-intro/) | Python for network automation with Netmiko and Cisco IOS | 3 hours | Beginner |

## 🎯 Getting Started

Each lab includes:
- **START-HERE.md** - Overview and learning objectives
- **QUICKSTART.md** - Installation and setup guide
- **README.md** - Complete curriculum and lessons
- **Hands-on examples** - Practical exercises and working code

### Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd learning-labs

# Choose a lab
cd docker-basics/        # or ansible/ or python-intro/

# Start learning
cat START-HERE.md
```

## 📖 Lab Structure

All labs follow a consistent format:

```
lab-name/
├── START-HERE.md           # Entry point
├── QUICKSTART.md          # Setup instructions
├── README.md              # Full curriculum
├── part1-topic/           # Progressive lessons
│   ├── README.md
│   ├── 01-lesson.md
│   └── 02-lesson.md
├── part2-topic/
└── examples/              # Working code examples
```

## 🎓 Learning Paths

### DevOps Track
1. Start with **Docker Basics** - Learn containerization
2. Explore **Ansible** - Automate infrastructure
3. Combine both for container orchestration

### Network Automation Track
1. Start with **Python Intro** - Learn Python basics
2. Move to **Ansible** - Network device automation
3. Use **Docker** for automation tool deployment

## 🔧 Prerequisites

- Basic command-line knowledge
- Terminal/shell access (Linux, macOS, or WSL2 on Windows)
- Internet connection for downloading tools and images
- Text editor

Specific requirements are listed in each lab's QUICKSTART.md

## 💡 Features

- ✅ Progressive difficulty (beginner to advanced)
- ✅ Hands-on practical examples
- ✅ Real-world use cases
- ✅ Troubleshooting guides
- ✅ Best practices included
- ✅ Self-paced learning
- ✅ Working code examples ready to run

## 📊 Lab Overview

### Docker Basics
**What you'll learn:**
- Running and managing containers
- Building custom images with Dockerfiles
- Creating web applications (Streamlit)
- Multi-container orchestration with Docker Compose
- Production deployment patterns

**Highlights:**
- Deploy a speedtest server
- Build a Streamlit web app
- Create Flask + PostgreSQL stack

### Ansible
**What you'll learn:**
- Network device automation
- Ansible playbooks and roles
- Configuration management
- Compliance checking
- Template-based configuration

**Highlights:**
- Cisco IOS automation
- Backup and restore configurations
- VLAN provisioning

### Python Intro
**What you'll learn:**
- Python fundamentals
- Network automation with Netmiko
- Working with CSV and text files
- Error handling and functions
- Concurrent operations

**Highlights:**
- Connect to network devices
- Automate configuration tasks
- Process device inventories

## 🤝 Contributing

These labs are designed for training and education. Feedback and improvements are welcome!

## 📝 License

These learning materials are provided for educational purposes.

---

**Happy Learning!** 🚀
