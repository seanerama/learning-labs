# Lesson 2: Merging and Conflict Resolution

Learn to combine changes from different branches and confidently resolve merge conflicts.

## 🎯 Objectives

By the end of this lesson, you'll be able to:
- Merge branches successfully
- Understand different merge strategies
- Identify and resolve merge conflicts
- Choose between merging and rebasing
- Maintain clean commit history

## 📝 What You'll Learn

- How Git merging works
- Fast-forward vs. three-way merges
- Identifying and resolving conflicts
- Merge conflict resolution strategies
- When to use merge vs. rebase

## 🔀 Part 1: Understanding Merges

### What is Merging?

**Merging** combines changes from one branch into another. It's how you bring tested changes back into production.

**Network Engineering Analogy:**
```
Lab environment (feature branch)
    ↓ test and validate
    ↓ merge when ready
Production (main branch)
```

### Merge Scenarios

**Scenario 1: Tested Feature Ready for Production**
```bash
git checkout main
git merge feature/port-security
# Port security config now in main
```

**Scenario 2: Site Config Ready to Deploy**
```bash
git checkout main
git merge site-chicago
# Chicago config approved and merged
```

**Scenario 3: Multiple Sites Merging**
```bash
git merge site-chicago    # OK
git merge site-newyork    # Might conflict if both changed same lines
```

## 🚀 Part 2: Basic Merging

### Setup: Create Sample Branches

Let's create a scenario to practice:

```bash
cd ~/network-configs
git checkout main

# Ensure clean state
git status
```

### Fast-Forward Merge (Simplest Case)

A **fast-forward merge** happens when the target branch hasn't changed since the feature branch was created.

```bash
# Create and switch to new branch
git checkout -b add-ntp-config

# Add NTP configuration
cat >> SW-ACCESS-01.cfg << 'EOF'
!
ntp server 10.1.1.1 prefer
ntp server 10.1.1.2
ntp update-calendar
!
EOF

# Commit the change
git add SW-ACCESS-01.cfg
git commit -m "Add NTP servers for time synchronization"

# View the history
git log --oneline --graph
```

**Output:**
```
* d4e5f6g (HEAD -> add-ntp-config) Add NTP servers for time synchronization
* c3d4e5f (main) Previous commit
```

```bash
# Now merge into main
git checkout main
git merge add-ntp-config
```

**Output:**
```
Updating c3d4e5f..d4e5f6g
Fast-forward
 SW-ACCESS-01.cfg | 5 +++++
 1 file changed, 5 insertions(+)
```

**What happened?**
- Git simply moved main forward to point to add-ntp-config
- No new commit created
- Linear history maintained

```bash
# Verify
git log --oneline --graph
# * d4e5f6g (HEAD -> main, add-ntp-config) Add NTP servers
# * c3d4e5f Previous commit
```

### Three-Way Merge

A **three-way merge** happens when both branches have new commits.

```bash
# Create first feature
git checkout -b add-snmp
echo "snmp-server community NetworkOps RO" >> SW-ACCESS-01.cfg
git add SW-ACCESS-01.cfg
git commit -m "Add SNMP monitoring"

# Go back to main and create different change
git checkout main
git checkout -b add-logging
echo "logging host 10.2.2.10" >> SW-ACCESS-01.cfg
git add SW-ACCESS-01.cfg
git commit -m "Add syslog server"

# Merge first feature
git checkout main
git merge add-snmp
# Fast-forward (we're first)

# Merge second feature
git merge add-logging
```

**Output:**
```
Merge made by the 'recursive' strategy.
 SW-ACCESS-01.cfg | 1 +
 1 file changed, 1 insertion(+)
```

**What happened?**
- Git created a **merge commit** combining both changes
- Both features now in main
- History shows both branches

```bash
git log --oneline --graph --all
```

**Output:**
```
*   a1b2c3d (HEAD -> main) Merge branch 'add-logging'
|\
| * d4e5f6g (add-logging) Add syslog server
* | c3d4e5f (add-snmp) Add SNMP monitoring
|/
* b2c3d4e Previous commit
```

## ⚠️ Part 3: Merge Conflicts

### What is a Merge Conflict?

A **merge conflict** occurs when:
- Both branches modified the **same lines** in the same file
- Git doesn't know which version to keep
- **You must decide** manually

### Common Conflict Scenarios

**Scenario 1: Different hostname in each site branch**
```bash
# Branch 1 changes line 5: hostname SW-CHI-ACCESS-01
# Branch 2 changes line 5: hostname SW-NYC-ACCESS-01
# Git can't automatically choose
```

