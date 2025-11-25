# Lesson 3: Pull Requests and Code Review

Master the professional workflow for reviewing and merging changes through pull requests.

## 🎯 Objectives

By the end of this lesson, you'll be able to:
- Create pull requests on GitHub and GitLab
- Review code changes effectively
- Comment on specific lines and suggest changes
- Approve or request changes to PRs
- Merge pull requests properly
- Understand PR best practices

## 📝 What You'll Learn

- What pull requests are and why they're essential
- Creating PRs on GitHub and GitLab
- Code review process and etiquette
- Using PR discussions effectively
- Merging strategies for PRs

## 🔍 Part 1: Understanding Pull Requests

### What is a Pull Request?

A **Pull Request (PR)** is a formal request to merge changes from one branch into another. It's called a **Merge Request (MR)** in GitLab, but the concept is identical.

**Without PR:**
```bash
git checkout main
git merge feature-branch
# Changes immediately in main
```

**With PR:**
```bash
git push origin feature-branch
# Create PR on GitHub/GitLab
# Team reviews
# Discuss, request changes
# Approve
# Then merge
```

### Why Use Pull Requests?

**Network Engineering Scenario:**

**Before PRs (risky):**
```
Junior engineer → makes change → pushes to main → breaks production ❌
```

**With PRs (safe):**
```
Junior engineer → creates branch → pushes branch → creates PR
    ↓
Senior engineer reviews → "Change logging level to informational"
    ↓
Junior engineer updates → senior approves → merge to main ✓
```

### PR Benefits

✅ **Code review** - Catch mistakes before production
✅ **Knowledge sharing** - Team learns from each other
✅ **Discussion** - Ask questions, suggest improvements
✅ **Testing** - Run automated tests before merging
✅ **Audit trail** - See who approved what
✅ **Quality control** - Enforce standards

### Real-World Use Cases

**Use Case 1: Configuration Review**
```
Engineer adds new security ACLs → PR → Security team reviews → Approves → Deploy
```

**Use Case 2: Multi-Site Deployment**
```
Test in Chicago site → PR for Chicago → Review → Merge
Clone config for Dallas → PR for Dallas → Review → Merge
```

**Use Case 3: Change Request Process**
```
CHG0012345: Add new VLANs
  ↓
Create branch CHG0012345-vlans
  ↓
PR with change ticket reference
  ↓
Change board reviews and approves
  ↓
Merge and deploy
```

## 🚀 Part 2: Creating Pull Requests on GitHub

### Prerequisites

```bash
cd ~/network-configs

# Ensure you have:
# 1. GitHub repository (from Part 1)
# 2. Local repository connected to GitHub
git remote -v
# Should show: origin  git@github.com:yourusername/network-configs.git
```

### Step 1: Create a Feature Branch

```bash
# Start from updated main
git checkout main
git pull

# Create feature branch
git checkout -b feature/add-security-settings
```

### Step 2: Make Changes

```bash
# Add security configurations
cat >> SW-ACCESS-01.cfg << 'EOF'
!
! Security Hardening
!
interface range GigabitEthernet0/2-24
 switchport port-security maximum 2
 switchport port-security violation restrict
 switchport port-security mac-address sticky
!
spanning-tree portfast bpduguard default
!
no ip http server
no ip http secure-server
!
service password-encryption
!
EOF
```

```bash
# Commit the changes
git add SW-ACCESS-01.cfg
git commit -m "Add port security and hardening settings

- Enable port security on access ports (max 2 MACs)
- Configure sticky MAC learning
- Enable BPDU guard on portfast ports
- Disable HTTP/HTTPS services
- Enable password encryption

CHG0012345"
```

### Step 3: Push Branch to GitHub

```bash
# Push the branch
git push -u origin feature/add-security-settings
```

**Output:**
```
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 456 bytes | 456.00 KiB/s, done.
Total 3 (delta 1), reused 0 (delta 0)
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
remote:
remote: Create a pull request for 'feature/add-security-settings' on GitHub by visiting:
remote:      https://github.com/yourusername/network-configs/pull/new/feature/add-security-settings
remote:
To github.com:yourusername/network-configs.git
 * [new branch]      feature/add-security-settings -> feature/add-security-settings
```

