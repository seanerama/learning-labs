# Lesson 1: Branching Strategies for Multi-Site Networks

Learn to use Git branches to safely manage configurations for multiple network sites in parallel.

## 🎯 Objectives

By the end of this lesson, you'll be able to:
- Understand what branches are and why they're essential
- Create and switch between branches
- Manage configurations for multiple sites independently
- Use branches for testing before production deployment
- Follow professional branching naming conventions

## 📝 What You'll Learn

- Branch fundamentals and use cases
- Creating and switching branches
- Multi-site configuration management
- Feature branch workflow
- Branch naming best practices

## 🌿 Part 1: Understanding Branches

### What is a Branch?

A **branch** is an independent line of development. Think of it as a parallel universe for your repository where you can make changes without affecting the main codebase.

**Network Engineering Analogy:**
- **Main branch** = Production configurations (live on devices)
- **Feature branch** = Lab/staging environment for testing changes
- **Site branch** = Site-specific customizations

### Why Use Branches?

**Scenario 1: Testing Changes**
```
main branch (production configs)
    ↓
feature-branch (test new security settings)
    ↓
merge back when tested ✓
```

**Scenario 2: Multi-Site Management**
```
main branch (standard config template)
    ├── site-chicago (Chicago customizations)
    ├── site-newyork (New York customizations)
    └── site-dallas (Dallas customizations)
```

**Scenario 3: Team Collaboration**
```
main branch
    ├── engineer1-vlan-updates
    ├── engineer2-security-hardening
    └── engineer3-qos-config
```

### Branch Benefits

✅ **Safe experimentation** - Test without breaking production
✅ **Parallel development** - Multiple people work simultaneously
✅ **Easy rollback** - Discard failed experiments
✅ **Code review** - Review changes before deploying
✅ **Clear history** - See what changed and why

## 🔧 Part 2: Branch Basics

### View Existing Branches

```bash
cd ~/network-configs

# List local branches
git branch

# Output:
# * main

# The * shows your current branch
```

```bash
# List all branches (including remote)
git branch -a

# Output:
# * main
#   remotes/origin/main
```

### Create a New Branch

**Method 1: Create and switch separately**
```bash
# Create new branch
git branch test-branch

# List branches
git branch
# Output:
#   main
# * test-branch

# Switch to new branch
git checkout test-branch
# Output: Switched to branch 'test-branch'
```

**Method 2: Create and switch in one command** (recommended)
```bash
# Create and switch in one step
git checkout -b my-feature

# Output: Switched to a new branch 'my-feature'
```

**Method 3: Modern syntax**
```bash
# Newer Git versions (2.23+)
git switch -c my-feature

# -c means "create"
```

### Check Current Branch

```bash
# Method 1: git branch (shows * next to current)
git branch

# Method 2: git status
git status
# Output: On branch my-feature

# Method 3: Command prompt (if configured)
# Often shows in PS1: ~/network-configs (my-feature)$
```

### Switch Between Branches

```bash
# Switch to existing branch
git checkout main
# Output: Switched to branch 'main'

# Or use modern syntax
git switch main
```

**⚠️ Important:** Uncommitted changes come with you when switching branches!

```bash
# If you have uncommitted changes:
git status
# Output: Changes not staged for commit: modified: SW-ACCESS-01.cfg

git checkout main
# Output: error: Your local changes would be overwritten by checkout

# Solution 1: Commit your changes first
git add .
git commit -m "Save work in progress"
git checkout main

# Solution 2: Stash changes temporarily
git stash
git checkout main
git stash pop  # Reapply changes when you come back
```

## 🏢 Part 3: Multi-Site Configuration Management

### Scenario Setup

You manage network configs for three branch offices:
- **Chicago** - Manufacturing facility (needs industrial IoT VLANs)
- **New York** - Corporate headquarters (needs guest and conference VLANs)
- **Dallas** - Call center (needs quality of service for VoIP)

Each site shares a common base config but has unique requirements.

### Create Site Branches

```bash
cd ~/network-configs

# Ensure you're on main
git checkout main

# Create Chicago branch
git checkout -b site-chicago
# Output: Switched to a new branch 'site-chicago'

# Verify
git branch
# Output:
#   main
# * site-chicago
```

### Customize for Chicago Site