**Scenario 2: Different VLAN configurations**
```bash
# Branch 1: vlan 30 name GUEST
# Branch 2: vlan 30 name IOT
# Same VLAN number, different purpose
```

### Creating a Conflict (Practice)

Let's intentionally create a conflict to learn how to fix it:

```bash
cd ~/network-configs
git checkout main

# Create Chicago branch
git checkout -b site-chicago-v2
```

```bash
# Create Chicago-specific config
cat > SW-ACCESS-01.cfg << 'EOF'
hostname SW-CHI-ACCESS-01
!
vlan 10
 name DATA
vlan 30
 name IOT-DEVICES
!
interface GigabitEthernet0/1
 description UPLINK-CHICAGO
!
EOF

git add SW-ACCESS-01.cfg
git commit -m "Configure for Chicago site"
```

```bash
# Go back to main
git checkout main

# Create New York branch from main
git checkout -b site-newyork-v2
```

```bash
# Create NY-specific config (SAME FILE, DIFFERENT CONTENT)
cat > SW-ACCESS-01.cfg << 'EOF'
hostname SW-NYC-ACCESS-01
!
vlan 10
 name DATA
vlan 30
 name GUEST-WIFI
!
interface GigabitEthernet0/1
 description UPLINK-NEWYORK
!
EOF

git add SW-ACCESS-01.cfg
git commit -m "Configure for New York site"
```

### Trigger the Conflict

```bash
# Merge Chicago first (will work)
git checkout main
git merge site-chicago-v2
# Output: Fast-forward (no problem)

# Now try to merge New York (CONFLICT!)
git merge site-newyork-v2
```

**Output:**
```
Auto-merging SW-ACCESS-01.cfg
CONFLICT (content): Merge conflict in SW-ACCESS-01.cfg
Automatic merge failed; fix conflicts and then commit the result.
```

**🎉 Congratulations!** You created your first merge conflict!

## 🔧 Part 4: Resolving Conflicts

### Identify the Conflict

```bash
# Check status
git status
```

**Output:**
```
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both modified:   SW-ACCESS-01.cfg

no changes added to commit (use "git add" and/or "git commit -a")
```

### View the Conflicted File

```bash
cat SW-ACCESS-01.cfg
```

**Output:**
```
<<<<<<< HEAD
hostname SW-CHI-ACCESS-01
!
vlan 10
 name DATA
vlan 30
 name IOT-DEVICES
!
interface GigabitEthernet0/1
 description UPLINK-CHICAGO
=======
hostname SW-NYC-ACCESS-01
!
vlan 10
 name DATA
vlan 30
 name GUEST-WIFI
!
interface GigabitEthernet0/1
 description UPLINK-NEWYORK
>>>>>>> site-newyork-v2
!
```

### Understanding Conflict Markers

```
<<<<<<< HEAD
  [Content from current branch (main, which has Chicago merged)]
=======
  [Content from branch being merged (site-newyork-v2)]
>>>>>>> site-newyork-v2
```

**Breaking it down:**
- `<<<<<<< HEAD` - Start of current branch's version
- `=======` - Separator between versions
- `>>>>>>> branch-name` - End of incoming branch's version

### Resolution Strategy 1: Choose One Side

**Option A: Keep Chicago (current branch)**
```bash
# Edit file, remove conflict markers and NY content
cat > SW-ACCESS-01.cfg << 'EOF'
hostname SW-CHI-ACCESS-01
!
vlan 10
 name DATA
vlan 30
 name IOT-DEVICES
!
interface GigabitEthernet0/1
 description UPLINK-CHICAGO
!
EOF

# Mark as resolved
git add SW-ACCESS-01.cfg

# Complete the merge
git commit -m "Merge site-newyork-v2: kept Chicago config"
```

**Option B: Keep New York (incoming branch)**
```bash
# Edit file, remove conflict markers and Chicago content
cat > SW-ACCESS-01.cfg << 'EOF'
hostname SW-NYC-ACCESS-01
!
vlan 10
 name DATA
vlan 30
 name GUEST-WIFI
!
interface GigabitEthernet0/1
 description UPLINK-NEWYORK
!
EOF

git add SW-ACCESS-01.cfg
git commit -m "Merge site-newyork-v2: chose NY config"
```

### Resolution Strategy 2: Combine Both

Sometimes you want parts from each:

