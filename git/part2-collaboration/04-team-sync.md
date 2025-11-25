# Lesson 4: Team Synchronization

Learn to keep your work in sync with teammates and handle concurrent changes safely.

## 🎯 Objectives

By the end of this lesson, you'll be able to:
- Keep your local repository in sync with remote
- Understand fetch vs. pull
- Handle concurrent changes from team members
- Update feature branches with latest main
- Resolve synchronization conflicts
- Use rebase vs. merge for updates

## 📝 What You'll Learn

- Fetching vs. pulling changes
- Keeping feature branches current
- Handling concurrent development
- Synchronization workflows
- Avoiding and resolving sync issues

## 🔄 Part 1: Understanding Synchronization

### The Synchronization Challenge

**Scenario:** Two engineers working simultaneously

```
Engineer A (You):
  main → create feature-A → work... work... work...

Engineer B (Teammate):
  main → create feature-B → work → merge to main ✓

Your main is now BEHIND!
```

**Without sync:**
```
Your PR: feature-A → main (old version)
  Result: Merge conflict or integration issues ❌
```

**With sync:**
```
Your PR: feature-A (updated with latest main) → main (current)
  Result: Clean merge ✓
```

### Real-World Examples

**Example 1: Network Standards Update**
```
You: Working on Chicago switch config
Teammate: Updates security baseline (merged to main)
You need: Latest security baseline in your Chicago config
```

**Example 2: Shared Infrastructure**
```
You: Adding VLANs to core switch
Teammate: Modified same switch for routing (merged)
You need: Their routing changes before adding VLANs
```

**Example 3: Breaking Changes**
```
You: Using old ACL syntax
Teammate: Refactored ACL format (merged)
You need: Update to new format before merging
```

## 📥 Part 2: Fetch vs. Pull

### Understanding Fetch

`git fetch` downloads changes without modifying your working directory.

```bash
# Fetch all branches from remote
git fetch origin
```

**What happens:**
```
Remote (origin):
  main: A---B---C---D---E

Local before fetch:
  main: A---B---C

Local after fetch:
  main: A---B---C
  origin/main: A---B---C---D---E  (remote-tracking branch updated)

Your working directory: UNCHANGED
```

**Benefits:**
- ✅ Safe - doesn't touch your code
- ✅ Review changes before applying
- ✅ See what teammates did

```bash
# View what was fetched
git fetch origin

# Compare local to remote
git log main..origin/main

# See what changed
git diff main origin/main
```

### Understanding Pull

`git pull` = `git fetch` + `git merge`

```bash
# Pull changes (fetch + merge)
git pull origin main
```

**What happens:**
```
Step 1 (fetch): Downloads changes from remote
Step 2 (merge): Merges origin/main into your current branch
```

**Equivalent to:**
```bash
git fetch origin
git merge origin/main
```

### Pull with Rebase

`git pull --rebase` = `git fetch` + `git rebase`

```bash
# Pull with rebase instead of merge
git pull --rebase origin main
```

**Difference:**

**Regular pull (merge):**
```
Local:  A---B---C---F---G (your commits)
Remote: A---B---C---D---E (their commits)
Result: A---B---C---D---E---M (merge commit)
                    \     /
                     F---G
```

**Pull --rebase:**
```
Local:  A---B---C---F---G (your commits)
Remote: A---B---C---D---E (their commits)
Result: A---B---C---D---E---F'---G' (your commits replayed)
```

## 🔧 Part 3: Basic Synchronization Workflow

### Daily Sync Routine

**Every morning before starting work:**

```bash
# 1. Go to main branch
git checkout main

# 2. Pull latest changes
git pull origin main

# 3. View what changed overnight
git log --oneline --since="1 day ago"

# 4. Now create feature branch from updated main
git checkout -b feature/todays-work
```

### Before Creating a Pull Request

```bash
# 1. Ensure main is current
git checkout main
git pull origin main

# 2. Update feature branch
git checkout feature/your-feature
git merge main
# or
git rebase main

# 3. Resolve any conflicts
# 4. Push updated branch
git push --force-with-lease origin feature/your-feature

# 5. Create PR
```

### After Your PR is Merged

```bash
# 1. Switch to main
git checkout main

# 2. Pull your merged changes
git pull origin main

# 3. Delete local feature branch
git branch -d feature/your-feature

# 4. Verify remote branch auto-deleted
git fetch --prune

# 5. Start next feature from updated main
git checkout -b feature/next-task
```

## 👥 Part 4: Handling Concurrent Development