```bash
# Modify the switch config for Chicago
cat > SW-CHI-ACCESS-01.cfg << 'EOF'
hostname SW-CHI-ACCESS-01
!
vlan 10
 name DATA
vlan 20
 name VOICE
vlan 30
 name IOT-SENSORS
vlan 40
 name IOT-CONTROLLERS
vlan 99
 name MANAGEMENT
!
interface GigabitEthernet0/1
 description UPLINK-TO-CORE-CHI
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40,99
!
interface range GigabitEthernet0/2-10
 description DATA-PORTS
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
!
interface range GigabitEthernet0/11-15
 description IOT-SENSOR-PORTS
 switchport mode access
 switchport access vlan 30
 spanning-tree portfast
!
interface range GigabitEthernet0/16-20
 description IOT-CONTROLLER-PORTS
 switchport mode access
 switchport access vlan 40
 spanning-tree portfast
!
line vty 0 4
 transport input ssh
!
end
EOF
```

```bash
# Check status
git status
# Output:
# On branch site-chicago
# Untracked files:
#   SW-CHI-ACCESS-01.cfg

# Add and commit
git add SW-CHI-ACCESS-01.cfg
git commit -m "Add Chicago site configuration with IoT VLANs"
```

### Create New York Branch

```bash
# Go back to main (fresh start)
git checkout main

# Create NY branch
git checkout -b site-newyork
```

```bash
# Customize for New York
cat > SW-NYC-ACCESS-01.cfg << 'EOF'
hostname SW-NYC-ACCESS-01
!
vlan 10
 name DATA
vlan 20
 name VOICE
vlan 30
 name GUEST-NETWORK
vlan 40
 name CONFERENCE-ROOMS
vlan 99
 name MANAGEMENT
!
interface GigabitEthernet0/1
 description UPLINK-TO-CORE-NYC
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40,99
!
interface range GigabitEthernet0/2-15
 description OFFICE-DATA-PORTS
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
!
interface range GigabitEthernet0/16-20
 description CONFERENCE-ROOM-PORTS
 switchport mode access
 switchport access vlan 40
 spanning-tree portfast
!
interface range GigabitEthernet0/21-24
 description GUEST-NETWORK-PORTS
 switchport mode access
 switchport access vlan 30
 spanning-tree portfast
 spanning-tree bpduguard enable
!
line vty 0 4
 transport input ssh
!
end
EOF
```

```bash
git add SW-NYC-ACCESS-01.cfg
git commit -m "Add New York HQ configuration with guest and conference VLANs"
```

### Create Dallas Branch

```bash
# Return to main
git checkout main

# Create Dallas branch
git checkout -b site-dallas
```

```bash
# Customize for Dallas (call center with QoS)
cat > SW-DAL-ACCESS-01.cfg << 'EOF'
hostname SW-DAL-ACCESS-01
!
vlan 10
 name DATA
vlan 20
 name VOICE
vlan 99
 name MANAGEMENT
!
mls qos
!
interface GigabitEthernet0/1
 description UPLINK-TO-CORE-DAL
 switchport mode trunk
 switchport trunk allowed vlan 10,20,99
 mls qos trust dscp
!
interface range GigabitEthernet0/2-24
 description CALL-CENTER-DESK-PORTS
 switchport mode access
 switchport access vlan 10
 switchport voice vlan 20
 spanning-tree portfast
 mls qos trust cos
 auto qos voip cisco-phone
!
line vty 0 4
 transport input ssh
!
end
EOF
```

```bash
git add SW-DAL-ACCESS-01.cfg
git commit -m "Add Dallas call center configuration with VoIP QoS"
```

### View Your Branch Structure

```bash
# List all branches
git branch
# Output:
#   main
#   site-chicago
#   site-dallas
# * site-newyork

# View commit history across branches
git log --oneline --graph --all --decorate
```

**Output:**
```
* d4e5f6g (HEAD -> site-dallas) Add Dallas call center configuration with VoIP QoS
| * c3d4e5f (site-newyork) Add New York HQ configuration with guest and conference VLANs
|/
| * b2c3d4e (site-chicago) Add Chicago site configuration with IoT VLANs
|/
* a1b2c3d (origin/main, main) Initial switch configuration
```

This graph shows three branches splitting from main!

## 🔀 Part 4: Working with Branches

### Compare Branches

```bash
# See what's different between branches
git diff main site-chicago

# See only which files differ
git diff --name-only main site-chicago
# Output: SW-CHI-ACCESS-01.cfg

# Compare two site branches
git diff site-chicago site-newyork
```

