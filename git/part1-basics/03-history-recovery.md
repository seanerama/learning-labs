# Lesson 3: History Navigation and Recovery

Master Git's time machine - view history, compare changes, and recover from mistakes!

## 🎯 Objectives

By the end of this lesson, you'll be able to:
- Navigate commit history effectively
- Compare configurations across time
- Find when specific changes were made
- Restore previous file versions
- Recover from common mistakes
- Use Git as a configuration audit trail

## 📝 What You'll Learn

- Advanced git log options
- Using git diff to compare versions
- Checking out old commits
- Restoring files
- Finding bugs with git bisect
- Undoing changes safely

## 🚀 Part 1: Exploring History

### Setup: Create Sample History

Let's create a meaningful history to explore:

```bash
cd ~/network-configs

# Make several changes to simulate real work
echo "logging buffered 51200" >> SW-ACCESS-01.cfg
git add SW-ACCESS-01.cfg
git commit -m "Increase logging buffer size"

echo "snmp-server community NetworkOps RO" >> SW-ACCESS-01.cfg
git add SW-ACCESS-01.cfg
git commit -m "Add SNMP community string for monitoring"

echo "ntp server 10.1.1.1 prefer" >> SW-ACCESS-01.cfg
git add SW-ACCESS-01.cfg
git commit -m "Configure NTP server"
```

### Basic Log Viewing

```bash
# Standard log (most detailed)
git log
```

Output shows full details:
```
commit d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3 (HEAD -> main)
Author: Your Name <your.email@example.com>
Date:   Mon Jan 15 11:30:00 2024 -0500

    Configure NTP server

commit c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2
Author: Your Name <your.email@example.com>
Date:   Mon Jan 15 11:25:00 2024 -0500

    Add SNMP community string for monitoring
...
```

### Compact History Views

```bash
# One line per commit
git log --oneline
```

Output:
```
d4e5f6g (HEAD -> main) Configure NTP server
c3d4e5f Add SNMP community string for monitoring
b2c3d4e Increase logging buffer size
a1b2c3d Add port security to access ports
...
```

```bash
# Show last 3 commits
git log --oneline -n 3

# Show commits with stats
git log --stat

# Show commits with actual changes
git log -p
```

### Visual History

```bash
# Pretty format with graph
git log --oneline --graph --all --decorate
```

Output:
```
* d4e5f6g (HEAD -> main, origin/main) Configure NTP server
* c3d4e5f Add SNMP community string for monitoring
* b2c3d4e Increase logging buffer size
* a1b2c3d Add port security to access ports
```

### Filtered History

```bash
# Commits by author
git log --author="Your Name"

# Commits in last 2 days
git log --since="2 days ago"

# Commits before specific date
git log --until="2024-01-15"

# Commits that changed specific file
git log -- SW-ACCESS-01.cfg

# Search commit messages
git log --grep="VLAN"

# Commits that added or removed specific text
git log -S "port-security"
```

## 🔍 Part 2: Comparing Changes

### Comparing Working Directory

```bash
# Make a test change
echo "# Test change" >> SW-ACCESS-01.cfg

# See what changed (not yet staged)
git diff
```

Output:
```diff
diff --git a/SW-ACCESS-01.cfg b/SW-ACCESS-01.cfg
index c3d4e5f..d4e5f6g 100644
--- a/SW-ACCESS-01.cfg
+++ b/SW-ACCESS-01.cfg
@@ -25,3 +25,4 @@ line vty 0 4
  transport input ssh
 !
 ntp server 10.1.1.1 prefer
+# Test change
```

**Understanding the diff:**
- `---` = old version
- `+++` = new version
- `@@` = line numbers
- Lines with `+` = added
- Lines with `-` = removed

### Comparing Staged Changes

```bash
# Stage the change
git add SW-ACCESS-01.cfg

# Compare staged changes to last commit
git diff --staged
```

### Comparing Commits

