# Lesson 2: Remote Repositories with GitHub and GitLab

Master remote repositories, backup your configurations to the cloud, and understand GitHub/GitLab!

## 🎯 Objectives

By the end of this lesson, you'll be able to:
- Understand what GitHub and GitLab are
- Create accounts on GitHub or GitLab
- Set up SSH authentication
- Push local repositories to remote backup
- Clone repositories to multiple locations
- Pull updates from remotes

## 📝 What You'll Learn

- Understanding remote repositories
- GitHub vs GitLab comparison
- Account creation (step-by-step)
- SSH key generation and setup
- Connecting local and remote repositories
- Push, pull, clone, and fetch operations

## 🌐 Part 1: Understanding Remote Repositories

### What is a Remote Repository?

A **remote repository** is a copy of your Git repository stored on a server (like GitHub or GitLab) instead of your local machine.

```
Your Computer                    Cloud Server
┌─────────────────┐             ┌──────────────────┐
│  Local Repo     │   push →    │  Remote Repo     │
│  .git/          │   ← pull    │  (GitHub/GitLab) │
│                 │             │                  │
│  Working files  │             │  Backup copy     │
└─────────────────┘             └──────────────────┘
```

### Why Use Remotes?

**Disaster Recovery:**
- Hardware failures won't lose your configs
- Instant recovery from backup
- Multiple backup locations

**Collaboration:**
- Share configurations with team
- Work from multiple locations
- Coordinate changes safely

**Access Anywhere:**
- Clone to laptop, jump server, automation host
- Same configurations everywhere
- Always up-to-date

## 🌟 Part 2: GitHub vs GitLab

Both are excellent choices for hosting Git repositories. You only need **one** for this lab!

### GitHub

**What it is:**
- World's largest code hosting platform
- Owned by Microsoft
- 100+ million users

**Best for:**
- Open source projects
- Public repositories
- Large community
- GitHub Actions CI/CD
- Integration with many tools

**Pricing:**
- Free: Unlimited public and private repos
- Paid: Advanced features ($4/month)

**When to choose:**
- Your organization uses it
- Public/open source projects
- Need extensive marketplace integrations

### GitLab

**What it is:**
- Complete DevOps platform
- Can self-host or use cloud
- Open core model

**Best for:**
- Private enterprise projects
- Self-hosted requirements
- Built-in CI/CD pipelines
- Complete DevOps toolchain
- Advanced security features

**Pricing:**
- Free: Unlimited repos, basic CI/CD
- Paid: Advanced features ($19/month)

**When to choose:**
- Need self-hosted option
- Want built-in DevOps platform
- Require advanced security
- Your organization uses it

### Quick Comparison

| Feature | GitHub | GitLab |
|---------|--------|--------|
| **Free private repos** | ✅ Yes | ✅ Yes |
| **Free public repos** | ✅ Yes | ✅ Yes |
| **CI/CD** | GitHub Actions | Built-in pipelines |
| **Self-hosting** | ❌ No | ✅ Yes |
| **Community** | Larger | Growing |
| **Interface** | Simpler | More features |
| **Best for** | Public projects | Enterprise/DevOps |

**For this lab:** Choose whichever your organization uses, or GitHub if unsure.

## 🚀 Part 3: Setting Up GitHub

### Step 1: Create GitHub Account

1. **Visit** https://github.com

2. **Click** "Sign up" (top right)

3. **Enter your information:**
   - Email address (use work email for professional repos)
   - Password (strong password required)
   - Username (choose wisely - this appears in URLs)
   - Verify you're human (solve puzzle)

4. **Verify email:**
   - Check your email inbox
   - Click verification link
   - Complete verification

5. **Choose free plan:**
   - Select "Free" option
   - Skip surveys (or fill them out)
   - You're now on GitHub!

### Step 2: Create Your First Repository

**On GitHub website:**

1. **Click** the "+" icon (top right) → "New repository"