### Scenario: Multiple Engineers, Same Repository

**Setup:**
- Engineer A (you): Working on Chicago site
- Engineer B: Working on New York site
- Engineer C: Updating security baseline

```bash
# Everyone starts from same point
git checkout main
git pull
```

### Scenario 1: No Conflicts (Different Files)

**Engineer B finishes first and merges:**

```bash
# Engineer B
git checkout site-newyork
# ... makes changes to SW-NYC-ACCESS-01.cfg ...
git push origin site-newyork
# Creates PR, gets approved, merges
```

**You (Engineer A) synchronize:**

```bash
# You're still working on site-chicago
git status
# On branch site-chicago
# Changes to SW-CHI-ACCESS-01.cfg

# Fetch to see what changed
git fetch origin

# View what was merged
git log main..origin/main --oneline
# Output: a1b2c3d Merge branch 'site-newyork'

# Update your main
git checkout main
git pull origin main

# Update your feature branch (different files = no conflict)
git checkout site-chicago
git merge main

# Output: Auto-merging... no conflicts!
```

### Scenario 2: Potential Conflicts (Same File)

**Engineer C updates security baseline (affects all sites):**

```bash
# Engineer C modifies SW-ACCESS-01.cfg (template)
# Adds new security ACL
# Merges to main
```

**You need to incorporate their changes:**

```bash
# Fetch the changes
git fetch origin

# Update main
git checkout main
git pull origin main

# Try to merge into your branch
git checkout site-chicago
git merge main
```

**If conflict:**
```
Auto-merging SW-CHI-ACCESS-01.cfg
CONFLICT (content): Merge conflict in SW-CHI-ACCESS-01.cfg
Automatic merge failed; fix conflicts and then commit the result.
```

**Resolve:**
```bash
# Edit SW-CHI-ACCESS-01.cfg
nano SW-CHI-ACCESS-01.cfg

# Remove conflict markers
# Keep security baseline + your site-specific changes

# Stage resolution
git add SW-CHI-ACCESS-01.cfg

# Complete merge
git commit -m "Merge main: incorporate updated security baseline"

# Push updated branch
git push origin site-chicago
```

### Scenario 3: PR Has Conflicts

**Your PR shows "This branch has conflicts":**

```bash
# Someone merged changes that conflict with yours
# Update your feature branch

# Fetch latest
git fetch origin

# Update main
git checkout main
git pull origin main

# Go back to feature branch
git checkout feature/your-feature

# Merge main (or rebase)
git merge main
# Resolve conflicts if any

# Push updated branch
git push origin feature/your-feature

# PR automatically updates and conflicts resolved!
```

## 🔄 Part 5: Rebase Workflow for Clean History

### Why Rebase for Synchronization?

**Problem with merge:**
```
Your commits:    A---B---C---F---G
Main advances:   A---B---C---D---E
After merge:     A---B---C---D---E---M
                         \         /
                          F-------G

Result: Merge commit M clutters history
```

**Solution with rebase:**
```
Your commits:    A---B---C---F---G
Main advances:   A---B---C---D---E
After rebase:    A---B---C---D---E---F'---G'

Result: Linear history, no merge commit
```

### Rebase Workflow

```bash
# Start feature from main
git checkout main
git pull origin main
git checkout -b feature/add-qos

# ... work, work, work ...
# ... meanwhile, main advances ...

# Update feature branch with latest main
git fetch origin

# Rebase your commits onto updated main
git rebase origin/main
```

**If conflicts during rebase:**
```bash
# Git stops at conflicted commit
# Output: Conflict in file.cfg

# Resolve conflict
nano file.cfg

# Stage resolution
git add file.cfg

# Continue rebase
git rebase --continue

# Repeat for each conflict
# When done, all commits replayed
```

**Push rebased branch:**
```bash
# Use --force-with-lease (safe force push)
git push --force-with-lease origin feature/add-qos
```

**⚠️ Warning:** Only rebase branches that:
- Haven't been reviewed yet
- Only you are working on
- Haven't been merged

**Never rebase:**
- main or other shared branches
- Branches others are working on
- Commits already in PR being reviewed

## 📊 Part 6: Advanced Synchronization

### Keeping Long-Lived Feature Branch Updated

**Pattern for features taking days/weeks:**

```bash
# Daily: Sync with main
git checkout main
git pull origin main

git checkout feature/long-running
git rebase main  # or git merge main

# Resolve any conflicts
# Continue working
```