```bash
# Compare two commits
git diff a1b2c3d c3d4e5f

# Compare current to specific commit
git diff c3d4e5f

# Compare specific file between commits
git diff a1b2c3d c3d4e5f -- SW-ACCESS-01.cfg

# Show what changed in a commit
git show c3d4e5f
```

### Comparing Branches

```bash
# Compare current branch to main
git diff main

# Compare two branches
git diff main..feature-branch

# Show only changed files
git diff --name-only main
```

## ⏪ Part 3: Viewing Old Versions

### Viewing File at Specific Commit

```bash
# View file as it was in specific commit
git show c3d4e5f:SW-ACCESS-01.cfg

# Save old version to new file for comparison
git show c3d4e5f:SW-ACCESS-01.cfg > SW-ACCESS-01.cfg.old

# Compare with current
diff SW-ACCESS-01.cfg SW-ACCESS-01.cfg.old

# Clean up
rm SW-ACCESS-01.cfg.old
```

### Checking Out Old Commits (Read-Only)

**⚠️ Warning:** This puts you in "detached HEAD" state - you're viewing history, not making changes.

```bash
# View repository as it was in past
git checkout c3d4e5f

# You'll see warning:
# You are in 'detached HEAD' state...

# Look around
ls -la
cat SW-ACCESS-01.cfg

# Return to present
git checkout main
```

**What just happened?**
- Git "time traveled" to that commit
- All files show how they were then
- You can look but shouldn't make changes
- `git checkout main` brings you back

### Viewing Specific File from Past

```bash
# Checkout just one file from old commit (overwrites current!)
git checkout c3d4e5f -- SW-ACCESS-01.cfg

# This CHANGES your working directory!
# File now matches that commit

# See it's modified
git status

# If you want to keep it, commit:
git commit -m "Restore SW-ACCESS-01 config from c3d4e5f"

# If you don't want it, restore current version:
git restore SW-ACCESS-01.cfg
```

## 🔧 Part 4: Recovering from Mistakes

### Scenario 1: Undo Working Directory Changes

**Problem:** You modified a file but haven't staged it yet, and want to undo.

```bash
# Make a bad change
echo "BAD CONFIG LINE" >> SW-ACCESS-01.cfg

# Oh no! Undo it
git restore SW-ACCESS-01.cfg

# File is back to last committed version
```

### Scenario 2: Unstage Files

**Problem:** You accidentally staged the wrong file.

```bash
# Stage wrong file
git add SW-ACCESS-02.cfg

# Check status
git status

# Unstage it
git restore --staged SW-ACCESS-02.cfg

# Now it's unstaged (but changes still in file)
git status
```

### Scenario 3: Amend Last Commit

**Problem:** You forgot to include a file in your last commit.

```bash
# You committed but forgot a file
git commit -m "Update switch configs"

# Oh no! Forgot to add SW-ACCESS-02.cfg
git add SW-ACCESS-02.cfg

# Amend the previous commit
git commit --amend --no-edit

# --no-edit keeps same commit message
# --amend adds new changes to previous commit
```

**Change commit message too:**

```bash
git commit --amend -m "Update switch configs with security settings"
```

**⚠️ Warning:** Only amend commits that haven't been pushed!

### Scenario 4: Revert a Commit

**Problem:** A commit introduced a bug. You want to undo it safely.

```bash
# View history
git log --oneline

# Revert specific commit (creates new commit that undoes it)
git revert c3d4e5f

# Git opens editor for commit message
# Save and close

# New commit created that undoes the changes
git log --oneline
```

**What happened?**
- Old commit stays in history
- New commit created that reverses the changes
- Safe for shared repositories

### Scenario 5: Reset to Previous Commit

**⚠️ Danger:** This rewrites history - only use on unpushed commits!

```bash
# View commits
git log --oneline

# Soft reset: Undo commit but keep changes
git reset --soft HEAD~1

# Changes are now staged, ready to recommit
git status

# Mixed reset (default): Undo commit and unstage
git reset HEAD~1

# Changes in working directory, not staged
git status

# Hard reset: Undo commit and discard changes
git reset --hard HEAD~1

# ⚠️ Changes are GONE forever!
```