**Notice:** GitHub gives you a direct link to create the PR!

### Step 4: Create PR on GitHub Web Interface

**Option A: Use the link from push output**

Click the URL shown above, or:

**Option B: Navigate manually:**

1. Go to https://github.com/yourusername/network-configs
2. You'll see a yellow banner: "feature/add-security-settings had recent pushes"
3. Click **"Compare & pull request"**

**Option C: From Pull Requests tab:**

1. Click **"Pull requests"** tab
2. Click **"New pull request"** button
3. Select:
   - Base: `main`
   - Compare: `feature/add-security-settings`
4. Click **"Create pull request"**

### Step 5: Fill Out PR Information

**Title:**
```
Add port security and hardening settings
```

**Description (use this template):**
```markdown
## Summary
Implements security hardening configurations for access switches per security policy SEC-2024-001.

## Changes
- ✅ Port security on access ports (max 2 MAC addresses)
- ✅ Sticky MAC address learning
- ✅ BPDU guard on portfast ports
- ✅ Disabled HTTP/HTTPS management
- ✅ Enabled password encryption

## Testing
- [x] Tested on lab switch SW-LAB-01
- [x] Verified port security triggers correctly
- [x] Confirmed BPDU guard blocks rogue BPDUs
- [ ] Pending approval from security team

## Change Ticket
CHG0012345

## Deployment Notes
Apply during maintenance window. May briefly disrupt port connectivity as port security initializes.

## Reviewers
@security-team @network-lead
```

**Tips for good PR descriptions:**
- ✅ Explain **why**, not just what
- ✅ List specific changes
- ✅ Include testing performed
- ✅ Link to change tickets
- ✅ Tag relevant reviewers
- ✅ Note any deployment considerations

### Step 6: Request Reviewers

On the right sidebar:
1. Click **"Reviewers"**
2. Select teammates to review
3. They'll receive notification

### Step 7: Create the PR

Click **"Create pull request"**

**🎉 Your first PR is created!**

## 🔍 Part 3: Creating Pull Requests on GitLab

The process is similar but with GitLab terminology:

### Push Branch to GitLab

```bash
git push -u origin feature/add-security-settings
```

### Create Merge Request (GitLab's name for PR)

**Option A: Use the link from push output**

GitLab shows:
```
remote: To create a merge request for feature/add-security-settings, visit:
remote:   https://gitlab.com/yourusername/network-configs/-/merge_requests/new?merge_request[source_branch]=feature/add-security-settings
```

**Option B: Navigate manually:**

1. Go to your project on GitLab
2. Click **"Merge requests"** in left sidebar
3. Click **"New merge request"**
4. Select:
   - Source branch: `feature/add-security-settings`
   - Target branch: `main`
5. Click **"Compare branches and continue"**

### Fill Out Merge Request

**Title and description:** Same as GitHub example above

**Additional GitLab options:**
- **Assignee:** Person responsible for merging
- **Milestone:** Project milestone
- **Labels:** Add tags (e.g., `security`, `configuration`)
- **Delete source branch:** Check this to auto-delete after merge

Click **"Create merge request"**

## 👁️ Part 4: Reviewing Pull Requests

### As a Reviewer: View the PR

**On GitHub:**
1. Navigate to repository
2. Click **"Pull requests"** tab
3. Click on the PR to review

**On GitLab:**
1. Navigate to project
2. Click **"Merge requests"** in sidebar
3. Click on the MR to review

### Review Tabs (GitHub)

**Conversation Tab:**
- Overall discussion
- Status checks (if configured)
- Merge button

**Commits Tab:**
- List of all commits in the PR
- Click any to see changes

**Files changed Tab:**
- **Most important!** See all code changes
- Line-by-line diff

**Checks Tab:**
- Automated test results
- CI/CD pipeline status

### Reviewing the Code Changes

Click **"Files changed"** tab:

**You'll see:**
```diff
diff --git a/SW-ACCESS-01.cfg b/SW-ACCESS-01.cfg
index a1b2c3d..d4e5f6g 100644
--- a/SW-ACCESS-01.cfg
+++ b/SW-ACCESS-01.cfg
@@ -15,6 +15,18 @@ interface GigabitEthernet0/1
  switchport mode trunk
  switchport trunk allowed vlan 10,20,99
 !
+! Security Hardening
+!
+interface range GigabitEthernet0/2-24
+ switchport port-security maximum 2
+ switchport port-security violation restrict
+ switchport port-security mac-address sticky
+!
+spanning-tree portfast bpduguard default
+!
+no ip http server
+no ip http secure-server
+!
 line vty 0 4
  transport input ssh
 !
```

**Understanding the diff:**
- Green lines with `+` = Added
- Red lines with `-` = Removed (none in this example)
- Line numbers on left
- Context lines (unchanged) shown around changes

### Adding Comments

**Comment on specific lines:**

1. Hover over line number in diff
2. Click the **+** (plus) icon that appears
3. Type your comment
4. Click **"Start a review"** (or **"Add review comment"**)

**Example comments:**

**Line 21 (port security maximum 2):**
```
Should this be 3? We have some desks with PC + phone + printer.
```

**Line 22 (violation restrict):**
```
✓ Good choice. 'restrict' logs violations but keeps port up. Better than 'shutdown' for troubleshooting.
```

**Line 28 (no ip http server):**
```
⚠️ Confirm this won't break our monitoring tool. Let's verify it uses SNMP, not HTTP polling.
```

### Review Types

**Comment:** 💬
- Ask questions
- Suggest improvements
- General discussion
- No approval/rejection

**Approve:** ✅
- Changes look good
- Ready to merge
- Formal approval

**Request Changes:** ⚠️
- Must be fixed before merge
- Blocks merging (if required reviews enabled)
- Formal rejection until addressed

### Submitting Your Review

After commenting on lines:

1. Click **"Finish your review"** (top right)
2. Write overall summary
3. Choose review type:
   - **Comment** - Just discussion
   - **Approve** - LGTM (Looks Good To Me)
   - **Request changes** - Needs work
4. Click **"Submit review"**

## ✏️ Part 5: Responding to Review Comments

### As PR Author: View Comments

You'll receive email notification when review is submitted.

**On GitHub:**
1. Go to your PR
2. Click **"Conversation"** or **"Files changed"** tab
3. See inline comments

### Responding to Comments

**Option 1: Reply to discussion**
- Click **"Reply"** on comment thread
- Answer questions
- Explain decisions

**Option 2: Make requested changes**

```bash
# Still on your feature branch
git checkout feature/add-security-settings

# Make the requested changes
# Example: Change port-security maximum to 3
nano SW-ACCESS-01.cfg

# Commit the fix
git add SW-ACCESS-01.cfg
git commit -m "Change port-security maximum to 3 per review feedback"

# Push to same branch
git push
```

**✨ Magic:** The PR automatically updates with your new commit!

**Option 3: Use suggestion feature (GitHub)**

If reviewer used "suggestion" feature:
1. View suggestion in PR
2. Click **"Commit suggestion"**
3. Done! Changes committed automatically

### Resolving Conversations

After addressing a comment:
1. Reply explaining what you did
2. Click **"Resolve conversation"**
3. This collapses the thread

**Reviewer:** Can also resolve if satisfied

### Re-request Review

After making changes:
1. Click the 🔄 (refresh) icon next to reviewer's name
2. They get notified to review again

## 🎯 Part 6: Merging Pull Requests

### Prerequisites for Merging

Check that:
- ✅ All required reviews approved
- ✅ All CI/CD checks pass (if configured)
- ✅ No merge conflicts
- ✅ All conversations resolved
- ✅ Branch is up to date with main

### Merge Strategies

**1. Create a merge commit (default)**
```
Preserves full history with merge commit
Best for: Feature branches, maintaining full context
```

**2. Squash and merge**
```
Combines all commits into single commit
Best for: Cleaning up messy commit history
```

**3. Rebase and merge**
```
Replays commits on main without merge commit
Best for: Linear history, small changes
```