### View Files in Different Branches

```bash
# You're on site-dallas
git branch
# * site-dallas

# List files in current branch
ls *.cfg
# Output: SW-DAL-ACCESS-01.cfg

# Switch to different branch
git checkout site-chicago
ls *.cfg
# Output: SW-CHI-ACCESS-01.cfg

# Switch to another
git checkout site-newyork
ls *.cfg
# Output: SW-NYC-ACCESS-01.cfg
```

**Notice:** Each branch has its own file! This is perfect for site-specific configs.

### View File from Another Branch Without Switching

```bash
# Currently on site-newyork
# Want to see Dallas config without switching

git show site-dallas:SW-DAL-ACCESS-01.cfg
```

### Push Branches to Remote

```bash
# Push Chicago branch
git checkout site-chicago
git push -u origin site-chicago

# Output:
# To github.com:yourusername/network-configs.git
#  * [new branch]      site-chicago -> site-chicago

# Push all branches
git push --all origin
```

### View Remote Branches

```bash
# Fetch remote branch info
git fetch

# List remote branches
git branch -r
# Output:
#   origin/main
#   origin/site-chicago
#   origin/site-dallas
#   origin/site-newyork

# List all (local and remote)
git branch -a
```

## 📋 Part 5: Feature Branch Workflow

### Common Pattern for Changes

This is the professional workflow for making any configuration change:

```bash
# 1. Start from updated main
git checkout main
git pull

# 2. Create feature branch
git checkout -b feature/add-syslog-servers

# 3. Make changes
cat >> SW-ACCESS-01.cfg << 'EOF'
!
logging buffered 51200
logging host 10.1.1.10
logging host 10.1.1.11
logging trap informational
!
EOF

# 4. Commit changes
git add SW-ACCESS-01.cfg
git commit -m "Add syslog servers for centralized logging - CHG0012345"

# 5. Push to remote
git push -u origin feature/add-syslog-servers

# 6. Create pull request (next lesson)
# 7. After review and merge, delete branch
git checkout main
git pull
git branch -d feature/add-syslog-servers
```

### Why This Pattern?

✅ **main stays clean** - Only reviewed, tested changes
✅ **Parallel work** - Multiple features in progress
✅ **Easy review** - Clear what changed and why
✅ **Safe rollback** - Can abandon feature branch if needed

## 🏷️ Part 6: Branch Naming Conventions

### Professional Naming Patterns

**Feature branches:**
```bash
feature/add-snmp-monitoring
feature/enable-port-security
feature/update-ntp-servers
```

**Site branches:**
```bash
site-chicago
site-newyork
site-dallas-datacenter
```

**Bugfix branches:**
```bash
bugfix/fix-vlan-trunk-config
fix/correct-stp-priority
hotfix/security-acl-urgent
```

**Change ticket branches:**
```bash
CHG0012345-add-vlans
INC0067890-fix-routing
```

### Naming Best Practices

✅ **DO:**
- Use lowercase with hyphens: `feature-name`
- Be descriptive: `add-guest-wifi-vlan`
- Include ticket numbers: `CHG0012345-description`
- Use prefixes: `feature/`, `bugfix/`, `site-`

❌ **DON'T:**
- Use spaces: `my feature branch` (breaks Git)
- Be vague: `test`, `temp`, `stuff`
- Use special characters: `feature@123`, `branch#1`

## 🧪 Practice Exercises

### Exercise 1: Create a Security Hardening Branch

Create a branch to test security improvements:

```bash
cd ~/network-configs
git checkout main
git checkout -b feature/port-security

# Add port security config
cat > security-hardening.txt << 'EOF'
# Port Security Configuration

interface range GigabitEthernet0/2-24
 switchport port-security maximum 2
 switchport port-security violation restrict
 switchport port-security mac-address sticky
!
spanning-tree portfast bpduguard default
!
no ip http server
no ip http secure-server
EOF

git add security-hardening.txt
git commit -m "Document port security hardening standards"
git push -u origin feature/port-security
```

### Exercise 2: Create Branch for Each Site

Practice the multi-site pattern:

```bash
# Create branches for three more sites
git checkout main
git checkout -b site-boston

# Add Boston config
echo "hostname SW-BOS-ACCESS-01" > SW-BOS-ACCESS-01.cfg
git add SW-BOS-ACCESS-01.cfg
git commit -m "Add Boston site initial config"

# Repeat for other sites
git checkout main
git checkout -b site-miami

git checkout main
git checkout -b site-seattle

# View all branches
git branch
```

