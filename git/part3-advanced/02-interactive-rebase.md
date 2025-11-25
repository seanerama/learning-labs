# Lesson 2: Interactive Rebase for Clean History

Master interactive rebase to clean up messy commit history and maintain a professional project timeline.

## 🎯 Objectives

By the end of this lesson, you'll be able to:
- Understand when and why to use interactive rebase
- Squash multiple commits into one
- Reorder commits
- Edit commit messages
- Split commits
- Remove unwanted commits
- Maintain clean, readable Git history

## 📝 What You'll Learn

- Interactive rebase fundamentals
- Rebase commands (pick, squash, reword, edit, drop)
- Cleaning up work-in-progress commits
- When to rebase vs. when not to
- Safe rebasing practices

## 🔄 Part 1: Understanding Interactive Rebase

### What is Interactive Rebase?

**Regular rebase:** Replays commits onto a new base
**Interactive rebase:** Lets you **edit** commits while replaying them

### Why Use Interactive Rebase?

**Scenario: Messy Development History**

You're troubleshooting a VLAN configuration:

```bash
git log --oneline
```

**Output:**
```
d4e5f6g Fix VLAN again
c3d4e5f Try different VLAN
b2c3d4e Maybe this VLAN?
a1b2c3d Add VLAN 50
9a8b7c6 Initial config
```

**Problem:**
- 4 commits for one simple feature
- Commit messages are unclear
- History is cluttered
- Hard to understand what actually changed

**Solution with interactive rebase:**
```
After cleanup:
b2c3d4e Add VLAN 50 for server network
9a8b7c6 Initial config
```

One clean commit that explains what was done!

### When to Use Interactive Rebase

✅ **DO use interactive rebase:**
- Before creating a pull request
- Cleaning up local work-in-progress commits
- Combining related commits
- Improving commit messages
- Removing debug/test commits
- **Only on commits you haven't pushed** (or pushed to your private branch)

❌ **DON'T use interactive rebase:**
- On main/shared branches
- On commits others are working from
- After pull request has been reviewed
- On public history

### Real-World Network Engineering Example

**Bad history:**
```
Add ACL
Fix typo in ACL
Actually fix the ACL
Remove debug line
Add comment
Fix comment formatting
```

**Good history (after rebase):**
```
Add management ACL restricting SSH access to 10.0.0.0/8
```

## 🛠️ Part 2: Basic Interactive Rebase

### Setup: Create Practice History

```bash
cd ~/network-configs
git checkout main
git checkout -b practice-rebase

# Create some messy commits
echo "vlan 50" >> SW-ACCESS-01.cfg
git add SW-ACCESS-01.cfg
git commit -m "Add VLAN"

echo " name SERVERS" >> SW-ACCESS-01.cfg
git add SW-ACCESS-01.cfg
git commit -m "Try server name"

echo " name PRODUCTION-SERVERS" > temp.txt
cat SW-ACCESS-01.cfg | grep -v "name SERVERS" > temp2.txt
cat temp2.txt temp.txt > SW-ACCESS-01.cfg
rm temp.txt temp2.txt
git add SW-ACCESS-01.cfg
git commit -m "Actually name it production"

echo "! Servers VLAN" >> SW-ACCESS-01.cfg
git add SW-ACCESS-01.cfg
git commit -m "Add comment"

echo "! For production server farm" >> SW-ACCESS-01.cfg
git add SW-ACCESS-01.cfg
git commit -m "Better comment"

# View the messy history
git log --oneline
```

**Output:**
```
a1b2c3d (HEAD -> practice-rebase) Better comment
d4e5f6g Add comment
c3d4e5f Actually name it production
b2c3d4e Try server name
9a8b7c6 Add VLAN
f8e7d6c (main) Previous work
```

5 commits for one simple feature!

### Start Interactive Rebase

```bash
# Rebase last 5 commits
git rebase -i HEAD~5
```

**Or rebase everything since main:**
```bash
git rebase -i main
```