### How to Merge (GitHub)

1. **Scroll to bottom** of PR "Conversation" tab
2. Click **"Merge pull request"** (green button)
3. Choose merge strategy from dropdown
4. **Optional:** Edit merge commit message
5. Click **"Confirm merge"**
6. **Optional:** Click **"Delete branch"** (recommended)

**Output:**
```
✓ Pull request successfully merged and closed
  feature/add-security-settings can be safely deleted
```

### How to Merge (GitLab)

1. Click **"Merge"** button on MR page
2. **Options before merging:**
   - ☑️ Delete source branch (recommended)
   - ☑️ Squash commits (if desired)
3. Click **"Merge"**

### After Merging

```bash
# Update your local repository
git checkout main
git pull

# Verify the changes are in main
git log --oneline

# Delete local feature branch
git branch -d feature/add-security-settings

# Delete remote branch (if not auto-deleted)
git push origin --delete feature/add-security-settings
```

## 📋 Part 7: PR Best Practices

### Creating Good PRs

✅ **DO:**
- **Small PRs** - 1-2 files, <500 lines of changes
- **Single purpose** - One feature or fix per PR
- **Descriptive titles** - "Add port security" not "Update config"
- **Detailed descriptions** - Explain why, not just what
- **Link tickets** - Reference CHG, INC, or JIRA numbers
- **Self-review first** - Check your own diff before requesting review

❌ **DON'T:**
- Giant PRs (1000+ lines) - Hard to review
- Mixed changes - "Fix bug and add feature and refactor"
- Vague descriptions - "Updated files"
- Force push after review - Confuses reviewers

### Reviewing Code

✅ **DO:**
- **Be constructive** - Suggest improvements, don't just criticize
- **Ask questions** - "Why did you choose X?" not "X is wrong"
- **Explain reasoning** - "This could cause Y because Z"
- **Praise good work** - "Nice catch!" "Good approach!"
- **Test if possible** - Pull branch and test locally

❌ **DON'T:**
- Be rude or dismissive
- Nitpick trivial things
- Approve without reading
- Let PRs sit for days

### Review Etiquette

**Good comment examples:**

✅ "Consider using 'shutdown' instead of 'restrict' here. While restrict is generally better, this is our DMZ interface where we want aggressive security."

✅ "Nice! This matches our new security baseline. Can you also add this to the Dallas switches?"

✅ "Question: Have we tested this with our IP phone models? I'm worried about the MAC limit."

**Bad comment examples:**

❌ "This is wrong." (Not constructive)

❌ "Why didn't you do X?" (Accusatory tone)

❌ "I wouldn't have done it this way." (Not helpful without explanation)

### PR Description Template

Save this as `.github/pull_request_template.md`:

```markdown
## Summary
Brief description of the change and why it's needed.

## Type of Change
- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📝 Documentation update

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing Performed
- [x] Tested in lab environment
- [ ] Tested in staging
- [ ] Tested in production

## Change Ticket
Closes #123
Relates to CHG0012345

## Deployment Notes
Any special instructions for deploying this change.

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] My changes generate no new warnings
- [ ] I have updated documentation accordingly
```

## 🧪 Practice Exercises

### Exercise 1: Create Your First PR

Complete end-to-end PR workflow:

```bash
cd ~/network-configs
git checkout main
git pull

# Create feature
git checkout -b feature/add-ntp-servers

# Make change
cat >> SW-ACCESS-01.cfg << 'EOF'
!
ntp server 10.1.1.1 prefer
ntp server 10.1.1.2
!
EOF

git add SW-ACCESS-01.cfg
git commit -m "Add NTP servers for time synchronization"
git push -u origin feature/add-ntp-servers

# Go to GitHub/GitLab and create PR
# Fill out description
# Request review
```

### Exercise 2: Review a PR

Ask a colleague to create a PR, then:

1. View the PR
2. Check the **Files changed** tab
3. Add comments on at least 2 lines
4. Submit review with approval

### Exercise 3: Respond to Review

Have someone review your PR, then:

1. Read their comments
2. Make requested changes
3. Push updates
4. Reply to comments
5. Resolve conversations

