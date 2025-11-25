# Lesson 1: Repository Basics and Core Workflow

Master Git fundamentals by tracking your first network device configuration!

## 🎯 Objectives

By the end of this lesson, you'll be able to:
- Create and initialize Git repositories
- Understand the basic Git workflow (add, commit, status)
- Track changes to network device configurations
- Write meaningful commit messages
- View your change history

## 📝 What You'll Learn

- Repository initialization
- The add-commit cycle
- Staging area concept
- Status checking
- Commit history viewing
- Working with configuration files

## 🚀 Part 1: Creating Your First Repository

### Step 1: Create a Project Directory

```bash
# Create directory for network configurations
mkdir ~/network-configs
cd ~/network-configs

# Verify you're in the right place
pwd
# Output: /home/username/network-configs
```

### Step 2: Initialize Git Repository

```bash
# Initialize Git repository
git init

# Output:
# Initialized empty Git repository in /home/username/network-configs/.git/
```

**What just happened?**
- Git created a hidden `.git` directory
- This directory stores ALL version history
- Your folder is now a Git repository!

```bash
# View the .git directory (optional)
ls -la
# You'll see: .git/

# Check repository status
git status
# Output: On branch main
#         No commits yet
#         nothing to commit (create/copy files and use "git add" to track)
```

### Step 3: Understand the Repository Structure

```
network-configs/              ← Your working directory
├── .git/                    ← Git's database (don't modify!)
│   ├── objects/            ← Stores all commits
│   ├── refs/               ← Branches and tags
│   ├── HEAD                ← Current branch pointer
│   └── config              ← Repository settings
└── (your files here)        ← Files you're tracking
```

## 🚀 Part 2: The Basic Workflow

### Step 4: Create Your First Configuration File

Let's create a Cisco switch configuration:

```bash
# Create a switch configuration file
cat > SW-ACCESS-01.cfg << 'EOF'
hostname SW-ACCESS-01
!
vlan 10
 name DATA
vlan 20
 name VOICE
vlan 99
 name MANAGEMENT
!
interface GigabitEthernet0/1
 description UPLINK-TO-CORE
 switchport mode trunk
 switchport trunk allowed vlan 10,20,99
!
interface range GigabitEthernet0/2-24
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
!
line vty 0 4
 login local
 transport input ssh
!
end
EOF

# Verify file was created
ls -l
# Output: SW-ACCESS-01.cfg
```

### Step 5: Check Repository Status

```bash
git status
```

Output:
```
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        SW-ACCESS-01.cfg

nothing added to commit but untracked files present (use "git add" to track)
```

**Understanding the output:**
- `Untracked files` = Files Git sees but isn't tracking yet
- Git is telling us to use `git add` to start tracking

### Step 6: Stage the File (Add to Staging Area)

```bash
# Add file to staging area
git add SW-ACCESS-01.cfg

# Check status again
git status
```

Output:
```
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   SW-ACCESS-01.cfg
```

**What changed?**
- File moved from "Untracked" to "Changes to be committed"
- File is now in the **staging area**
- Ready to be committed!

### Step 7: Create Your First Commit

```bash
# Commit the staged file
git commit -m "Initial switch configuration for SW-ACCESS-01"
```

Output:
```
[main (root-commit) a1b2c3d] Initial switch configuration for SW-ACCESS-01
 1 file changed, 20 insertions(+)
 create mode 100644 SW-ACCESS-01.cfg
```

**What just happened?**
- Git created a snapshot of your project
- Assigned it a unique ID (a1b2c3d...)
- Saved your commit message
- This is your first commit!

```bash
# Check status now
git status
```

Output:
```
On branch main
nothing to commit, working tree clean
```

Clean! No pending changes.

## 🚀 Part 3: Making Changes and More Commits

### Step 8: Modify the Configuration

Let's add a new VLAN:

```bash
# Edit the file (add VLAN 30 for GUEST)
# You can use nano, vim, or any text editor

# For this example, we'll use sed to add it
sed -i '/vlan 99/a vlan 30\n name GUEST' SW-ACCESS-01.cfg

# Verify the change
grep -A1 "vlan 30" SW-ACCESS-01.cfg
# Output:
# vlan 30
#  name GUEST
```

