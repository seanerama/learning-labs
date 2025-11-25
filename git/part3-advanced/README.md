# Part 3: Advanced Concepts

Master automation, history management, and professional Git workflows for network operations.

## 🎯 Learning Objectives

By the end of Part 3, you'll be able to:
- ✅ Automate configuration backups with Python
- ✅ Clean up commit history with interactive rebase
- ✅ Implement pre-commit validation hooks
- ✅ Create comprehensive network change workflows
- ✅ Use Git for pre/post maintenance snapshots
- ✅ Integrate Git into CI/CD pipelines

## 📚 Lessons

1. **[Automated Backups](01-automated-backups.md)** - Python script for automated device backups
2. **[Interactive Rebase](02-interactive-rebase.md)** - Clean up and reorganize commit history
3. **[Git Hooks](03-git-hooks.md)** - Automated validation and enforcement
4. **[Complete Workflow](04-complete-workflow.md)** - End-to-end network change process

## ⏱️ Time Estimate

**Total:** 1.5 hours
- Automated Backups: 30 minutes
- Interactive Rebase: 20 minutes
- Git Hooks: 20 minutes
- Complete Workflow: 20 minutes

## 🎓 What You'll Build

Throughout Part 3, you'll:
1. Build a Python script that automatically backs up network devices
2. Learn to clean up messy commit history
3. Create validation hooks to prevent common mistakes
4. Implement a complete change management workflow
5. Create pre/post upgrade snapshot system

## 🚀 Prerequisites

**Required:**
- Completed Part 1 and Part 2
- Python 3.7+ installed
- Basic Python knowledge (helpful but not required)
- GitHub or GitLab account with repository

**Optional (for full automation):**
- Network devices to backup (or use test configs)
- Cron/scheduler access for automation
- CI/CD platform access (GitHub Actions, GitLab CI)

**Verify You're Ready:**
```bash
# Check Python version
python3 --version

# Should show 3.7 or higher

# Check you have a repository
cd ~/network-configs
git status

# Check remote access
git remote -v
```

## 📖 Learning Path

Follow the lessons in order:

```
01-automated-backups.md
    ↓
02-interactive-rebase.md
    ↓
03-git-hooks.md
    ↓
04-complete-workflow.md
```

Each lesson builds on the previous one!

## 💡 Key Concepts Covered

### Automation
Scripts that automatically backup, commit, and push configuration changes.

### Interactive Rebase
Powerful tool to rewrite history, combine commits, and maintain clean project history.

### Git Hooks
Scripts that run automatically on Git events (pre-commit, pre-push, etc.).

### Change Management
Complete workflow from planning to deployment using Git as the backbone.

### Snapshot System
Capture configuration state before and after changes for comparison and rollback.

## 🎯 Practice Scenarios

**Scenario 1: Automated Daily Backups**
- Python script backs up all network devices
- Automatic Git commits if changes detected
- Scheduled via cron
- Email alerts on changes

**Scenario 2: Pre-Maintenance Snapshot**
- Capture all configs before maintenance
- Create snapshot branch
- Perform maintenance
- Capture post-maintenance configs
- Compare pre/post automatically

**Scenario 3: Configuration Validation**
- Pre-commit hook validates configs
- Blocks commits with default passwords
- Ensures required commands present
- Validates syntax where possible

**Scenario 4: Complete Change Workflow**
- Change ticket created
- Feature branch from ticket number
- Automated backup captures current state
- Changes made and tested
- PR created with validation checks
- Review and approval
- Merge and deploy
- Post-change verification

## ✅ Completion Checklist

Mark off as you complete each lesson:

- [ ] **Lesson 1:** Created automated backup script
- [ ] **Lesson 2:** Cleaned up commit history with interactive rebase
- [ ] **Lesson 3:** Implemented pre-commit validation hooks
- [ ] **Lesson 4:** Executed complete network change workflow

## 🎓 Skills Gained

After Part 3, you'll know:

### Automation Skills
- Python + Git integration
- Scheduled automation (cron)
- Error handling and logging
- Email notifications

### History Management
- Interactive rebase
- Commit squashing
- History rewriting (safely)
- Maintaining clean project history

### Validation and Quality
- Pre-commit hooks
- Pre-push hooks
- Configuration validation
- Preventing common mistakes

### Professional Workflows
- Change management integration
- Pre/post snapshots
- Rollback procedures
- Documentation automation

## 🆘 Common Issues

### "python: command not found"
**Solution:**
```bash
# Try python3 instead
python3 --version

# Or install Python
# Ubuntu/Debian
sudo apt install python3 python3-pip

# macOS
brew install python3
```

### "Permission denied" on git hooks
**Solution:**
```bash
chmod +x .git/hooks/pre-commit
```

### Rebase conflicts
**Solution:**
```bash
# Resolve conflict
git add <file>
git rebase --continue

# Or abort if needed
git rebase --abort
```

### Automation script fails
**Solution:**
Check logs, ensure Git credentials configured, verify file permissions.

## 📊 Quick Reference

```bash
# Automated backups (Python)
python3 backup_configs.py

# Interactive rebase
git rebase -i HEAD~5          # Last 5 commits
git rebase -i main            # All commits since main

# Rebase actions
pick    # Keep commit as-is
reword  # Change commit message
edit    # Stop to amend commit
squash  # Combine with previous commit
drop    # Remove commit

# Hooks
.git/hooks/pre-commit         # Runs before commit
.git/hooks/pre-push            # Runs before push
.git/hooks/post-commit         # Runs after commit
chmod +x .git/hooks/pre-commit # Make executable

# Snapshot workflow
git checkout -b pre-upgrade-$(date +%Y%m%d)
# ... backup configs ...
git add .
git commit -m "Pre-upgrade snapshot"
git checkout -b post-upgrade-$(date +%Y%m%d)
# ... perform upgrade ...
# ... backup configs again ...
git add .
git commit -m "Post-upgrade snapshot"
git diff pre-upgrade-<date> post-upgrade-<date>
```

## 🎯 What's Next?

After completing Part 3:

**Apply to your environment:**
- Set up automated backups for your devices
- Implement validation hooks
- Create your team's change workflow
- Integrate with your ticketing system

**Further learning:**
- GitHub Actions / GitLab CI for testing
- Advanced Git techniques
- Infrastructure as Code (Ansible, Terraform)
- Configuration management at scale

**Integration with other labs:**
- **Ansible Lab:** Version control your playbooks
- **Python Lab:** Enhance backup scripts
- **Docker Lab:** Containerize backup automation

## 🌟 Advanced Topics (Beyond This Lab)

Once you've mastered Part 3:
- Git submodules for complex projects
- Git LFS for large configuration files
- Advanced branching strategies (GitFlow, trunk-based)
- CI/CD integration for automatic testing
- Configuration drift detection
- Multi-repo management (mono-repo vs. multi-repo)

---

**Ready to start?** → [Lesson 1: Automated Backups](01-automated-backups.md)

**Need help?** Each lesson includes:
- Complete working code examples
- Step-by-step instructions
- Troubleshooting sections
- Practice exercises

**Time to complete:** 1.5 hours
**Difficulty:** Intermediate → Advanced
**Prerequisites:** Parts 1 and 2 completed, Python installed