### Exercise 4: Merge a PR

After approval:

1. Ensure all checks pass
2. Choose merge strategy
3. Merge the PR
4. Delete the branch
5. Pull changes locally

## 📊 Commands Reference

```bash
# Create and push feature branch
git checkout -b feature-name
git push -u origin feature-name

# Update PR with new commits
git add .
git commit -m "Address review comments"
git push

# Fetch PR from others to test locally
git fetch origin
git checkout pull/123/head       # GitHub
git checkout merge-requests/123   # GitLab

# Update branch with main changes
git checkout feature-branch
git merge main                    # Or: git rebase main
git push

# Delete branch after merge
git branch -d feature-name               # Local
git push origin --delete feature-name    # Remote

# View PR diff locally
git diff main..feature-branch
```

## 📱 Using GitHub CLI (Optional)

Install `gh` CLI for faster PR workflow:

```bash
# Install GitHub CLI
# Ubuntu/Debian
sudo apt install gh

# macOS
brew install gh

# Authenticate
gh auth login

# Create PR from command line
git checkout -b feature/my-feature
# ... make changes ...
git push -u origin feature/my-feature
gh pr create --title "My feature" --body "Description"

# View PRs
gh pr list

# Check out PR
gh pr checkout 123

# Merge PR
gh pr merge 123 --squash --delete-branch

# View PR in browser
gh pr view 123 --web
```

## ✅ Verification Checklist

Make sure you can:

- [ ] Create a pull request on GitHub
- [ ] Create a merge request on GitLab
- [ ] Write a good PR description
- [ ] Request reviewers
- [ ] Review someone else's PR
- [ ] Comment on specific lines
- [ ] Approve or request changes
- [ ] Respond to review feedback
- [ ] Update an open PR
- [ ] Merge a pull request
- [ ] Delete merged branches

## ❓ Common Issues

### Issue: Can't create PR - "No changes"

**Cause:** Feature branch and main are identical
```bash
# Check if commits exist
git log main..feature-branch
# If empty, no commits to PR

# Make sure you committed your changes
git status
```

### Issue: PR shows more commits than expected

**Cause:** Branch not created from latest main
```bash
# Update your branch
git checkout feature-branch
git rebase main
git push --force-with-lease origin feature-branch
```

### Issue: Merge conflicts in PR

**Cause:** Main changed since branch was created
```bash
# Update branch with main's changes
git checkout feature-branch
git merge main
# Resolve conflicts
git add .
git commit
git push
```

### Issue: Can't merge - "Review required"

**Cause:** Repository requires approval before merge
**Solution:** Request review from someone with merge permissions

## 🎯 Advanced PR Features

### Draft Pull Requests

Create PR marked as work-in-progress:

**GitHub:** Click **"Create draft pull request"**
**GitLab:** Click **"Mark as draft"**

**Use when:**
- Early feedback needed
- Work not complete yet
- Sharing progress

**Convert to ready:**
- Click **"Ready for review"**

### Auto-linking Issues

In PR description:
```markdown
Closes #42
Fixes #56
Resolves #78
```

When PR merges, those issues auto-close!

### Protected Branches

Configure main branch to require:
- Minimum number of reviews
- Passing CI checks
- Up-to-date with base branch
- Signed commits

**GitHub:** Settings → Branches → Branch protection rules
**GitLab:** Settings → Repository → Protected branches

## 🎉 Lesson Complete!

You've learned:
✅ What pull requests are and why they're essential
✅ How to create PRs on GitHub and GitLab
✅ Code review process and best practices
✅ Responding to review feedback
✅ Merging PRs properly

### Next Steps

**Ready for Lesson 4?** → [Team Synchronization](04-team-sync.md)

Learn how to:
- Keep your work in sync with teammates
- Handle concurrent changes
- Use fetch vs. pull
- Resolve synchronization issues

**Or practice more:**
- Create multiple PRs
- Review others' code
- Try different merge strategies
- Set up branch protection

---

**Lesson Duration:** 30 minutes
**Difficulty:** Intermediate
**Next:** Team synchronization patterns
