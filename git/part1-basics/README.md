# Part 1: Single Developer Basics

Master the core Git workflow for managing network configurations on your own.

## 🎯 Learning Objectives

By the end of Part 1, you'll be able to:
- ✅ Create and initialize Git repositories
- ✅ Track changes to network device configurations
- ✅ Write meaningful commit messages
- ✅ Use remote repositories for backup
- ✅ View configuration history
- ✅ Recover from mistakes

## 📚 Lessons

1. **[Repository Setup](01-repository-setup.md)** - Create your first Git repository
2. **[Basic Workflow](02-basic-workflow.md)** - Add, commit, and track changes
3. **[Remote Repositories](03-remote-repositories.md)** - GitHub/GitLab setup and backups
4. **[Viewing History](04-viewing-history.md)** - Explore configuration changes
5. **[Undoing Changes](05-undoing-changes.md)** - Recover and restore

## ⏱️ Time Estimate

**Total:** 1.5 hours
- Repository Setup: 15 minutes
- Basic Workflow: 20 minutes
- Remote Repositories: 30 minutes
- Viewing History: 15 minutes
- Undoing Changes: 10 minutes

## 🎓 What You'll Build

Throughout Part 1, you'll:
1. Create a repository for network configurations
2. Track changes to a Cisco switch configuration
3. Set up remote backup on GitHub or GitLab
4. Practice viewing and comparing configurations
5. Learn to recover from common mistakes

## 🚀 Getting Started

### Prerequisites
- Git installed (see [../QUICKSTART.md](../QUICKSTART.md))
- Text editor
- Basic command-line knowledge

### Verify You're Ready

```bash
# Check Git is installed
git --version

# Check configuration
git config user.name
git config user.email

# If these are empty, configure them:
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 📖 Learning Path

Follow the lessons in order:

```
01-repository-setup.md
    ↓
02-basic-workflow.md
    ↓
03-remote-repositories.md
    ↓
04-viewing-history.md
    ↓
05-undoing-changes.md
```

Each lesson builds on the previous one!

## 💡 Key Concepts Covered

### Repository
A folder tracked by Git containing your project history.

### Commit
A snapshot of your project at a specific point in time.

### Remote
A copy of your repository stored on GitHub/GitLab for backup.

### Working Directory
The actual files you edit (not yet staged).

### Staging Area
Files prepared for the next commit.

### .git Directory
Hidden folder containing all version history.

## 🎯 Practice Scenario

You'll work through this real-world scenario:

**Setup:** You're a network engineer managing configurations for a small branch office with 1 switch.

**Goals:**
- Track all configuration changes
- Maintain history for compliance
- Backup configs to cloud
- Quick rollback capability

**By the end of Part 1:**
- ✅ Repository created
- ✅ Switch config tracked
- ✅ Backed up to GitHub/GitLab
- ✅ History viewable
- ✅ Can recover from mistakes

## ✅ Completion Checklist

Mark off as you complete each lesson:

- [ ] **Lesson 1:** Created Git repository
- [ ] **Lesson 2:** Made commits with meaningful messages
- [ ] **Lesson 3:** Set up GitHub/GitLab account and remote
- [ ] **Lesson 4:** Used git log and git diff effectively
- [ ] **Lesson 5:** Recovered from accidental changes

## 🎓 Skills Gained

After Part 1, you'll know:

### Core Commands
- `git init` - Create repository
- `git add` - Stage changes
- `git commit` - Save snapshot
- `git status` - Check status
- `git log` - View history
- `git diff` - Compare changes
- `git remote` - Manage remotes
- `git push` - Upload to remote
- `git pull` - Download from remote
- `git restore` - Undo changes

### Workflows
- Daily config tracking
- Commit message best practices
- Remote backup strategy
- History navigation
- Error recovery

## 🆘 Common Issues

### "fatal: not a git repository"
**Cause:** Not in a Git repository directory
**Solution:** Run `git init` or `cd` to your repository

### "Author identity unknown"
**Cause:** Git user.name and user.email not set
**Solution:** Configure with `git config --global`

### "Nothing to commit"
**Cause:** No changes to commit or files not staged
**Solution:** Make changes, then `git add` before `git commit`

## 📊 Quick Reference

```bash
# Initialize repository
git init

# Check status
git status

# Stage file
git add filename.cfg

# Stage all files
git add .

# Commit with message
git commit -m "Description of changes"

# View history
git log
git log --oneline

# See changes
git diff

# Add remote
git remote add origin <url>

# Push to remote
git push -u origin main

# Pull from remote
git pull

# Undo working directory changes
git restore filename
```

## 🎯 What's Next?

After completing Part 1:

**Continue to Part 2** for:
- Branching strategies
- Team collaboration
- Merge conflict resolution
- Pull requests

**Or review** if needed:
- Practice exercises in each lesson
- Try the troubleshooting scenarios
- Experiment with different commands

---

**Ready to start?** → [Lesson 1: Repository Setup](01-repository-setup.md)

**Need help?** Each lesson includes:
- Step-by-step instructions
- Expected outputs
- Troubleshooting tips
- Practice exercises

**Time to complete:** 1.5 hours
**Difficulty:** Beginner
**Prerequisites:** Git installed