**Why this matters:**
- Prevents massive conflicts at the end
- Ensures compatibility with latest code
- Makes final PR review easier

### Working with Remote Branches

```bash
# List all remote branches
git branch -r

# Checkout someone else's branch to test
git fetch origin
git checkout -b test-their-feature origin/feature/their-branch

# Test it...

# Go back to your work
git checkout your-feature-branch
```

### Cleaning Up

```bash
# Remove local branches that were deleted remotely
git fetch --prune

# List branches merged to main (candidates for deletion)
git branch --merged main

# Delete multiple local branches
git branch -d branch1 branch2 branch3

# Delete remote branch
git push origin --delete old-feature-branch
```

### Synchronizing After Force Push

**If teammate force-pushed (rare, but happens):**

```bash
# Fetch all changes
git fetch origin

# Reset your local branch to match remote
git checkout problematic-branch
git reset --hard origin/problematic-branch

# ⚠️ Warning: This discards local changes!
```

## 🧪 Practice Exercises

### Exercise 1: Simulate Team Development

Open two terminal windows to simulate two engineers:

**Terminal 1 (Engineer A - You):**
```bash
cd ~/network-configs
git checkout main
git checkout -b feature/engineer-a
echo "Change A" >> fileA.txt
git add fileA.txt
git commit -m "Engineer A's work"
# Don't push yet
```

**Terminal 2 (Engineer B - Teammate):**
```bash
cd ~/network-configs
git checkout main
git checkout -b feature/engineer-b
echo "Change B" >> fileB.txt
git add fileB.txt
git commit -m "Engineer B's work"
git push origin feature/engineer-b
# Create and merge PR via GitHub/GitLab
```

**Terminal 1 (Engineer A - Sync):**
```bash
# Engineer B merged while you were working
git fetch origin
git checkout main
git pull origin main

# Update your feature branch
git checkout feature/engineer-a
git rebase main

# Push
git push origin feature/engineer-a
```

### Exercise 2: Update Feature Branch

```bash
# Create feature branch
git checkout main
git checkout -b feature/my-work
echo "My changes" >> my-file.txt
git add my-file.txt
git commit -m "My work"

# Simulate teammate merging to main
git checkout main
echo "Teammate changes" >> their-file.txt
git add their-file.txt
git commit -m "Teammate work"

# Update feature branch
git checkout feature/my-work
git merge main

# View history
git log --oneline --graph --all
```

### Exercise 3: Fetch and Review Before Pull

```bash
# Fetch without pulling
git fetch origin

# Review what changed
git log main..origin/main --oneline

# See the actual changes
git diff main origin/main

# Decide if you want to pull
git pull origin main
```

### Exercise 4: Resolve Sync Conflict

```bash
# Create conflict scenario
git checkout main
echo "version 1" > conflict-file.txt
git add conflict-file.txt
git commit -m "Initial version"

# Branch A
git checkout -b branch-a
echo "version A" > conflict-file.txt
git add conflict-file.txt
git commit -m "Change to A"

# Branch B (from main, not branch-a)
git checkout main
git checkout -b branch-b
echo "version B" > conflict-file.txt
git add conflict-file.txt
git commit -m "Change to B"

# Merge B to main
git checkout main
git merge branch-b

# Try to merge main into A (conflict!)
git checkout branch-a
git merge main
# Resolve conflict, practice sync workflow
```

## 📊 Commands Reference

```bash
# Fetching
git fetch origin                      # Fetch from default remote
git fetch --all                       # Fetch from all remotes
git fetch --prune                     # Remove deleted remote branches

# Pulling
git pull                              # Fetch + merge
git pull origin main                  # Pull specific branch
git pull --rebase                     # Fetch + rebase instead of merge
git pull --rebase=interactive         # Interactive rebase

# Viewing remote state
git remote show origin                # Show remote details
git branch -r                         # List remote branches
git branch -a                         # List all branches (local + remote)
git log main..origin/main            # Commits in remote not in local

# Comparing
git diff main origin/main             # See differences
git diff --stat main origin/main      # Summary of differences

# Updating feature branches
git checkout feature-branch
git merge main                        # Merge main into feature
git rebase main                       # Rebase feature onto main
git push --force-with-lease          # Safe force push after rebase

# Cleaning
git fetch --prune                     # Remove stale remote-tracking branches
git branch --merged                   # List branches merged to current
git branch -d branch-name             # Delete local branch
git push origin --delete branch-name  # Delete remote branch

# Synchronization
git checkout main && git pull         # Update main
git rebase origin/main               # Rebase onto remote main
git reset --hard origin/main         # Reset to match remote (discard local)
```

