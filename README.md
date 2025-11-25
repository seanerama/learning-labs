# Learning Labs

A collection of hands-on learning labs for DevOps, automation, and infrastructure technologies.

## 📚 Available Labs

| Lab | Description | Duration | Difficulty |
|-----|-------------|----------|------------|
| [🐳 Docker Basics](docker-basics/) | Container fundamentals, image building, and Docker Compose | 5 hours | Beginner → Intermediate |
| [☸️ Kubernetes](kubernetes/) | Container orchestration, deployments, and cluster management | TBD | Intermediate |
| [🤖 Ansible](ansible/) | Network automation with Ansible for Cisco IOS devices | 4 hours | Beginner → Advanced |
| [🐍 Python Intro](python-intro/) | Python for network automation with Netmiko and Cisco IOS | 3 hours | Beginner |
| [🔌 MCP](mcp/) | Model Context Protocol implementation and usage | TBD | Advanced |
| [🌿 Git](git/) | Version control fundamentals and workflows | Coming Soon | Beginner |

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
1. Start with **Git** - Version control fundamentals
2. Learn **Docker Basics** - Containerization
3. Progress to **Kubernetes** - Container orchestration
4. Explore **Ansible** - Infrastructure automation

### Network Automation Track
1. Start with **Git** - Version control for configs
2. Learn **Python Intro** - Automation basics
3. Move to **Ansible** - Network device automation
4. Use **Docker** for automation tool deployment

### Cloud Native Track
1. **Docker Basics** - Container fundamentals
2. **Kubernetes** - Orchestration at scale
3. **MCP** - Advanced protocol integration

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

### Git (Coming Soon)
**What you'll learn:**
- Git fundamentals and workflow
- Branching and merging strategies
- Collaboration with remote repositories
- Resolving conflicts
- Best practices for commits

**Highlights:**
- Initialize and manage repositories
- Collaborate with teams
- CI/CD integration basics

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

### Kubernetes
**What you'll learn:**
- Kubernetes architecture and concepts
- Deployments, services, and pods
- ConfigMaps and secrets
- Scaling and updates
- Cluster management

**Highlights:**
- Deploy applications to Kubernetes
- Manage microservices
- Production orchestration

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

### MCP
**What you'll learn:**
- Model Context Protocol implementation
- Server and client architecture
- Integration patterns
- Advanced use cases

**Highlights:**
- Build MCP servers
- Integrate with applications
- Protocol deep dive

## 🤝 Contributing

These labs are designed for training and education. Feedback and improvements are welcome!

## 📝 License

These learning materials are provided for educational purposes.

---

**Happy Learning!** 🚀
