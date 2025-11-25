# Part 2: Collaborative Development

Master team workflows and branching strategies for managing multi-site network infrastructure.

## 🎯 Learning Objectives

By the end of Part 2, you'll be able to:
- ✅ Create and manage branches for parallel development
- ✅ Merge branches and resolve conflicts
- ✅ Use pull requests for code review
- ✅ Manage multi-site configurations safely
- ✅ Synchronize work with team members
- ✅ Implement professional branching strategies

## 📚 Lessons

1. **[Branching Strategies](01-branching-strategies.md)** - Create branches for multi-site management
2. **[Merging and Conflicts](02-merging-conflicts.md)** - Merge site configs and resolve conflicts
3. **[Pull Requests and Review](03-pull-requests.md)** - Team code review workflow
4. **[Team Synchronization](04-team-sync.md)** - Keep work in sync with teammates

## ⏱️ Time Estimate

**Total:** 2 hours
- Branching Strategies: 30 minutes
- Merging and Conflicts: 40 minutes
- Pull Requests and Review: 30 minutes
- Team Synchronization: 20 minutes

## 🎓 What You'll Build

Throughout Part 2, you'll:
1. Manage configurations for multiple branch offices using branches
2. Test site-specific changes before merging to production
3. Practice resolving merge conflicts between site configs
4. Create pull requests for team review
5. Synchronize changes with teammates working on the same infrastructure

## 🚀 Prerequisites

**Required:**
- Completed Part 1: Single Developer Basics
- Active GitHub or GitLab account
- SSH access configured
- Existing `network-configs` repository

**Verify You're Ready:**
```bash
# You should have a repo from Part 1
cd ~/network-configs
git status

# You should have a remote configured
git remote -v

# You should be able to push
git push
```

If any of these fail, review Part 1 lessons.

## 📖 Learning Path

Follow the lessons in order:

```
01-branching-strategies.md
    ↓
02-merging-conflicts.md
    ↓
03-pull-requests.md
    ↓
04-team-sync.md
```

Each lesson builds on the previous one!

## 💡 Key Concepts Covered

### Branches
Independent lines of development allowing parallel work without interference.

### Merging
Combining changes from different branches back together.

### Merge Conflicts
When Git can't automatically combine changes and requires manual resolution.

### Pull Requests (PRs)
Formal request to merge changes, enabling code review and discussion.

### Rebase
Alternative to merging that maintains linear history.

### Fast-Forward Merge
When branch can be merged without creating merge commit.

## 🎯 Practice Scenario

You'll work through this real-world scenario:

**Setup:** You're part of a network team managing configurations for multiple branch offices (Chicago, New York, Dallas). Each site has unique requirements but shares common standards.

**Goals:**
- Test site-specific configs in branches
- Review each other's changes before deployment
- Merge approved changes to production
- Handle conflicts when sites have different requirements

**By the end of Part 2:**
- ✅ Multi-site branch structure established
- ✅ Merge conflicts resolved
- ✅ Pull request workflow implemented
- ✅ Team synchronization practiced

## ✅ Completion Checklist

Mark off as you complete each lesson:

- [ ] **Lesson 1:** Created branches for different sites
- [ ] **Lesson 2:** Merged branches and resolved conflicts
- [ ] **Lesson 3:** Created and merged a pull request
- [ ] **Lesson 4:** Synced work with team changes

## 🎓 Skills Gained

After Part 2, you'll know:

### Core Commands
- `git branch` - List and create branches
- `git checkout` / `git switch` - Change branches
- `git merge` - Combine branches
- `git rebase` - Reapply commits on different base
- `git fetch` - Download remote changes
- `git pull --rebase` - Fetch and rebase

### Workflows
- Feature branch workflow
- Pull request process
- Code review best practices
- Conflict resolution strategies
- Team synchronization

## 🆘 Common Issues

### "Already up to date" when merging
**Cause:** No changes to merge
**Solution:** This is OK - the branches are already in sync

### Merge conflicts
**Cause:** Same lines changed in both branches
**Solution:** Edit conflicted files, choose which changes to keep

### Detached HEAD after checkout
**Cause:** Checked out a commit instead of branch
**Solution:** `git checkout main` to return to a branch

### Can't push to branch
**Cause:** Remote has changes you don't have locally
**Solution:** `git pull` first, then `git push`

## 📊 Quick Reference

```bash
# Create branch
git branch feature-name
git checkout feature-name
# OR combined
git checkout -b feature-name

# List branches
git branch              # Local only
git branch -a           # Include remote

# Switch branches
git checkout main
git switch main         # Newer syntax

# Merge branch
git checkout main
git merge feature-name

# Delete branch
git branch -d feature-name       # Safe (only if merged)
git branch -D feature-name       # Force delete

# View remote branches
git remote show origin

# Fetch all remote changes
git fetch --all

# Rebase instead of merge
git rebase main
```

## 🎯 What's Next?

After completing Part 2:

**Continue to Part 3** for:
- Automated configuration backups with Python
- Interactive rebase for clean history
- Git hooks for validation
- Complete network change workflow

**Or review** if needed:
- Practice the exercises in each lesson
- Try the troubleshooting scenarios
- Experiment with different merge strategies

---

**Ready to start?** → [Lesson 1: Branching Strategies](01-branching-strategies.md)

**Need help?** Each lesson includes:
- Step-by-step instructions
- Expected outputs
- Troubleshooting tips
- Practice exercises

**Time to complete:** 2 hours
**Difficulty:** Intermediate
**Prerequisites:** Part 1 completed