**Understanding HEAD~1:**
- `HEAD` = current commit
- `HEAD~1` = one commit before HEAD
- `HEAD~2` = two commits before
- Or use commit hash: `git reset --hard a1b2c3d`

### Scenario 6: Recover "Lost" Commits

**Problem:** You did `git reset --hard` and want those commits back!

```bash
# View all actions (even "deleted" commits)
git reflog

# Output shows all HEAD movements:
# d4e5f6g HEAD@{0}: reset: moving to HEAD~1
# e5f6g7h HEAD@{1}: commit: Configure NTP server
# c3d4e5f HEAD@{2}: commit: Add SNMP

# Recover lost commit
git checkout e5f6g7h

# Or create branch from it
git checkout -b recovered-commit e5f6g7h

# Or reset back to it
git reset --hard e5f6g7h
```

**Pro tip:** Git keeps commits for ~30 days even after "deleting" them!

## 🔎 Part 5: Finding Bugs in History

### Using git blame

Find who changed each line and when:

```bash
# See who last modified each line
git blame SW-ACCESS-01.cfg
```

Output:
```
a1b2c3d (Your Name 2024-01-15 10:25:00 -0500  1) hostname SW-ACCESS-01
a1b2c3d (Your Name 2024-01-15 10:25:00 -0500  2) !
a1b2c3d (Your Name 2024-01-15 10:25:00 -0500  3) vlan 10
b2c3d4e (Your Name 2024-01-15 10:30:00 -0500  4)  name DATA
c3d4e5f (Jane Doe  2024-01-15 11:00:00 -0500  5) vlan 30
```

```bash
# Show specific line range
git blame -L 10,20 SW-ACCESS-01.cfg

# Ignore whitespace changes
git blame -w SW-ACCESS-01.cfg
```

### Using git bisect (Finding Bugs)

**Scenario:** Config worked 10 commits ago, broken now. Find the breaking commit!

```bash
# Start bisecting
git bisect start

# Mark current as bad
git bisect bad

# Mark old known-good commit
git bisect good a1b2c3d

# Git checks out middle commit
# Test if config works...

# If it works:
git bisect good

# If it doesn't:
git bisect bad

# Repeat until Git finds the exact breaking commit
# Git will tell you: "abc123 is the first bad commit"

# Finish bisecting
git bisect reset
```

## 🧪 Practice Exercises

### Exercise 1: Configuration Archaeology

Find when a specific setting was added:

```bash
# Search for when SNMP was added
git log -S "snmp-server" --oneline

# View that commit's changes
git show <commit-hash>

# See who added it
git blame SW-ACCESS-01.cfg | grep snmp
```

### Exercise 2: Compare Configurations

Compare your switch config from 5 commits ago to now:

```bash
# Find commit from 5 commits ago
git log --oneline | head -n 6

# Compare to now
git diff HEAD~5 SW-ACCESS-01.cfg

# Save both versions to files
git show HEAD~5:SW-ACCESS-01.cfg > old-config.txt
cp SW-ACCESS-01.cfg new-config.txt

# Use your favorite diff tool
diff -u old-config.txt new-config.txt
```

### Exercise 3: Recover from Mistake

Simulate accidentally deleting important config:

```bash
# Accidentally delete file
rm SW-ACCESS-01.cfg

# Oh no!
ls -la

# Restore it
git restore SW-ACCESS-01.cfg

# It's back!
ls -la
cat SW-ACCESS-01.cfg
```

### Exercise 4: Audit Trail

Create an audit report of all changes:

```bash
# Generate change log
git log --oneline --since="1 week ago" > weekly-changes.txt

# Detailed report with diffs
git log -p --since="1 week ago" > detailed-changes.txt

# Summary by author
git shortlog --since="1 week ago" --numbered

# View the reports
cat weekly-changes.txt
```

## 📊 Commands Reference

