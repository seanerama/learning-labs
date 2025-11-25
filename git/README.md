# Git Fundamentals for Network Engineers

Master version control for network configurations and infrastructure automation!

## 🎯 Overview

This comprehensive lab teaches Git through practical network automation scenarios. Learn to track configuration changes, collaborate with teams, and implement professional version control workflows.

## 📚 What You'll Learn

### Part 1: Single Developer Basics (1.5 hours)
- Repository setup and initialization
- Core Git workflow (add, commit, status, log)
- Tracking network device configurations
- Remote repositories for disaster recovery
- Recovering from mistakes

### Part 2: Collaborative Development (2 hours)
- Branching strategies for multi-site networks
- Merging and conflict resolution
- Pull requests and code review
- Team synchronization patterns
- GitHub/GitLab workflows

### Part 3: Advanced Concepts (1.5 hours)
- Automated configuration backups with Python
- Interactive rebase for clean history
- Git hooks for validation
- Pre/post upgrade snapshots
- Complete network change workflow

## 🏗️ Lab Structure

```
git/
├── START-HERE.md              # Start here!
├── QUICKSTART.md             # Git installation
├── README.md                 # This file
│
├── part1-basics/             # Single Developer (1.5 hrs)
│   ├── README.md
│   ├── 01-repository-setup.md
│   ├── 02-basic-workflow.md
│   ├── 03-remote-repositories.md
│   ├── 04-viewing-history.md
│   └── 05-undoing-changes.md
│
├── part2-collaboration/      # Team Workflows (2 hrs)
│   ├── README.md
│   ├── 01-understanding-branches.md
│   ├── 02-merging-conflicts.md
│   ├── 03-github-gitlab.md
│   ├── 04-pull-requests.md
│   └── 05-team-workflows.md
│
├── part3-advanced/           # Advanced Topics (1.5 hrs)
│   ├── README.md
│   ├── 01-automated-backups.md
│   ├── 02-rebase-history.md
│   ├── 03-git-hooks.md
│   └── 04-complete-workflow.md
│
└── examples/                 # Working code examples
    ├── switch-configs/
    ├── backup-automation/
    └── hooks/
```

## 🌟 Why Git for Network Engineers?

### Configuration Management
- **Track every change** to device configurations
- **Know who changed what** and when
- **Rollback instantly** to previous working configs

### Disaster Recovery
- **Remote backups** of all configurations
- **Version history** going back months or years
- **Quick restoration** when devices fail

### Team Collaboration
- **Parallel work** on different sites or features
- **Code review** before deploying changes
- **Merge conflict detection** prevents overwriting

### Automation Integration
- **Automated backups** with Python scripts
- **Pre-commit validation** prevents bad configs
- **CI/CD pipelines** for infrastructure changes

## 🚀 Quick Start

1. **Install Git:**
   ```bash
   cat QUICKSTART.md
   ```

2. **Start learning:**
   ```bash
   cd part1-basics/
   cat README.md
   ```

3. **Follow the lessons** in order within each part

## 📖 Lessons Overview

### Part 1: Single Developer Basics

**Lesson 1: Repository Setup**
- Creating your first Git repository
- Understanding the .git directory
- Setting up for network configs

**Lesson 2: Basic Workflow**
- The add-commit-status cycle
- Writing meaningful commit messages
- Tracking switch configurations

**Lesson 3: Remote Repositories**
- Understanding GitHub and GitLab
- Creating accounts and repositories
- Pushing configs for backup
- Cloning to multiple locations

**Lesson 4: Viewing History**
- Using git log effectively
- Comparing configurations with git diff
- Finding when changes were made

**Lesson 5: Undoing Changes**
- Restoring modified files
- Reverting to previous configs
- Recovering from mistakes

### Part 2: Collaborative Development

**Lesson 1: Understanding Branches**
- What are branches and why use them
- Creating branches for each site
- Switching between branches
- Branch naming conventions

**Lesson 2: Merging and Conflicts**
- Merging site-specific changes
- Understanding merge conflicts
- Resolving conflicts in configs
- Fast-forward vs. three-way merges

**Lesson 3: GitHub and GitLab**
- What are GitHub/GitLab?
- Creating accounts (step-by-step)
- SSH key setup
- Web interface overview
- Public vs. private repositories

**Lesson 4: Pull Requests**
- Creating pull requests
- Code review process
- Commenting on changes
- Merging pull requests

**Lesson 5: Team Workflows**
- Feature branch workflow
- Keeping branches synchronized
- Handling multiple contributors
- Best practices

### Part 3: Advanced Concepts

**Lesson 1: Automated Backups**
- Python script for device backups
- Automatic Git commits
- Scheduling with cron
- Email notifications on changes

**Lesson 2: Rebase and History**
- Interactive rebase
- Squashing commits
- Rewriting history safely
- When to rebase vs. merge

**Lesson 3: Git Hooks**
- Pre-commit validation
- Preventing bad passwords
- Enforcing naming conventions
- Custom validation rules

**Lesson 4: Complete Workflow**
- Pre/post upgrade snapshots
- Change request process
- Rollback procedures
- Production deployment

## 🎓 Learning Outcomes

After completing this lab, you will:

✅ **Understand Git fundamentals**
- Repository initialization and cloning
- Add, commit, push, pull workflow
- Branching and merging

✅ **Manage network configurations**
- Track all device config changes
- Maintain history for compliance
- Quick rollback capabilities

✅ **Collaborate effectively**
- Use branches for parallel work
- Review team members' changes
- Resolve conflicts confidently

✅ **Automate workflows**
- Automated configuration backups
- Pre-commit validation
- CI/CD integration basics

✅ **Implement best practices**
- Meaningful commit messages
- Clean commit history
- Secure credential handling