2. **Fill in details:**
   ```
   Repository name: network-configs
   Description: Network device configuration backup
   Visibility: ⚪ Public or 🔘 Private (choose Private for work)
   Initialize: ☐ Do NOT check "Add README" (we have local repo)
   ```

3. **Click** "Create repository"

4. **You'll see** quick setup page with instructions - **keep this page open!**

### Step 3: Generate SSH Key (if you haven't already)

```bash
# Check if you already have an SSH key
ls -la ~/.ssh/id_*.pub

# If you see id_rsa.pub or id_ed25519.pub, you already have one!
# If not, generate one:

# Generate new ED25519 SSH key (recommended)
ssh-keygen -t ed25519 -C "your.email@example.com"

# Press Enter for default location (~/.ssh/id_ed25519)
# Enter passphrase (recommended but optional)
# Press Enter again to confirm

# Start SSH agent
eval "$(ssh-agent -s)"

# Add key to agent
ssh-add ~/.ssh/id_ed25519
```

### Step 4: Add SSH Key to GitHub

```bash
# Display your PUBLIC key
cat ~/.ssh/id_ed25519.pub
```

Copy the entire output (starts with `ssh-ed25519` and ends with your email).

**On GitHub:**

1. Click your profile picture (top right) → **Settings**

2. In left sidebar → **SSH and GPG keys**

3. Click **"New SSH key"**

4. **Fill in:**
   ```
   Title: My Laptop (or descriptive name)
   Key type: Authentication Key
   Key: (paste your public key here)
   ```

5. Click **"Add SSH key"**

6. **Confirm** with your GitHub password if prompted

### Step 5: Test SSH Connection

```bash
# Test connection to GitHub
ssh -T git@github.com
```

**First time?** You'll see:
```
The authenticity of host 'github.com' can't be established.
ED25519 key fingerprint is SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU.
Are you sure you want to continue connecting (yes/no)?
```

Type `yes` and press Enter.

**Success looks like:**
```
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

Perfect! You're connected.

### Step 6: Connect Local Repository to GitHub

**Go to your local repository:**

```bash
cd ~/network-configs

# Add GitHub as remote (use URL from GitHub setup page)
git remote add origin git@github.com:yourusername/network-configs.git

# Verify remote was added
git remote -v
```

Output:
```
origin  git@github.com:yourusername/network-configs.git (fetch)
origin  git@github.com:yourusername/network-configs.git (push)
```

### Step 7: Push to GitHub

```bash
# Push your commits to GitHub
git push -u origin main
```

**First time output:**
```
Enumerating objects: 6, done.
Counting objects: 100% (6/6), done.
Delta compression using up to 4 threads
Compressing objects: 100% (4/4), done.
Writing objects: 100% (6/6), 1.2 KiB | 1.2 MiB/s, done.
Total 6 (delta 0), reused 0 (delta 0)
To github.com:yourusername/network-configs.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

**What `-u` means:**
- `-u` = `--set-upstream`
- Creates tracking relationship
- Future pushes just need `git push` (no arguments)

### Step 8: Verify on GitHub

1. **Refresh** your GitHub repository page
2. **You should see:**
   - Your commit history
   - Your files (SW-ACCESS-01.cfg, etc.)
   - Commit messages
   - Branch: main

**Success!** Your configurations are backed up to GitHub.

## 🔷 Part 4: Setting Up GitLab (Alternative)

*Use this instead of GitHub if that's your organization's choice*

### Step 1: Create GitLab Account

1. **Visit** https://gitlab.com

2. **Click** "Register" or "Get free trial"

3. **Fill in registration:**
   ```
   First name: Your Name
   Last name: Last Name
   Username: yourusername
   Email: your.email@example.com
   Password: (strong password)
   ```

4. **Verify email** (check inbox, click link)

5. **Complete profile** (optional surveys)

### Step 2: Create Project on GitLab

1. Click **"New project"** (big button)

2. Click **"Create blank project"**