**Editor opens with:**
```
pick 9a8b7c6 Add VLAN
pick b2c3d4e Try server name
pick c3d4e5f Actually name it production
pick d4e5f6g Add comment
pick a1b2c3d Better comment

# Rebase f8e7d6c..a1b2c3d onto f8e7d6c (5 commands)
#
# Commands:
# p, pick <commit> = use commit
# r, reword <commit> = use commit, but edit the commit message
# e, edit <commit> = use commit, but stop for amending
# s, squash <commit> = use commit, but meld into previous commit
# f, fixup <commit> = like "squash" but discard this commit's log message
# x, exec <command> = run command (the rest of the line) using shell
# b, break = stop here (continue rebase later with 'git rebase --continue')
# d, drop <commit> = remove commit
# l, label <label> = label current HEAD with a name
# t, reset <label> = reset HEAD to a label
# m, merge [-C <commit> | -c <commit>] <label> [# <oneline>]
# .       create a merge commit using the original merge commit's
# .       message (or the oneline, if no original merge commit was
# .       specified); use -c <commit> to reword the commit message
#
# These lines can be re-ordered; they are executed from top to bottom.
#
# If you remove a line here THAT COMMIT WILL BE LOST.
#
# However, if you remove everything, the rebase will be aborted.
#
```

## 🎨 Part 3: Rebase Commands

### Command: pick (keep as-is)

```
pick 9a8b7c6 Add VLAN
```

**Effect:** Keep this commit unchanged

### Command: squash (combine with previous)

**Modify editor to:**
```
pick 9a8b7c6 Add VLAN
squash b2c3d4e Try server name
squash c3d4e5f Actually name it production
squash d4e5f6g Add comment
squash a1b2c3d Better comment
```

**Effect:** All 5 commits become 1

Save and close editor.

**Next editor opens for combined commit message:**
```
# This is a combination of 5 commits.
# This is the 1st commit message:

Add VLAN

# This is the commit message #2:

Try server name

# This is the commit message #3:

Actually name it production

# This is the commit message #4:

Add comment

# This is the commit message #5:

Better comment
```

**Replace with clean message:**
```
Add VLAN 50 for production server network

Configured VLAN 50 for the new production server farm.
VLAN will be used across all access switches in datacenter.
```

Save and close.

**Result:**
```bash
git log --oneline
```

**Output:**
```
b2c3d4e (HEAD -> practice-rebase) Add VLAN 50 for production server network
f8e7d6c (main) Previous work
```

One clean commit! ✨

### Command: fixup (squash but discard message)

Similar to squash but automatically uses the first commit's message:

```
pick 9a8b7c6 Add VLAN
fixup b2c3d4e Try server name
fixup c3d4e5f Actually name it production
fixup d4e5f6g Add comment
fixup a1b2c3d Better comment
```

**Effect:** Same as squash but no second editor - uses "Add VLAN" as message

### Command: reword (change commit message)

```
reword 9a8b7c6 Add VLAN
pick b2c3d4e Try server name
```

**Effect:** Editor opens to change "Add VLAN" message

**New message:**
```
Add VLAN 50 for production server network
```

### Command: edit (stop to amend commit)

```
edit 9a8b7c6 Add VLAN
pick b2c3d4e Try server name
```

**Effect:** Rebase stops at that commit

```bash
# Rebase pauses
# You can now make changes

echo "! Additional change" >> SW-ACCESS-01.cfg
git add SW-ACCESS-01.cfg
git commit --amend --no-edit

# Continue rebase
git rebase --continue
```

### Command: drop (remove commit)

```
pick 9a8b7c6 Add VLAN
drop b2c3d4e Try server name
pick c3d4e5f Actually name it production
```

**Effect:** "Try server name" commit removed from history

**Or delete the line:**
```
pick 9a8b7c6 Add VLAN
pick c3d4e5f Actually name it production
```

Same effect!

### Reordering Commits

Just reorder the lines:

**Before:**
```
pick 9a8b7c6 Add VLAN
pick b2c3d4e Add ACL
pick c3d4e5f Add NTP
```