## ✅ Verification Checklist

Make sure you can:

- [ ] Fetch changes without pulling
- [ ] Compare local vs. remote branches
- [ ] Pull updates to main branch
- [ ] Update feature branch with latest main
- [ ] Handle conflicts when synchronizing
- [ ] Use rebase to keep clean history
- [ ] Force push safely after rebase
- [ ] Clean up merged branches
- [ ] Review teammates' changes before merging

## ❓ Common Issues

### Issue: "Your branch is behind"

**Message:**
```
Your branch is behind 'origin/main' by 3 commits
```

**Solution:**
```bash
git pull origin main
```

### Issue: "Your branch and 'origin/main' have diverged"

**Message:**
```
Your branch and 'origin/main' have diverged,
and have 2 and 3 different commits each, respectively.
```

**Cause:** You have local commits AND remote has new commits

**Solution:**
```bash
# Option 1: Merge remote changes
git pull origin main

# Option 2: Rebase your commits
git pull --rebase origin main
```

### Issue: "Cannot pull with rebase: You have unstaged changes"

**Cause:** Uncommitted changes in working directory

**Solution:**
```bash
# Option 1: Commit changes
git add .
git commit -m "Save work"
git pull --rebase

# Option 2: Stash changes
git stash
git pull --rebase
git stash pop
```

### Issue: "! [rejected] (non-fast-forward)"

**Message:**
```
! [rejected]        feature-branch -> feature-branch (non-fast-forward)
```

**Cause:** Remote branch has commits you don't have

**Solution:**
```bash
# Fetch and rebase
git fetch origin
git rebase origin/feature-branch

# Or pull with rebase
git pull --rebase origin feature-branch
```

### Issue: "force push" after rebase

**Why needed:** Rebase rewrites history

**Safe way:**
```bash
# Use --force-with-lease (checks remote hasn't changed)
git push --force-with-lease origin feature-branch
```

**⚠️ Never:**
```bash
# DON'T use bare --force (unsafe)
git push --force origin feature-branch
```

## 🎯 Best Practices

### Daily Workflow

**Start of day:**
```bash
git checkout main
git pull origin main
git checkout -b feature/todays-task
```

**End of day:**
```bash
git add .
git commit -m "Progress on feature"
git push origin feature/todays-task
```

**Next morning:**
```bash
git checkout main
git pull origin main

git checkout feature/todays-task
git rebase main  # Start with latest changes
```

### Before Creating PR

```bash
# 1. Update main
git checkout main
git pull origin main

# 2. Update feature branch
git checkout feature/your-work
git rebase main

# 3. Force push if you rebased
git push --force-with-lease origin feature/your-work

# 4. Create PR
```

### Team Communication

✅ **DO:**
- Communicate before force pushing shared branches
- Pull before starting work each day
- Keep feature branches short-lived
- Merge/rebase frequently to avoid big conflicts

❌ **DON'T:**
- Force push to main or shared branches
- Work on same branch simultaneously without coordinating
- Let feature branches diverge for weeks
- Ignore fetch warnings

### Merge vs. Rebase for Sync

**Use merge when:**
- ✅ Updating public/shared branches
- ✅ Want to preserve complete history
- ✅ Working with others on same branch

**Use rebase when:**
- ✅ Updating your private feature branch
- ✅ Want clean, linear history
- ✅ Before creating PR
- ✅ Only you are working on the branch

## 🎉 Lesson Complete!

You've learned:
✅ Difference between fetch and pull
✅ How to keep local repository in sync
✅ Handling concurrent team development
✅ Updating feature branches safely
✅ Using rebase for clean history

## 🎓 Part 2 Complete!

You've mastered collaborative development:
✅ Branching strategies for multi-site networks
✅ Merging and conflict resolution
✅ Pull requests and code review
✅ Team synchronization

### What's Next?

**Ready for Part 3?** → [Part 3: Advanced Concepts](../part3-advanced/README.md)

Learn:
- Automated configuration backups with Python
- Interactive rebase for clean history
- Git hooks for validation
- Complete network change workflow

**Or practice more:**
- Work with a teammate on shared repository
- Practice daily sync routine
- Create and merge multiple PRs
- Experiment with rebase workflow

---

**Lesson Duration:** 20 minutes
**Difficulty:** Intermediate
**Part 2 Total Duration:** 2 hours
**Next:** Part 3 - Advanced automation and workflows