### Step 9: Check What Changed

```bash
# Check status
git status
```

Output:
```
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   SW-ACCESS-01.cfg

no changes added to commit (use "git add" and/or "git commit -a")
```

**See the difference:**

```bash
# View exact changes
git diff
```

Output (example):
```diff
diff --git a/SW-ACCESS-01.cfg b/SW-ACCESS-01.cfg
index a1b2c3d..d4e5f6g 100644
--- a/SW-ACCESS-01.cfg
+++ b/SW-ACCESS-01.cfg
@@ -7,6 +7,8 @@ vlan 20
  name VOICE
 vlan 99
  name MANAGEMENT
+vlan 30
+ name GUEST
 !
 interface GigabitEthernet0/1
  description UPLINK-TO-CORE
```

**Understanding git diff:**
- Lines starting with `+` = Added lines
- Lines starting with `-` = Removed lines (none here)
- Lines without `+/-` = Context (unchanged)

### Step 10: Commit the Change

```bash
# Stage the modified file
git add SW-ACCESS-01.cfg

# Commit with descriptive message
git commit -m "Add GUEST VLAN (VLAN 30) for visitor access"
```

Output:
```
[main b2c3d4e] Add GUEST VLAN (VLAN 30) for visitor access
 1 file changed, 2 insertions(+)
```

### Step 11: View Your History

```bash
# View commit history
git log
```

Output:
```
commit b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1 (HEAD -> main)
Author: Your Name <your.email@example.com>
Date:   Mon Jan 15 10:30:00 2024 -0500

    Add GUEST VLAN (VLAN 30) for visitor access

commit a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
Author: Your Name <your.email@example.com>
Date:   Mon Jan 15 10:25:00 2024 -0500

    Initial switch configuration for SW-ACCESS-01
```

**Compact view:**

```bash
# One line per commit
git log --oneline
```

Output:
```
b2c3d4e (HEAD -> main) Add GUEST VLAN (VLAN 30) for visitor access
a1b2c3d Initial switch configuration for SW-ACCESS-01
```

## 💡 Key Concepts

### The Three Areas

```
┌─────────────────┐
│ Working         │  ← Files you're editing
│ Directory       │
└────────┬────────┘
         │ git add
         ▼
┌─────────────────┐
│ Staging Area    │  ← Files ready to commit
│ (Index)         │
└────────┬────────┘
         │ git commit
         ▼
┌─────────────────┐
│ Repository      │  ← Committed snapshots
│ (.git)          │
└─────────────────┘
```

### The Basic Workflow

```
1. Modify files         → Working Directory
2. git add             → Stage changes
3. git commit          → Save snapshot
4. Repeat!
```

### File States

```
Untracked    → Git doesn't know about the file
Modified     → File changed since last commit
Staged       → File ready to be committed
Committed    → File safely stored in repository
```

## 🧪 Practice Exercises

### Exercise 1: Add Security Configuration

Add port security to access ports:

```bash
# Edit SW-ACCESS-01.cfg
# Add these lines after the interface range configuration:

interface range GigabitEthernet0/2-24
 switchport mode access
 switchport access vlan 10
 switchport port-security maximum 2
 switchport port-security violation restrict
 switchport port-security mac-address sticky
 spanning-tree portfast

# Check what changed
git diff

# Stage and commit
git add SW-ACCESS-01.cfg
git commit -m "Add port security to access ports"

# Verify with log
git log --oneline
```

<details>
<summary>Show expected output</summary>

```bash
$ git log --oneline
c3d4e5f (HEAD -> main) Add port security to access ports
b2c3d4e Add GUEST VLAN (VLAN 30) for visitor access
a1b2c3d Initial switch configuration for SW-ACCESS-01
```
</details>

### Exercise 2: Multiple Files

Create a second switch configuration:

```bash
# Create another switch config
cat > SW-ACCESS-02.cfg << 'EOF'
hostname SW-ACCESS-02
!
vlan 10
 name DATA
vlan 20
 name VOICE
vlan 99
 name MANAGEMENT
vlan 30
 name GUEST
!
interface GigabitEthernet0/1
 description UPLINK-TO-CORE
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,99
!
end
EOF

# Check status
git status

# Add both files (if SW-ACCESS-01 was modified)
git add .

# Commit
git commit -m "Add SW-ACCESS-02 configuration"

# Verify
git log --oneline
ls -l
```