**After:**
```
pick c3d4e5f Add NTP
pick 9a8b7c6 Add VLAN
pick b2c3d4e Add ACL
```

**Effect:** Commits applied in new order (NTP, then VLAN, then ACL)

## 🔧 Part 4: Real-World Scenarios

### Scenario 1: Clean Up Before Pull Request

**Situation:** You made 10 commits while developing a feature

```bash
git log --oneline
```

**Output:**
```
j9k8l7m Fix typo in comment
i8j7k6l Adjust port range
h7i6j5k Add port security (actually works now)
g6h5i4j Fix port security
f5g4h3i Try port security again
e4f3g2h Debug port security
d3e2f1g WIP port security
c2d1e0f Add port security
b1c0d9e Update config
a0b9c8d Initial attempt
```

**Action:** Clean this up before creating PR

```bash
git rebase -i HEAD~10
```

**Edit to:**
```
pick a0b9c8d Initial attempt
fixup b1c0d9e Update config
fixup c2d1e0f Add port security
fixup d3e2f1g WIP port security
fixup e4f3g2h Debug port security
fixup f5g4h3i Try port security again
fixup g6h5i4j Fix port security
pick h7i6j5k Add port security (actually works now)
fixup i8j7k6l Adjust port range
fixup j9k8l7m Fix typo in comment
```

Wait, that's still messy. Better:

```
pick a0b9c8d Initial attempt
fixup b1c0d9e Update config
squash c2d1e0f Add port security
fixup d3e2f1g WIP port security
fixup e4f3g2h Debug port security
fixup f5g4h3i Try port security again
fixup g6h5i4j Fix port security
fixup h7i6j5k Add port security (actually works now)
fixup i8j7k6l Adjust port range
fixup j9k8l7m Fix typo in comment
```

**Then update commit message:**
```
Add port security to access ports

Configured port security on GigabitEthernet0/2-24:
- Maximum 2 MAC addresses per port
- Violation mode: restrict (log but don't shutdown)
- Sticky MAC learning enabled

CHG0012345
```

**Result:**
```bash
git log --oneline
```

**Output:**
```
c3d4e5f (HEAD -> feature-port-security) Add port security to access ports
```

One professional commit!

### Scenario 2: Split a Large Commit

**Situation:** You made one commit with multiple unrelated changes

```bash
git log --oneline
```

**Output:**
```
a1b2c3d Add VLANs, ACLs, and NTP config
```

**Action:** Split into separate commits

```bash
git rebase -i HEAD~1
```

**Change to:**
```
edit a1b2c3d Add VLANs, ACLs, and NTP config
```

**Rebase stops:**
```bash
# Reset to previous commit but keep changes in working directory
git reset HEAD^

# Now stage and commit each part separately
git add -p  # Interactive staging

# Stage only VLAN changes
git commit -m "Add VLANs 50-60 for server network"

# Stage only ACL changes
git add -p
git commit -m "Add management ACL restricting SSH"

# Stage NTP changes
git add -p
git commit -m "Configure NTP servers for time sync"

# Continue rebase
git rebase --continue
```

**Result:**
```bash
git log --oneline
```

**Output:**
```
d4e5f6g Configure NTP servers for time sync
c3d4e5f Add management ACL restricting SSH
b2c3d4e Add VLANs 50-60 for server network
```

Three clear, focused commits!

### Scenario 3: Remove Debug/Test Commits

**Situation:** You committed debug output

```bash
git log --oneline
```

**Output:**
```
e5f6g7h Remove debug output
d4e5f6g Add debug output to troubleshoot
c3d4e5f Fix VLAN configuration
b2c3d4e Add VLAN
```

**Action:** Remove both debug commits

```bash
git rebase -i HEAD~4
```

**Edit to:**
```
pick b2c3d4e Add VLAN
pick c3d4e5f Fix VLAN configuration
drop d4e5f6g Add debug output to troubleshoot
drop e5f6g7h Remove debug output
```

**Result:** Clean history without debug noise

## ⚠️ Part 5: Handling Conflicts During Rebase