3. **Fill in details:**
   ```
   Project name: network-configs
   Project slug: network-configs (auto-filled)
   Visibility: Private
   Initialize: ☐ Do NOT check "Initialize repository"
   ```

4. Click **"Create project"**

### Step 3: SSH Key Setup (GitLab)

Same as GitHub! If you already generated SSH key for GitHub, use same one.

If you need to generate:

```bash
ssh-keygen -t ed25519 -C "your.email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub
```

**On GitLab:**

1. Click your avatar (top right) → **Preferences**

2. Left sidebar → **SSH Keys**

3. **Paste your public key** in the "Key" box

4. **Fill in:**
   ```
   Title: My Laptop
   Usage type: Authentication & Signing
   Expiration date: (optional, or leave blank)
   ```

5. Click **"Add key"**

### Step 4: Test GitLab SSH

```bash
ssh -T git@gitlab.com
```

Success:
```
Welcome to GitLab, @yourusername!
```

### Step 5: Connect to GitLab

```bash
cd ~/network-configs

# Add GitLab as remote
git remote add origin git@gitlab.com:yourusername/network-configs.git

# Verify
git remote -v

# Push to GitLab
git push -u origin main
```

## 💡 Part 5: Working with Remotes

### Daily Workflow

```bash
# Morning: Get latest changes
git pull

# Make changes to configs
vim SW-ACCESS-01.cfg

# Stage and commit
git add SW-ACCESS-01.cfg
git commit -m "Update VLAN configuration"

# Push to backup
git push
```

### Clone Repository Elsewhere

**Scenario:** You need configs on your jump server.

```bash
# On jump server
cd ~
git clone git@github.com:yourusername/network-configs.git

# Navigate into it
cd network-configs

# You now have a complete copy!
ls -la
```

### Multiple Locations Workflow

```
Your Laptop                     GitHub/GitLab              Jump Server
┌─────────────┐                ┌─────────────┐            ┌─────────────┐
│ Make change │    push →      │             │            │             │
│             │                │   Central   │            │             │
│ git push    │                │   Remote    │  ← pull    │  git pull   │
└─────────────┘                └─────────────┘            └─────────────┘
```

**On Laptop:**
```bash
# Make changes
vim SW-ACCESS-02.cfg
git add .
git commit -m "Add SW-ACCESS-02"
git push
```

**On Jump Server:**
```bash
# Get updates
git pull
# You now have SW-ACCESS-02.cfg!
```

### View Remote Information

```bash
# List remotes
git remote -v

# Show remote details
git remote show origin

# See remote branches
git branch -r
```

## 🧪 Practice Exercises

### Exercise 1: Push New Configuration

```bash
# Create router config
cat > RTR-CORE-01.cfg << 'EOF'
hostname RTR-CORE-01
!
interface GigabitEthernet0/0
 description WAN-LINK
 ip address 203.0.113.1 255.255.255.252
 no shutdown
!
interface GigabitEthernet0/1
 description LAN-LINK
 ip address 192.168.1.1 255.255.255.0
 no shutdown
!
router ospf 1
 network 192.168.1.0 0.0.0.255 area 0
!
end
EOF

# Commit locally
git add RTR-CORE-01.cfg
git commit -m "Add core router configuration"

# Push to remote
git push

# Verify on GitHub/GitLab web interface
```

### Exercise 2: Clone to Another Location

```bash
# Simulate another machine
cd /tmp

# Clone your repository
git clone git@github.com:yourusername/network-configs.git test-clone

# Navigate and verify
cd test-clone
ls -la
git log --oneline

# Clean up
cd ~
rm -rf /tmp/test-clone
```

### Exercise 3: Fetch vs Pull

```bash
# Fetch downloads changes but doesn't apply them
git fetch origin

# See what's different
git log HEAD..origin/main

# Now apply the changes
git merge origin/main

# Pull does both in one command
git pull
# Equivalent to: git fetch && git merge
```

## 📊 Remote Commands Reference

