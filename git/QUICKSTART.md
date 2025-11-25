# Git Quick Start Guide

Get Git installed and configured in 10 minutes!

## 📋 Prerequisites

- Command-line terminal access
- Internet connection
- Administrator/sudo privileges (for installation)

## 🔧 Installation

### Linux

#### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install Git
sudo apt install -y git

# Verify installation
git --version
```

#### RHEL/CentOS/Fedora
```bash
# Install Git
sudo yum install -y git
# OR for newer versions
sudo dnf install -y git

# Verify installation
git --version
```

### macOS

#### Using Homebrew (Recommended)
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Git
brew install git

# Verify installation
git --version
```

#### Using Xcode Command Line Tools
```bash
# This will prompt to install if not present
git --version

# Or install explicitly
xcode-select --install
```

### Windows

#### Option 1: Git for Windows (Recommended)
1. Download from: https://git-scm.com/download/win
2. Run the installer
3. **Recommended settings during install:**
   - Use Git from Git Bash only (or command line if comfortable)
   - Use the OpenSSL library
   - Checkout Windows-style, commit Unix-style line endings
   - Use MinTTY terminal
   - Enable file system caching

4. Open "Git Bash" from Start menu
5. Verify installation:
```bash
git --version
```

#### Option 2: WSL2 (Windows Subsystem for Linux)
If you have WSL2:
```bash
# Inside WSL2 terminal
sudo apt update
sudo apt install -y git
git --version
```

## ⚙️ Initial Configuration

After installing Git, configure your identity:

```bash
# Set your name (appears in commits)
git config --global user.name "Your Name"

# Set your email (appears in commits)
git config --global user.email "your.email@example.com"

# Set default branch name to 'main'
git config --global init.defaultBranch main

# Set default editor (optional)
git config --global core.editor "nano"  # or vim, code, etc.

# Enable colored output
git config --global color.ui auto
```

### Verify Configuration

```bash
# View all configuration
git config --list

# View specific settings
git config user.name
git config user.email
```

## 🔐 SSH Setup (Optional but Recommended)

For GitHub/GitLab access without passwords:

### Generate SSH Key

```bash
# Generate new SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Press Enter to accept default location
# Enter passphrase (or press Enter for no passphrase)

# Start SSH agent
eval "$(ssh-agent -s)"

# Add key to agent
ssh-add ~/.ssh/id_ed25519

# Display public key to copy
cat ~/.ssh/id_ed25519.pub
```

### Add to GitHub/GitLab

1. Copy the output from the `cat` command above
2. Go to GitHub/GitLab Settings → SSH Keys
3. Click "New SSH Key"
4. Paste your key and give it a title
5. Click "Add SSH Key"

### Test Connection

```bash
# Test GitHub
ssh -T git@github.com

# Test GitLab
ssh -T git@gitlab.com

# You should see a success message
```

## ✅ Verification

Ensure everything is working:

```bash
# Check version
git --version
# Should show: git version 2.x.x or higher

# Check configuration
git config --list
# Should show your name and email

# Create a test repository
mkdir git-test
cd git-test
git init
# Should show: Initialized empty Git repository

# Create a test file
echo "Hello Git!" > test.txt

# Add and commit
git add test.txt
git commit -m "Test commit"
# Should show commit success

# View log
git log
# Should show your commit

# Clean up
cd ..
rm -rf git-test

# All working? You're ready!
echo "✓ Git is ready to use!"
```

## 🎯 Quick Start Commands

Once installed, here are the essential commands:

```bash
# Create new repository
git init

# Clone existing repository
git clone <url>

# Check status
git status

# Add files to staging
git add <file>
git add .  # Add all files

# Commit changes
git commit -m "Your message"

# View history
git log
git log --oneline  # Compact view

# View differences
git diff

# Create branch
git branch <name>

# Switch branch
git checkout <branch>
# OR (newer syntax)
git switch <branch>

# Push to remote
git push

# Pull from remote
git pull
```

## 📚 Learning Resources

Now that Git is installed:

1. **Start the lab:** `cat START-HERE.md`
2. **Begin Part 1:** `cd part1-basics/`
3. **Interactive tutorial:** Try `git help tutorial`

## 🆘 Troubleshooting

### Issue: "git: command not found"

**Solution:**
- **Linux:** Git not installed correctly. Re-run installation
- **Mac:** Run `xcode-select --install`
- **Windows:** Make sure Git is in your PATH, or use Git Bash

### Issue: "Permission denied" when installing

**Solution:**
```bash
# Use sudo on Linux/Mac
sudo apt install git

# Or run terminal as Administrator on Windows
```

### Issue: SSH connection fails

**Solution:**
```bash
# Check if key exists
ls -la ~/.ssh/

# Regenerate if needed
ssh-keygen -t ed25519 -C "your.email@example.com"

# Ensure agent is running
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Check GitHub/GitLab has your public key
```

### Issue: "Author identity unknown"

**Solution:**
```bash
# Configure user info
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

## 💡 Best Practices

### DO:
- ✅ Use meaningful commit messages
- ✅ Commit often (small, logical changes)
- ✅ Pull before you push
- ✅ Use branches for features
- ✅ Keep commits focused

### DON'T:
- ❌ Commit passwords or sensitive data
- ❌ Use vague commit messages ("fix", "update")
- ❌ Commit large binary files
- ❌ Force push to shared branches
- ❌ Commit directly to main/master

## 🎓 What's Next?

Git is installed and configured! Now:

1. **Read the overview:** `cat README.md`
2. **Start learning:** `cd part1-basics/`
3. **Follow the lessons** in order

## 📖 Additional Tools (Optional)

### GUI Clients
- **GitHub Desktop:** https://desktop.github.com/
- **GitKraken:** https://www.gitkraken.com/
- **SourceTree:** https://www.sourcetreeapp.com/

### IDE Integration
- **VS Code:** Built-in Git support
- **PyCharm:** Built-in Git support
- **Vim:** vim-fugitive plugin

### Command-Line Enhancements
```bash
# Install git-extras (helpful additional commands)
# Ubuntu/Debian
sudo apt install git-extras

# macOS
brew install git-extras

# Install diff-so-fancy (better diffs)
npm install -g diff-so-fancy
git config --global core.pager "diff-so-fancy | less"
```

---

**Installation complete?** Head to [README.md](README.md) to see the full curriculum!

**Having issues?** Each lesson includes troubleshooting sections.

**Ready to learn?** Start with [Part 1: Single Developer Basics](part1-basics/README.md)