```bash
# Viewing history
git log                              # Full history
git log --oneline                    # Compact view
git log --oneline --graph            # Visual graph
git log -n 5                         # Last 5 commits
git log --since="2 days ago"         # Time filtered
git log --author="Name"              # By author
git log -- file.txt                  # File history
git log -S "text"                    # Search changes
git log --grep="pattern"             # Search messages

# Comparing
git diff                             # Working vs staged
git diff --staged                    # Staged vs committed
git diff HEAD                        # Working vs last commit
git diff commit1 commit2             # Two commits
git diff branch1 branch2             # Two branches
git diff --stat                      # Summary only
git diff --name-only                 # Files only

# Viewing old versions
git show commit:file                 # View file at commit
git checkout commit                  # Go to commit (detached HEAD)
git checkout commit -- file          # Restore file from commit

# Undoing changes
git restore file                     # Discard working changes
git restore --staged file            # Unstage file
git commit --amend                   # Fix last commit
git revert commit                    # Undo commit (safe)
git reset --soft HEAD~1              # Undo commit, keep changes
git reset --hard HEAD~1              # Undo commit, discard changes

# Finding information
git blame file                       # Line-by-line history
git reflog                           # All HEAD movements
git bisect start/good/bad/reset      # Binary search for bugs
```

## ✅ Verification Checklist

Make sure you can:

- [ ] View commit history with `git log`
- [ ] Filter history by date, author, or file
- [ ] Compare configurations with `git diff`
- [ ] View old file versions
- [ ] Restore accidentally modified files
- [ ] Unstage files
- [ ] Amend commits
- [ ] Revert commits safely
- [ ] Use git blame to find changes
- [ ] Recover from git reset

## ❓ Common Issues

### Issue: "detached HEAD" warning

**This is OK!** You're viewing history. Return with:
```bash
git checkout main
```

### Issue: Can't find a commit

```bash
# Use reflog to find "lost" commits
git reflog

# Look for the commit you want
# Checkout or reset to it
git checkout <commit-hash>
```

### Issue: Accidentally committed to detached HEAD

**Solution:**
```bash
# Create branch from current position
git checkout -b recovered-work

# Now merge into main if you want to keep it
git checkout main
git merge recovered-work
```

### Issue: git reset went too far

```bash
# Find where you were
git reflog

# Reset to before the bad reset
git reset --hard HEAD@{1}
```

## 🎯 Best Practices

### Viewing History

✅ **DO:**
- Use `--oneline` for quick overview
- Use `-p` to see actual changes
- Filter by `--since` for recent work
- Use `--author` to see teammate's work

### Undoing Changes

✅ **SAFE (for shared repos):**
- `git revert` - creates new commit
- `git checkout -- file` - discards local changes
- `git commit --amend` - only before pushing

⚠️ **DANGEROUS (only for local commits):**
- `git reset --hard` - loses data
- `git push --force` - can break teammates' work

### Commit Message Search

Make commits findable:
```bash
# ✅ GOOD - searchable
git commit -m "Add VLAN 30 (GUEST) for visitor access - CHG0012345"

# Later find it:
git log --grep="CHG0012345"
git log --grep="VLAN 30"
```

## 🎉 Part 1 Complete!

You've mastered:

✅ Git fundamentals and workflow
✅ Remote repositories and backups
✅ History navigation and comparison
✅ Recovering from mistakes
✅ Finding changes and bugs

### Skills Gained

- Repository management
- Commit workflow mastery
- GitHub/GitLab usage
- History exploration
- Configuration recovery
- Audit trail generation

### What's Next?

**Ready for Part 2?** → [Part 2: Collaborative Development](../part2-collaboration/README.md)

Learn:
- Branching strategies for multi-site networks
- Merging and conflict resolution
- Pull request workflows
- Team collaboration patterns
- Advanced branching techniques

**Or practice more:**
- Try the exercises again
- Experiment with your own configs
- Set up automated backups
- Create audit reports

---

**Part 1 Duration:** 1.5 hours total
**Skills Level:** Beginner → Comfortable
**Next Challenge:** Team workflows and branching

Congratulations! You now have solid Git fundamentals. Part 2 will teach you how to collaborate with teams and manage complex projects!