```bash
# Keep both sites in separate files
cat > SW-CHI-ACCESS-01.cfg << 'EOF'
hostname SW-CHI-ACCESS-01
!
vlan 10
 name DATA
vlan 30
 name IOT-DEVICES
!
interface GigabitEthernet0/1
 description UPLINK-CHICAGO
!
EOF

cat > SW-NYC-ACCESS-01.cfg << 'EOF'
hostname SW-NYC-ACCESS-01
!
vlan 10
 name DATA
vlan 30
 name GUEST-WIFI
!
interface GigabitEthernet0/1
 description UPLINK-NEWYORK
!
EOF

# Remove original conflicted file
rm SW-ACCESS-01.cfg

# Stage the resolution
git add SW-CHI-ACCESS-01.cfg SW-NYC-ACCESS-01.cfg
git rm SW-ACCESS-01.cfg

# Complete merge
git commit -m "Merge site-newyork-v2: split into separate site files"
```

### Resolution Strategy 3: Abort the Merge

If you're not ready to resolve:

```bash
# Abort and go back to before merge
git merge --abort

# Everything returns to pre-merge state
git status
# Output: On branch main, nothing to commit
```

## 🛠️ Part 5: Advanced Conflict Resolution

### Using merge tools

Git supports visual merge tools:

```bash
# Configure a merge tool (one-time setup)
git config --global merge.tool vimdiff
# Or: meld, kdiff3, p4merge, etc.

# When conflict occurs
git mergetool
```

This opens a visual editor showing:
- Left: Your version (HEAD)
- Right: Their version (incoming branch)
- Center: Result (edit this)

### Check for Conflicts Before Merging

```bash
# See what would happen without actually merging
git merge --no-commit --no-ff branch-name

# If conflicts:
git merge --abort

# If no conflicts:
git merge --abort  # Still abort to do it properly later
```

### View Conflicts

```bash
# List conflicted files
git diff --name-only --diff-filter=U

# See detailed conflict diff
git diff

# See changes from both sides
git log --merge
```

## 🔄 Part 6: Merge vs. Rebase

### Merging (What We've Done)

Creates a merge commit preserving both branches:

```
main:       A---B---C---D---E
                     \     /
feature:              F---G
```

**Result after merge:**
```bash
git checkout main
git merge feature
```

```
main:       A---B---C---D---E---M  (M = merge commit)
                     \         /
feature:              F-------G
```

### Rebasing (Alternative)

Replays commits on top of target branch:

```bash
git checkout feature
git rebase main
```

**Result after rebase:**
```
main:       A---B---C---D---E
                             \
feature:                      F'---G'  (F' and G' are new commits)
```

### When to Use Each

**Use MERGE when:**
- ✅ Working on public/shared branches
- ✅ Want to preserve complete history
- ✅ Merging long-lived branches (e.g., site branches)
- ✅ Want to see when features were integrated

**Use REBASE when:**
- ✅ Cleaning up local commits before pushing
- ✅ Want linear history
- ✅ Updating feature branch with latest main
- ✅ Commits only exist locally (never pushed)

**⚠️ NEVER rebase commits that have been pushed!** This rewrites history and confuses collaborators.

### Example: Rebase Workflow

```bash
# You're working on a feature
git checkout feature-branch

# Main has advanced
git fetch origin

# Rebase your work on top of latest main
git rebase origin/main

# If conflicts, resolve them
# Edit conflicted files
git add .
git rebase --continue

# Or abort if needed
git rebase --abort
```

## 🧪 Practice Exercises

### Exercise 1: Simple Merge

```bash
cd ~/network-configs
git checkout main

# Create feature
git checkout -b add-acl
cat >> SW-ACCESS-01.cfg << 'EOF'
!
ip access-list extended RESTRICT-MGMT
 permit tcp 10.1.1.0 0.0.0.255 any eq 22
 deny   ip any any log
!
EOF
git add SW-ACCESS-01.cfg
git commit -m "Add management ACL"

# Merge it
git checkout main
git merge add-acl

# Verify
git log --oneline
```

### Exercise 2: Create and Resolve Conflict

```bash
# Create conflicting branches
git checkout main
git checkout -b vlan-plan-a
echo "vlan 50\n name SERVERS" >> vlans.txt
git add vlans.txt
git commit -m "Plan A: VLAN 50 for servers"

git checkout main
git checkout -b vlan-plan-b
echo "vlan 50\n name STORAGE" >> vlans.txt
git add vlans.txt
git commit -m "Plan B: VLAN 50 for storage"

# Merge first (OK)
git checkout main
git merge vlan-plan-a

# Merge second (CONFLICT!)
git merge vlan-plan-b

# Resolve by choosing storage
cat > vlans.txt << 'EOF'
vlan 50
 name STORAGE
EOF

git add vlans.txt
git commit -m "Resolved: chose storage for VLAN 50"
```