```bash
# Adding remotes
git remote add <name> <url>                    # Add remote
git remote add origin git@github.com:user/repo.git

# Viewing remotes
git remote                                     # List remote names
git remote -v                                  # List with URLs
git remote show origin                         # Detailed info

# Pushing
git push origin main                           # Push branch to remote
git push -u origin main                        # Push and set tracking
git push                                       # Push current branch

# Pulling
git pull                                       # Fetch and merge
git pull origin main                           # Pull specific branch

# Cloning
git clone <url>                                # Clone repository
git clone <url> <directory>                    # Clone to specific dir

# Fetching
git fetch origin                               # Download changes (no merge)
git fetch --all                                # Fetch from all remotes

# Removing/renaming
git remote remove origin                       # Remove remote
git remote rename origin upstream              # Rename remote
```

## ✅ Verification Checklist

Make sure you can:

- [ ] Create account on GitHub or GitLab
- [ ] Generate SSH key
- [ ] Add SSH key to account
- [ ] Test SSH connection successfully
- [ ] Create repository on GitHub/GitLab
- [ ] Add remote to local repository
- [ ] Push commits to remote
- [ ] View repository on web interface
- [ ] Clone repository to another location
- [ ] Pull changes from remote

## ❓ Common Issues

### Issue: "Permission denied (publickey)"

**Cause:** SSH key not set up correctly

**Solution:**
```bash
# Check if SSH agent has your key
ssh-add -l

# If empty, add your key
ssh-add ~/.ssh/id_ed25519

# Test connection again
ssh -T git@github.com  # or gitlab.com
```

### Issue: "fatal: remote origin already exists"

**Cause:** Remote named 'origin' already configured

**Solution:**
```bash
# View existing remotes
git remote -v

# Remove old remote
git remote remove origin

# Add correct one
git remote add origin git@github.com:yourusername/repo.git
```

### Issue: "error: failed to push some refs"

**Cause:** Remote has commits you don't have locally

**Solution:**
```bash
# Pull first to merge remote changes
git pull origin main

# Then push
git push origin main
```

### Issue: "Repository not found"

**Cause:** URL is wrong or you don't have access

**Solution:**
```bash
# Check remote URL
git remote -v

# Update if wrong
git remote set-url origin git@github.com:correctusername/repo.git

# Verify SSH access
ssh -T git@github.com
```

### Issue: SSH key passphrase prompt every time

**Solution:**
```bash
# Add key to SSH agent permanently
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# On Mac, save to keychain
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

## 🎯 Best Practices

### Repository Naming

✅ **GOOD:**
- `network-configs`
- `cisco-switch-configs`
- `datacenter-infrastructure`

❌ **BAD:**
- `my-stuff`
- `test123`
- `temp`

### Remote Names

- `origin` - Your primary remote (convention)
- `backup` - Secondary backup remote
- `upstream` - Original repo (if you forked)

### When to Push

✅ **DO push:**
- After completing a feature
- End of work session
- Before risky operations
- When code is tested and working

❌ **DON'T push:**
- Half-finished features
- Code that doesn't work
- Sensitive data or passwords
- Very large binary files

### Private vs Public

**Use Private for:**
- Production configurations
- Work projects
- Sensitive information
- Internal tools

**Use Public for:**
- Educational content
- Open source projects
- Templates and examples
- Documentation

## 🎉 Lesson Complete!

You now know:

✅ What GitHub and GitLab are
✅ How to create accounts
✅ SSH key generation and setup
✅ Pushing to remote repositories
✅ Cloning and pulling changes
✅ Working with multiple locations

### What's Next?

**Next Lesson:** [History Navigation and Recovery](03-history-recovery.md)

Learn to:
- View detailed commit history
- Compare configurations over time
- Find when bugs were introduced
- Recover from mistakes
- Restore previous versions

---

**Lesson Duration:** 40 minutes
**Difficulty:** Beginner
**Skills:** Remote repositories, GitHub/GitLab, SSH, push/pull operations