### When Conflicts Happen

```bash
git rebase -i HEAD~5
```

**Output:**
```
CONFLICT (content): Merge conflict in SW-ACCESS-01.cfg
error: could not apply c3d4e5f... Add port security
Resolve all conflicts manually, mark them as resolved with
"git add/rm <conflicted_files>", then run "git rebase --continue".
You can instead skip this commit: run "git rebase --skip".
To abort and get back to the state before "git rebase", run "git rebase --abort".
Could not apply c3d4e5f... Add port security
```

### Resolve Conflicts

```bash
# View conflicted files
git status

# Edit and resolve conflicts
nano SW-ACCESS-01.cfg

# Remove conflict markers:
# <<<<<<< HEAD
# =======
# >>>>>>> commit-hash

# Stage resolved files
git add SW-ACCESS-01.cfg

# Continue rebase
git rebase --continue
```

**If more conflicts:** Repeat process

**If stuck:** Abort and try different approach
```bash
git rebase --abort
```

## 🚀 Part 6: Safe Rebasing Practices

### Golden Rule: Never Rebase Published History

**Safe to rebase:**
```
Your local branch (not pushed)
Your feature branch (only you working on it)
Commits not yet in pull request
```

**NOT safe to rebase:**
```
main branch
Shared branches (multiple people working)
Commits already in pull request being reviewed
Anything pushed to public repository
```

### Force Pushing After Rebase

After rebasing, your branch history is different from remote:

```bash
git push
```

**Output:**
```
! [rejected]        feature -> feature (non-fast-forward)
error: failed to push some refs
```

**Must force push:**
```bash
# Safe way (checks remote hasn't changed)
git push --force-with-lease origin feature-branch

# Unsafe way (overwrites remote no matter what)
git push --force origin feature-branch  # Avoid this!
```

**⚠️ Only force push to YOUR branches!**

## 🧪 Practice Exercises

### Exercise 1: Squash Commits

```bash
cd ~/network-configs
git checkout -b exercise-squash

# Create 5 small commits
for i in {1..5}; do
  echo "Change $i" >> test-file.txt
  git add test-file.txt
  git commit -m "Change $i"
done

# View history
git log --oneline

# Squash into one commit
git rebase -i HEAD~5

# In editor, change all but first to 'squash'
# Save and write good combined commit message

# Verify
git log --oneline
```

### Exercise 2: Reorder Commits

```bash
git checkout -b exercise-reorder

# Create commits in wrong order
echo "Step 3" >> steps.txt
git add steps.txt
git commit -m "Step 3"

echo "Step 1" >> steps.txt
git add steps.txt
git commit -m "Step 1"

echo "Step 2" >> steps.txt
git add steps.txt
git commit -m "Step 2"

# Rebase and reorder
git rebase -i HEAD~3

# In editor, reorder lines:
# pick Step 1
# pick Step 2
# pick Step 3

# Verify
git log --oneline
```

### Exercise 3: Clean Up Messy History

```bash
git checkout -b exercise-cleanup

# Simulate messy development
echo "feature start" >> feature.txt
git add feature.txt
git commit -m "Start feature"

echo "WIP" >> feature.txt
git add feature.txt
git commit -m "WIP"

echo "broken" >> feature.txt
git add feature.txt
git commit -m "Fix"

echo "actually working" >> feature.txt
git add feature.txt
git commit -m "Actually fix"

echo "done" >> feature.txt
git add feature.txt
git commit -m "Done"

# Clean up
git rebase -i HEAD~5

# Squash all into one with good message
```

### Exercise 4: Remove a Commit

```bash
git checkout -b exercise-remove

# Create commits
echo "Good change 1" >> file.txt
git add file.txt
git commit -m "Good change 1"

echo "Mistake" >> file.txt
git add file.txt
git commit -m "Bad change - should not be here"

echo "Good change 2" >> file.txt
git add file.txt
git commit -m "Good change 2"

# Remove the mistake
git rebase -i HEAD~3

# In editor, drop the "Bad change" line

# Verify it's gone
git log --oneline
```