## 🌐 GitHub vs. GitLab

This lab covers both GitHub and GitLab:

### GitHub
- Most popular Git hosting platform
- Free public and private repositories
- Extensive CI/CD with GitHub Actions
- Large open-source community
- **Best for:** Public projects, OSS, documentation

### GitLab
- Complete DevOps platform
- Self-hosted or cloud options
- Built-in CI/CD pipelines
- Advanced security features
- **Best for:** Private enterprise, full DevOps lifecycle

**Both are covered** in Part 2, Lesson 3 with step-by-step account setup.

You only need **one** for this lab - choose based on your organization's preference!

## 💡 Practical Scenarios

### Scenario 1: Single Site Management
Track configurations for a single network site:
- Initialize repository
- Add switch configs
- Commit changes daily
- Push to remote for backup

### Scenario 2: Multi-Site Deployment
Manage configs across multiple branch offices:
- Create branch per site
- Customize configs per location
- Merge common changes
- Handle site-specific differences

### Scenario 3: Team Collaboration
Multiple engineers working on infrastructure:
- Feature branches for changes
- Pull requests for review
- Peer review before deployment
- Merge to main after approval

### Scenario 4: Automated Operations
Production-ready automation:
- Automated nightly backups
- Pre-commit validation
- Change tracking and audit
- Rollback procedures

## 🔧 Prerequisites

### Required
- Basic command-line knowledge
- Text editor (nano, vim, or VS Code)
- Git installed (see QUICKSTART.md)

### Helpful (but not required)
- Familiarity with network device configs
- Basic Python knowledge (for Part 3)
- Understanding of SSH

### Time Commitment
- **Minimum:** 1.5 hours (Part 1 only)
- **Recommended:** 5 hours (all parts)
- **Complete:** 8 hours (with all exercises)

## 📊 Progress Tracking

Track your progress through the lab:

### Part 1 Checklist
- [ ] Create your first repository
- [ ] Make commits with meaningful messages
- [ ] Set up remote repository
- [ ] Push and pull changes
- [ ] Recover from mistakes

### Part 2 Checklist
- [ ] Create and switch branches
- [ ] Merge branches
- [ ] Resolve merge conflicts
- [ ] Set up GitHub/GitLab account
- [ ] Create first pull request

### Part 3 Checklist
- [ ] Automate configuration backups
- [ ] Clean up commit history
- [ ] Implement validation hooks
- [ ] Complete full change workflow

## 🎯 Real-World Use Cases

### Configuration Backup
**Problem:** Switch configs lost after hardware failure
**Git Solution:** Clone repository, restore last known good config

### Change Tracking
**Problem:** Unknown config change broke network
**Git Solution:** `git log` and `git diff` identify exact change and author

### Team Collaboration
**Problem:** Two engineers modify same device simultaneously
**Git Solution:** Branches prevent conflicts, merge combines changes safely

### Audit Compliance
**Problem:** Need to prove when security policy was implemented
**Git Solution:** Commit history with timestamps and authors

### Rollback
**Problem:** New config causes issues in production
**Git Solution:** `git revert` or `git checkout` restores previous version

## 🆘 Getting Help

### Within Each Lesson
- **Common Issues** section with solutions
- **Troubleshooting** tips
- **FAQ** for frequently asked questions

### Additional Resources
- `git help <command>` - Built-in documentation
- `git <command> --help` - Detailed command help
- GitHub Documentation: https://docs.github.com
- GitLab Documentation: https://docs.gitlab.com

### Lab Support
- Each lesson includes debugging sections
- Step-by-step verification commands
- Expected outputs for comparison

## 🌟 Best Practices Covered

### Commit Messages
✅ Write clear, descriptive messages
✅ Use present tense ("Add VLAN" not "Added VLAN")
✅ Include ticket/change numbers
❌ Avoid vague messages ("fix", "update")

### Branching
✅ Use descriptive branch names
✅ Keep branches short-lived
✅ Delete merged branches
❌ Don't commit directly to main

### Security
✅ Use SSH keys for authentication
✅ Never commit passwords
✅ Use .gitignore for sensitive files
❌ Don't commit API keys or secrets

### Collaboration
✅ Pull before pushing
✅ Review others' code
✅ Keep branches updated
❌ Don't force push to shared branches

## 📚 What's Next After This Lab?

Once you've mastered Git:

### Integrate with Other Labs
- **Ansible Lab:** Version control Ansible playbooks
- **Python Lab:** Track automation scripts
- **Docker Lab:** Version control Dockerfiles

### Advanced Topics (Beyond This Lab)
- Git submodules for complex projects
- Git LFS for large files
- Advanced branching strategies (GitFlow)
- CI/CD pipeline integration

### Apply to Your Work
- Start tracking production configs
- Implement automated backups
- Establish team workflows
- Document in version control

## 🎉 Ready to Start?

Follow this learning path:

1. **[START-HERE.md](START-HERE.md)** - Lab overview
2. **[QUICKSTART.md](QUICKSTART.md)** - Install and configure Git
3. **[Part 1: Single Developer Basics](part1-basics/README.md)** - Core concepts
4. **[Part 2: Collaborative Development](part2-collaboration/README.md)** - Team workflows
5. **[Part 3: Advanced Concepts](part3-advanced/README.md)** - Automation and power tools

---

**Total Time:** 5 hours
**Difficulty:** Beginner → Intermediate
**Platform:** Universal (applies to all network vendors)
**Prerequisites:** Command-line basics, Git installed

**Questions?** Each lesson includes troubleshooting and FAQs.
**Stuck?** Check the Common Issues section in each lesson.
**Need help?** Review lesson objectives and verification steps.

**Let's master Git!** 🚀