### Exercise 3: View File at Specific Commit

View what a file looked like in the past:

```bash
# Get commit hash of first commit
git log --oneline

# View file as it was in first commit (use your actual hash)
git show a1b2c3d:SW-ACCESS-01.cfg

# Compare to current version
cat SW-ACCESS-01.cfg
```

## 📊 Common Commands Reference

```bash
# Repository basics
git init                          # Create new repository
git status                        # Check current state

# Staging and committing
git add <file>                    # Stage specific file
git add .                         # Stage all changes
git commit -m "message"           # Commit staged changes
git commit -am "message"          # Stage and commit (tracked files only)

# Viewing history
git log                           # Full commit history
git log --oneline                 # Compact history
git log --oneline --graph         # Visual branch graph
git log -n 5                      # Last 5 commits
git log --author="Name"           # Commits by author

# Viewing changes
git diff                          # Changes not staged
git diff --staged                 # Changes staged for commit
git diff HEAD                     # All changes since last commit
git show <commit>                 # Show specific commit

# Information
git show <commit>:<file>          # File contents at commit
git log --follow <file>           # History of specific file
```

## ✅ Verification Checklist

Make sure you can:

- [ ] Initialize a Git repository with `git init`
- [ ] Check repository status with `git status`
- [ ] Stage files with `git add`
- [ ] Create commits with meaningful messages
- [ ] View commit history with `git log`
- [ ] See changes with `git diff`
- [ ] Understand working directory vs staging area vs repository

## ❓ Common Issues

### Issue: "fatal: not a git repository"

**Cause:** You're not in a Git repository directory

**Solution:**
```bash
# Check if .git exists
ls -la

# If not, either:
# 1. Initialize here
git init

# 2. Or navigate to your repository
cd ~/network-configs
```

### Issue: "Author identity unknown"

**Cause:** Git doesn't know who you are

**Solution:**
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify
git config user.name
git config user.email
```

### Issue: "nothing to commit"

**Cause:** No changes to commit, or forgot to stage

**Solution:**
```bash
# Check what's changed
git status

# If files are modified but not staged:
git add <files>

# Then commit
git commit -m "message"
```

### Issue: Committed wrong file

**Solution:**
```bash
# If you haven't pushed yet, undo last commit but keep changes
git reset --soft HEAD~1

# Files are now staged again, unstage what you don't want
git restore --staged <unwanted-file>

# Commit again with correct files
git commit -m "message"
```

## 🎯 Best Practices

### Commit Messages

✅ **GOOD:**
```bash
git commit -m "Add GUEST VLAN (VLAN 30) for visitor wireless access"
git commit -m "Update trunk port to include VLAN 30"
git commit -m "Enable port security on access ports (CHG12345)"
```

❌ **BAD:**
```bash
git commit -m "update"
git commit -m "fix"
git commit -m "asdf"
git commit -m "changes"
```

### Commit Message Guidelines

1. **Use present tense:** "Add feature" not "Added feature"
2. **Be specific:** What and why, not how
3. **Keep first line under 50 characters**
4. **Include ticket numbers:** "Fix login bug (TICKET-123)"
5. **Explain why if not obvious**

### When to Commit

✅ **DO commit when:**
- You completed a logical unit of work
- Configuration passes syntax check
- Before testing risky changes
- End of day (if changes work)

❌ **DON'T commit when:**
- Code doesn't work yet
- You're in the middle of a change
- Files contain temporary test data

## 🎉 Lesson Complete!

You now know:

✅ How to create Git repositories
✅ The basic add-commit workflow
✅ How to track configuration changes
✅ How to view history and changes
✅ Best practices for commits

### What's Next?

**Next Lesson:** [Remote Repositories with GitHub/GitLab](02-remote-github-gitlab.md)

Learn to:
- Understand what GitHub and GitLab are
- Create accounts and SSH keys
- Push configurations for backup
- Clone repositories to multiple locations

---

**Lesson Duration:** 30 minutes
**Difficulty:** Beginner
**Skills:** Repository basics, staging, committing, viewing history