## 📊 Commands Reference

```bash
# Start interactive rebase
git rebase -i HEAD~N             # Last N commits
git rebase -i main               # All commits since main
git rebase -i <commit-hash>      # Since specific commit

# During rebase
git rebase --continue            # Continue after resolving conflicts
git rebase --skip                # Skip current commit
git rebase --abort               # Cancel rebase, return to start

# Common rebase actions (in editor)
pick    # Use commit as-is
reword  # Change commit message
edit    # Stop to amend commit
squash  # Combine with previous, edit message
fixup   # Combine with previous, keep previous message
drop    # Remove commit

# Force push after rebase
git push --force-with-lease origin branch-name  # Safe
git push --force origin branch-name             # Unsafe

# View what would be rebased
git log main..feature-branch
git log --oneline main..feature-branch

# Abort if things go wrong
git rebase --abort
```

## ✅ Verification Checklist

Make sure you can:

- [ ] Start an interactive rebase
- [ ] Squash multiple commits into one
- [ ] Reword a commit message
- [ ] Reorder commits
- [ ] Drop unwanted commits
- [ ] Resolve conflicts during rebase
- [ ] Continue or abort a rebase
- [ ] Force push safely after rebase

## ❓ Common Issues

### Issue: "Cannot rebase: You have unstaged changes"

**Solution:**
```bash
# Option 1: Commit changes
git add .
git commit -m "Save work"

# Option 2: Stash changes
git stash
git rebase -i HEAD~5
git stash pop
```

### Issue: Lost commits after rebase

**Solution:**
```bash
# Find lost commits
git reflog

# Output shows all HEAD movements:
# a1b2c3d HEAD@{0}: rebase -i (finish)
# d4e5f6g HEAD@{1}: commit: Lost commit

# Restore lost commit
git cherry-pick d4e5f6g

# Or reset to before rebase
git reset --hard HEAD@{1}
```

### Issue: Rebase created conflicts on every commit

**Cause:** Trying to rebase too many related commits

**Solution:**
```bash
# Abort this rebase
git rebase --abort

# Try rebasing fewer commits
# Or use a different strategy
```

### Issue: Editor won't open for rebase

**Solution:**
```bash
# Set your preferred editor
git config --global core.editor "nano"
# Or: vim, code --wait, etc.
```

## 🎯 Best Practices

### When to Rebase

✅ **DO rebase:**
- Before creating pull request
- Cleaning up local development
- Combining related commits
- Improving commit messages
- Your private feature branches

❌ **DON'T rebase:**
- main or master branch
- Shared team branches
- After pull request is under review
- Public history that others depend on

### Commit Message Guidelines After Rebase

Create clear, professional messages:

```
✅ Good:
"Add port security to access ports

Configured port security on GigabitEthernet0/2-24:
- Maximum 2 MAC addresses
- Violation mode: restrict
- Sticky MAC learning

CHG0012345"

❌ Bad:
"fixes"
"WIP"
"changed stuff"
"test"
```

### Squashing Strategy

**Pattern 1: Feature commits**
```
Squash ALL commits for a feature into ONE
Result: One commit per feature
```

**Pattern 2: Logical grouping**
```
Keep separate commits for distinct logical changes
Result: Clear history of major changes
```

## 🎉 Lesson Complete!

You've learned:
✅ Interactive rebase fundamentals
✅ Squashing and combining commits
✅ Reordering commit history
✅ Editing and removing commits
✅ Resolving rebase conflicts
✅ Safe rebasing practices

### Next Steps

**Ready for Lesson 3?** → [Git Hooks](03-git-hooks.md)

Learn how to:
- Create pre-commit validation hooks
- Prevent common mistakes automatically
- Enforce coding standards
- Automate quality checks

**Or practice more:**
- Clean up your actual feature branches
- Practice conflict resolution
- Try different squashing patterns
- Experiment with commit splitting

---

**Lesson Duration:** 20 minutes
**Difficulty:** Intermediate → Advanced
**Next:** Git hooks and automation