### Exercise 3: Multi-Site Merge

```bash
# From Lesson 1, merge all sites into main
git checkout main

# Merge each site
git merge site-chicago
git merge site-newyork
git merge site-dallas

# View the result
git log --oneline --graph --all
```

### Exercise 4: Abort and Retry

```bash
# Start a merge
git checkout main
git merge some-branch

# Conflict occurs
git status

# Not ready to resolve
git merge --abort

# Clean state restored
git status

# Try again later...
```

## 📊 Commands Reference

```bash
# Merging
git merge branch-name                    # Merge branch into current
git merge --no-ff branch-name           # Force merge commit (no fast-forward)
git merge --squash branch-name          # Combine all commits into one

# Conflict handling
git status                              # See conflicted files
git diff                                # View conflicts
git diff --name-only --diff-filter=U    # List conflicted files
git add file                            # Mark conflict as resolved
git merge --abort                       # Cancel merge
git merge --continue                    # Continue after resolving

# Rebasing
git rebase branch-name                  # Rebase current onto branch
git rebase --continue                   # Continue after resolving conflicts
git rebase --abort                      # Cancel rebase
git rebase -i HEAD~3                    # Interactive rebase last 3 commits

# Viewing
git log --merge                         # View commits causing conflicts
git log --oneline --graph --all         # Visual branch history
git show branch-name                    # View branch's latest commit
```

## ✅ Verification Checklist

Make sure you can:

- [ ] Perform a fast-forward merge
- [ ] Perform a three-way merge
- [ ] Identify when a conflict occurs
- [ ] Understand conflict markers
- [ ] Resolve a merge conflict manually
- [ ] Abort a merge if needed
- [ ] Choose between merge and rebase
- [ ] Complete a merge commit

## ❓ Common Issues

### Issue: "Already up to date"

**Cause:** Branch you're merging has no new commits
```bash
git log --oneline branch-name
# If all commits already in current branch, nothing to merge
```

### Issue: Accidentally committed with conflict markers

**Cause:** Forgot to remove `<<<<<<<`, `=======`, `>>>>>>>` markers
```bash
# Search for conflict markers
grep -r "<<<<<<< HEAD" .

# Fix the file
nano file-with-markers

# Amend the commit
git add file
git commit --amend
```

### Issue: Lost track during conflict resolution

**Cause:** Multiple conflicts, confusion
```bash
# Start over
git merge --abort

# Try merge tool instead
git merge branch-name
git mergetool
```

### Issue: Merge created unwanted results

**Cause:** Made mistake during resolution
```bash
# Undo the merge
git reset --hard HEAD~1

# Try again
git merge branch-name
```

## 🎯 Best Practices

### Before Merging

✅ **DO:**
- Pull latest changes: `git pull`
- Review what you're merging: `git log branch-name`
- Check for conflicts ahead: `git merge --no-commit --no-ff`
- Ensure tests pass on feature branch

### During Conflict Resolution

✅ **DO:**
- Read conflict markers carefully
- Test the resolved code
- Ask teammate if unsure which version to keep
- Remove ALL conflict markers before committing

❌ **DON'T:**
- Panic! Conflicts are normal
- Delete code without understanding what it does
- Forget to test after resolving

### After Merging

✅ **DO:**
- Delete merged feature branches: `git branch -d feature-name`
- Test the result thoroughly
- Push to remote: `git push`
- Document significant merges in commit message

## 🎉 Lesson Complete!

You've learned:
✅ How to merge branches successfully
✅ Understanding fast-forward vs. three-way merges
✅ Identifying and resolving merge conflicts
✅ Different conflict resolution strategies
✅ When to use merge vs. rebase

### Next Steps

**Ready for Lesson 3?** → [Pull Requests and Code Review](03-pull-requests.md)

Learn how to:
- Create pull requests on GitHub/GitLab
- Review team members' code
- Use PR comments and discussions
- Merge pull requests properly

**Or practice more:**
- Create intentional conflicts
- Practice different resolution strategies
- Try using a visual merge tool
- Experiment with rebase

---

**Lesson Duration:** 40 minutes
**Difficulty:** Intermediate
**Next:** Pull requests and code review