### Exercise 3: Compare Branches

```bash
# Compare what's different between sites
git diff site-chicago site-newyork

# List files unique to each branch
git diff --name-only site-chicago site-dallas

# View commit history
git log --oneline --graph --all
```

### Exercise 4: Test Branch Switching

```bash
# Switch between branches and observe files
git checkout site-chicago
ls *.cfg
cat SW-CHI-ACCESS-01.cfg | grep hostname

git checkout site-newyork
ls *.cfg
cat SW-NYC-ACCESS-01.cfg | grep hostname

git checkout site-dallas
ls *.cfg
cat SW-DAL-ACCESS-01.cfg | grep hostname

# Return to main
git checkout main
```

## 📊 Commands Reference

```bash
# Create branch
git branch branch-name                  # Create only
git checkout -b branch-name             # Create and switch
git switch -c branch-name               # Create and switch (new syntax)

# List branches
git branch                              # Local branches
git branch -r                           # Remote branches
git branch -a                           # All branches

# Switch branches
git checkout branch-name
git switch branch-name                  # New syntax

# Rename branch
git branch -m old-name new-name

# Delete branch
git branch -d branch-name               # Safe delete (only if merged)
git branch -D branch-name               # Force delete

# Compare branches
git diff branch1 branch2
git diff --name-only branch1 branch2

# View file from another branch
git show branch-name:filename

# Push branch to remote
git push -u origin branch-name          # First time
git push                                # After tracking is set

# Push all branches
git push --all origin

# Delete remote branch
git push origin --delete branch-name
```

## ✅ Verification Checklist

Make sure you can:

- [ ] Create a new branch
- [ ] Switch between branches
- [ ] See which branch you're on
- [ ] List all branches (local and remote)
- [ ] Create site-specific configuration branches
- [ ] Compare files between branches
- [ ] Push branches to remote repository
- [ ] Use proper branch naming conventions

## ❓ Common Issues

### Issue: "Already exists" when creating branch

**Cause:** Branch name already used
```bash
# List existing branches
git branch -a

# Use different name or delete old branch
git branch -d old-branch-name
```

### Issue: Lost changes when switching branches

**Cause:** Uncommitted changes were discarded
```bash
# Always commit or stash before switching
git stash               # Save changes temporarily
git checkout main
git stash pop          # Restore changes
```

### Issue: Can't switch - "uncommitted changes"

**Cause:** Changes would be overwritten
```bash
# Option 1: Commit changes
git add .
git commit -m "Save work"

# Option 2: Stash changes
git stash
```

### Issue: Don't see remote branches

**Cause:** Haven't fetched from remote
```bash
git fetch
git branch -r
```

## 🎯 Best Practices

### Branch Management

✅ **DO:**
- Create branches from updated main: `git checkout main && git pull`
- Use descriptive names: `feature/add-snmp-monitoring`
- Delete merged branches: `git branch -d feature-name`
- Push branches for backup: `git push -u origin branch-name`
- Keep branches short-lived (days, not months)

❌ **DON'T:**
- Make commits directly to main (use branches)
- Keep dozens of stale branches
- Use generic names: `test`, `temp`, `my-branch`
- Forget to push branches (local only = no backup)

### Workflow Pattern

For every change, follow this pattern:
```bash
git checkout main          # 1. Start from main
git pull                   # 2. Get latest
git checkout -b feature    # 3. Create branch
# ... make changes ...
git add .                  # 4. Stage
git commit -m "msg"        # 5. Commit
git push -u origin feature # 6. Push
# ... create pull request (next lesson) ...
```

## 🎉 Lesson Complete!

You've learned:
✅ What branches are and why they're essential
✅ How to create and switch between branches
✅ Multi-site configuration management with branches
✅ Feature branch workflow pattern
✅ Professional branch naming conventions

### Next Steps

**Ready for Lesson 2?** → [Merging and Conflicts](02-merging-conflicts.md)

Learn how to:
- Merge site branches back to main
- Resolve merge conflicts
- Choose the right merge strategy
- Maintain clean history

**Or practice more:**
- Create branches for more sites
- Experiment with different naming conventions
- Practice the feature branch workflow
- Try pushing and pulling branches

---

**Lesson Duration:** 30 minutes
**Difficulty:** Intermediate
**Next:** Merging and conflict resolution
