# Lesson 3: Git Hooks for Automation and Validation

Implement Git hooks to automatically validate configurations, enforce standards, and prevent common mistakes.

## 🎯 Objectives

By the end of this lesson, you'll be able to:
- Understand what Git hooks are and how they work
- Create pre-commit hooks for validation
- Implement pre-push hooks
- Validate network configurations automatically
- Prevent commits with security issues
- Share hooks with your team

## 📝 What You'll Learn

- Git hooks fundamentals
- Available hook types
- Creating validation scripts
- Configuration syntax checking
- Security validation
- Sharing hooks across teams

## 🪝 Part 1: Understanding Git Hooks

### What Are Git Hooks?

**Git hooks** are scripts that run automatically when certain Git events occur.

**Common hooks:**
- `pre-commit` - Before commit is created
- `commit-msg` - Before commit message is saved
- `pre-push` - Before push to remote
- `post-commit` - After commit is created
- `post-receive` - After push (server-side)

### Why Use Hooks?

**Without hooks:**
```
Engineer commits → Push → Discover password in config → Revert ❌
```

**With hooks:**
```
Engineer commits → Hook checks → "Error: Password detected" → Fix before commit ✓
```

### Hook Benefits

✅ **Automatic validation** - Catch errors before they're committed
✅ **Enforce standards** - Consistent formatting and style
✅ **Prevent mistakes** - Block commits with security issues
✅ **Save time** - No manual checks needed
✅ **Improve quality** - Higher code quality automatically

### Real-World Network Engineering Examples

**Example 1: Password Validation**
```
Block commits containing:
- enable password cisco
- username admin password cisco123
- snmp-server community public
```

**Example 2: Required Commands**
```
Ensure configs have:
- hostname command
- logging configuration
- no ip http server
```

**Example 3: Syntax Validation**
```
Check for:
- Valid VLAN IDs (1-4094)
- Valid IP addresses
- Correct command syntax
```

## 📂 Part 2: Hook Location and Setup

### Where Hooks Live

```bash
cd ~/network-configs

# Hooks directory
ls -la .git/hooks/
```

**Sample hooks included:**
```
.git/hooks/
├── applypatch-msg.sample
├── commit-msg.sample
├── post-update.sample
├── pre-applypatch.sample
├── pre-commit.sample
├── pre-push.sample
├── pre-rebase.sample
├── prepare-commit-msg.sample
└── update.sample
```

**To activate a hook:**
1. Remove `.sample` extension
2. Make it executable (`chmod +x`)
3. Edit the script

### Create Your First Hook

```bash
cd ~/network-configs

# Create pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Simple pre-commit hook

echo "Running pre-commit checks..."

# Hook passes
exit 0
EOF

# Make executable
chmod +x .git/hooks/pre-commit

# Test it
echo "test" >> test.txt
git add test.txt
git commit -m "Test commit"
```

**Output:**
```
Running pre-commit checks...
[main a1b2c3d] Test commit
 1 file changed, 1 insertion(+)
```

Hook ran successfully!

## 🔒 Part 3: Security Validation Hook

### Pre-Commit: Block Default Passwords

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Pre-commit hook: Validate network configurations
# Prevents commits with security issues

echo "🔍 Validating configuration security..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track if validation passes
VALIDATION_PASSED=true

# Get list of staged config files
STAGED_CONFIGS=$(git diff --cached --name-only --diff-filter=ACM | grep '\.cfg$')

if [ -z "$STAGED_CONFIGS" ]; then
    echo "  ℹ  No configuration files to validate"
    exit 0
fi

echo "  📁 Checking files:"
echo "$STAGED_CONFIGS" | while read file; do
    echo "     - $file"
done
echo ""

# Check 1: Default passwords
echo "  🔐 Checking for default passwords..."
if git diff --cached | grep -iE "password (cisco|admin|password|123|default)"; then
    echo -e "${RED}  ✗ ERROR: Default password detected!${NC}"
    echo -e "${YELLOW}    Please change passwords before committing.${NC}"
    echo -e "${YELLOW}    Found in:${NC}"
    git diff --cached | grep -iE "password (cisco|admin|password|123|default)" | sed 's/^/      /'
    VALIDATION_PASSED=false
else
    echo -e "${GREEN}  ✓ No default passwords found${NC}"
fi

# Check 2: Public SNMP community strings
echo "  📡 Checking SNMP community strings..."
if git diff --cached | grep -iE "snmp-server community (public|private) RW"; then
    echo -e "${RED}  ✗ ERROR: Insecure SNMP community with RW access!${NC}"
    echo -e "${YELLOW}    Using 'public' or 'private' with RW access is a security risk.${NC}"
    VALIDATION_PASSED=false
else
    echo -e "${GREEN}  ✓ SNMP community strings look OK${NC}"
fi

# Check 3: HTTP server enabled
echo "  🌐 Checking for HTTP server..."
if git diff --cached | grep -E "^[+]ip http server$"; then
    echo -e "${YELLOW}  ⚠  Warning: HTTP server being enabled${NC}"
    echo -e "${YELLOW}    Consider using HTTPS only (ip http secure-server)${NC}"
    # Warning only, don't fail
else
    echo -e "${GREEN}  ✓ No insecure HTTP server${NC}"
fi

# Check 4: Required commands present
echo "  📋 Checking for required commands..."
for file in $STAGED_CONFIGS; do
    # Check if hostname is present
    if ! git show ":$file" | grep -q "^hostname "; then
        echo -e "${RED}  ✗ ERROR: Missing hostname command in $file${NC}"
        VALIDATION_PASSED=false
    fi
done

if [ "$VALIDATION_PASSED" = true ]; then
    echo ""
    echo -e "${GREEN}✓ All validation checks passed!${NC}"
    echo ""
    exit 0
else
    echo ""
    echo -e "${RED}✗ Validation failed. Please fix the issues above.${NC}"
    echo -e "${YELLOW}  To bypass this check (not recommended):${NC}"
    echo -e "${YELLOW}    git commit --no-verify${NC}"
    echo ""
    exit 1
fi
```

Make it executable:

```bash
chmod +x .git/hooks/pre-commit
```

### Test the Security Hook

**Test 1: Try to commit default password**

```bash
cat >> configs/SW-ACCESS-01.cfg << 'EOF'
!
username admin password cisco
!
EOF

git add configs/SW-ACCESS-01.cfg
git commit -m "Add admin user"
```

**Output:**
```
🔍 Validating configuration security...
  📁 Checking files:
     - configs/SW-ACCESS-01.cfg

  🔐 Checking for default passwords...
  ✗ ERROR: Default password detected!
    Please change passwords before committing.
    Found in:
      +username admin password cisco

✗ Validation failed. Please fix the issues above.
  To bypass this check (not recommended):
    git commit --no-verify
```

**Commit blocked!** ✓

**Fix it:**
```bash
# Change to encrypted password
cat > temp.cfg << 'EOF'
username admin secret MySecureP@ssw0rd!
EOF

git add configs/SW-ACCESS-01.cfg
git commit -m "Add admin user with secure password"
```

**Output:**
```
🔍 Validating configuration security...
  🔐 Checking for default passwords...
  ✓ No default passwords found
  📡 Checking SNMP community strings...
  ✓ SNMP community strings look OK
  🌐 Checking for HTTP server...
  ✓ No insecure HTTP server
  📋 Checking for required commands...

✓ All validation checks passed!

[main d4e5f6g] Add admin user with secure password
 1 file changed, 2 insertions(+)
```

**Commit successful!** ✓

## ✅ Part 4: Configuration Validation Hook

### Advanced Pre-Commit: Syntax Validation

Create enhanced `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Enhanced pre-commit hook with syntax validation

echo "🔍 Running configuration validation..."

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0

# Get staged config files
STAGED_CONFIGS=$(git diff --cached --name-only --diff-filter=ACM | grep '\.cfg$')

if [ -z "$STAGED_CONFIGS" ]; then
    echo "  ℹ  No configuration files to validate"
    exit 0
fi

# Function: Validate VLAN IDs
validate_vlans() {
    local file=$1
    echo "  🏷️  Validating VLAN IDs in $file..."

    # Extract VLAN IDs from staged content
    VLANS=$(git show ":$file" | grep -oP '(?<=^vlan )\d+')

    for vlan in $VLANS; do
        if [ $vlan -lt 1 ] || [ $vlan -gt 4094 ]; then
            echo -e "${RED}    ✗ Invalid VLAN ID: $vlan (must be 1-4094)${NC}"
            ((ERRORS++))
        fi
    done

    # Check for reserved VLANs in production
    for vlan in $VLANS; do
        if [ $vlan -eq 1002 ] || [ $vlan -eq 1003 ] || [ $vlan -eq 1004 ] || [ $vlan -eq 1005 ]; then
            echo -e "${YELLOW}    ⚠  Warning: VLAN $vlan is reserved for Token Ring/FDDI${NC}"
        fi
    done
}

# Function: Validate IP addresses
validate_ip_addresses() {
    local file=$1
    echo "  🌐 Validating IP addresses in $file..."

    # Extract IP addresses
    IPS=$(git show ":$file" | grep -oP '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

    for ip in $IPS; do
        IFS='.' read -r i1 i2 i3 i4 <<< "$ip"

        if [ $i1 -gt 255 ] || [ $i2 -gt 255 ] || [ $i3 -gt 255 ] || [ $i4 -gt 255 ]; then
            echo -e "${RED}    ✗ Invalid IP address: $ip${NC}"
            ((ERRORS++))
        fi

        # Warn about default/example IPs
        if [[ $ip == "192.0.2."* ]] || [[ $ip == "198.51.100."* ]] || [[ $ip == "203.0.113."* ]]; then
            echo -e "${YELLOW}    ⚠  Warning: $ip is an example/documentation IP (TEST-NET)${NC}"
        fi
    done
}

# Function: Check for required commands
validate_required_commands() {
    local file=$1
    echo "  📋 Checking required commands in $file..."

    local content=$(git show ":$file")

    # Hostname required
    if ! echo "$content" | grep -q "^hostname "; then
        echo -e "${RED}    ✗ Missing required command: hostname${NC}"
        ((ERRORS++))
    fi

    # Check for end-of-config marker
    if ! echo "$content" | grep -qE "(^end$|^end\s*$)"; then
        echo -e "${YELLOW}    ⚠  Warning: Config doesn't end with 'end' marker${NC}"
    fi
}

# Function: Security checks
validate_security() {
    local file=$1
    echo "  🔐 Checking security settings in $file..."

    local content=$(git show ":$file")

    # Check for default passwords
    if echo "$content" | grep -qiE "password (cisco|admin|password|123)"; then
        echo -e "${RED}    ✗ Default or weak password detected${NC}"
        ((ERRORS++))
    fi

    # Check if password encryption is enabled
    if ! echo "$content" | grep -q "service password-encryption"; then
        echo -e "${YELLOW}    ⚠  Warning: Password encryption not enabled${NC}"
    fi

    # Check for Telnet
    if echo "$content" | grep -qE "transport input.*telnet"; then
        echo -e "${YELLOW}    ⚠  Warning: Telnet is insecure, use SSH only${NC}"
    fi

    # Check for HTTP server
    if echo "$content" | grep -qE "^ip http server$"; then
        if ! echo "$content" | grep -q "ip http secure-server"; then
            echo -e "${YELLOW}    ⚠  Warning: HTTP without HTTPS (consider 'no ip http server')${NC}"
        fi
    fi
}

# Function: Check for common mistakes
validate_common_mistakes() {
    local file=$1
    echo "  🔍 Checking for common mistakes in $file..."

    local staged_content=$(git show ":$file")

    # Check for "shutdown" on trunk ports (common mistake)
    if echo "$staged_content" | grep -A5 "switchport mode trunk" | grep -q "^\s*shutdown"; then
        echo -e "${YELLOW}    ⚠  Warning: Trunk port appears to be shutdown${NC}"
    fi

    # Check for mismatched VLAN on voice+data ports
    local voice_vlan=$(echo "$staged_content" | grep -oP "(?<=switchport voice vlan )\d+")
    local access_vlan=$(echo "$staged_content" | grep -oP "(?<=switchport access vlan )\d+")

    if [ ! -z "$voice_vlan" ] && [ ! -z "$access_vlan" ]; then
        if [ "$voice_vlan" = "$access_vlan" ]; then
            echo -e "${RED}    ✗ Voice VLAN and access VLAN are the same!${NC}"
            ((ERRORS++))
        fi
    fi
}

# Run validations on each file
for file in $STAGED_CONFIGS; do
    echo ""
    echo "  Validating: $file"
    echo "  ────────────────────────────"

    validate_vlans "$file"
    validate_ip_addresses "$file"
    validate_required_commands "$file"
    validate_security "$file"
    validate_common_mistakes "$file"
done

echo ""
echo "═══════════════════════════════════════"

# Summary
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ Validation passed!${NC}"
    echo -e "  All checks completed successfully."
    echo ""
    exit 0
else
    echo -e "${RED}✗ Validation failed with $ERRORS error(s)${NC}"
    echo -e "${YELLOW}  Fix the errors above and try again.${NC}"
    echo -e "${YELLOW}  To bypass (not recommended): git commit --no-verify${NC}"
    echo ""
    exit 1
fi
```

Make executable:

```bash
chmod +x .git/hooks/pre-commit
```

### Test Advanced Validation

```bash
# Create config with errors
cat > configs/TEST-SW-01.cfg << 'EOF'
! Missing hostname

vlan 10
 name DATA
vlan 5000
 name INVALID
!
interface GigabitEthernet0/1
 ip address 192.168.300.1 255.255.255.0
 switchport mode trunk
 shutdown
!
end
EOF

git add configs/TEST-SW-01.cfg
git commit -m "Test config"
```

**Output:**
```
🔍 Running configuration validation...

  Validating: configs/TEST-SW-01.cfg
  ────────────────────────────────
  🏷️  Validating VLAN IDs in configs/TEST-SW-01.cfg...
    ✗ Invalid VLAN ID: 5000 (must be 1-4094)
  🌐 Validating IP addresses in configs/TEST-SW-01.cfg...
    ✗ Invalid IP address: 192.168.300.1
  📋 Checking required commands in configs/TEST-SW-01.cfg...
    ✗ Missing required command: hostname
  🔐 Checking security settings in configs/TEST-SW-01.cfg...
  🔍 Checking for common mistakes in configs/TEST-SW-01.cfg...
    ⚠  Warning: Trunk port appears to be shutdown

═══════════════════════════════════════
✗ Validation failed with 3 error(s)
  Fix the errors above and try again.
  To bypass (not recommended): git commit --no-verify
```

**Commit blocked!** Fixed 3 errors automatically!

## 📨 Part 5: Commit Message Validation

### Hook: commit-msg

Create `.git/hooks/commit-msg`:

```bash
#!/bin/bash
# Validate commit message format

COMMIT_MSG_FILE=$1
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "📝 Validating commit message..."

# Check minimum length
if [ ${#COMMIT_MSG} -lt 10 ]; then
    echo -e "${RED}✗ Commit message too short (minimum 10 characters)${NC}"
    echo -e "${YELLOW}  Write a meaningful commit message describing the change${NC}"
    exit 1
fi

# Check for ticket reference (optional)
if ! echo "$COMMIT_MSG" | grep -qE "(CHG|INC|JIRA|#)[0-9]+"; then
    echo -e "${YELLOW}⚠  Warning: No ticket reference found${NC}"
    echo -e "${YELLOW}  Consider adding CHG/INC number for tracking${NC}"
    # Warning only, don't block
fi

# Prevent "WIP" or "TODO" in commit messages
if echo "$COMMIT_MSG" | grep -qiE "^(WIP|TODO|FIXME)"; then
    echo -e "${RED}✗ Commit message starts with WIP/TODO/FIXME${NC}"
    echo -e "${YELLOW}  Write a proper commit message before committing${NC}"
    exit 1
fi

echo -e "✓ Commit message format OK"
exit 0
```

Make executable:

```bash
chmod +x .git/hooks/commit-msg
```

### Test Message Validation

```bash
# Try short message
git commit -m "fix"
```

**Output:**
```
📝 Validating commit message...
✗ Commit message too short (minimum 10 characters)
  Write a meaningful commit message describing the change
```

```bash
# Try WIP message
git commit -m "WIP: testing something"
```

**Output:**
```
📝 Validating commit message...
✗ Commit message starts with WIP/TODO/FIXME
  Write a proper commit message before committing
```

```bash
# Good message
git commit -m "Add VLAN 50 for production servers - CHG0012345"
```

**Output:**
```
📝 Validating commit message...
✓ Commit message format OK
[main a1b2c3d] Add VLAN 50 for production servers - CHG0012345
```

## 🚀 Part 6: Pre-Push Hook

### Prevent Pushing to Main

Create `.git/hooks/pre-push`:

```bash
#!/bin/bash
# Pre-push hook: Prevent direct pushes to main branch

CURRENT_BRANCH=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')

if [ "$CURRENT_BRANCH" = "main" ] || [ "$CURRENT_BRANCH" = "master" ]; then
    echo ""
    echo "❌ Direct push to $CURRENT_BRANCH is not allowed!"
    echo ""
    echo "Please:"
    echo "  1. Create a feature branch"
    echo "  2. Push your feature branch"
    echo "  3. Create a pull request"
    echo ""
    echo "To bypass (only if you know what you're doing):"
    echo "  git push --no-verify"
    echo ""
    exit 1
fi

echo "✓ Pushing to $CURRENT_BRANCH"
exit 0
```

Make executable:

```bash
chmod +x .git/hooks/pre-push
```

### Test Pre-Push Hook

```bash
# Try to push to main
git checkout main
git push
```

**Output:**
```
❌ Direct push to main is not allowed!

Please:
  1. Create a feature branch
  2. Push your feature branch
  3. Create a pull request

To bypass (only if you know what you're doing):
  git push --no-verify
```

**Push blocked!** ✓

```bash
# Create feature branch
git checkout -b feature/my-change
git push -u origin feature/my-change
```

**Output:**
```
✓ Pushing to feature/my-change
[Push proceeds normally]
```

## 📤 Part 7: Sharing Hooks with Team

### Problem: Hooks Don't Sync

Git doesn't sync hooks (they're in `.git/hooks/`, which is not tracked).

### Solution 1: Hooks Directory

```bash
cd ~/network-configs

# Create tracked hooks directory
mkdir -p scripts/git-hooks

# Move hooks there
cp .git/hooks/pre-commit scripts/git-hooks/
cp .git/hooks/commit-msg scripts/git-hooks/
cp .git/hooks/pre-push scripts/git-hooks/

# Add to Git
git add scripts/git-hooks/
git commit -m "Add shared Git hooks"
git push
```

Create setup script `scripts/setup-hooks.sh`:

```bash
#!/bin/bash
# Setup Git hooks for this repository

echo "Setting up Git hooks..."

HOOKS_DIR="$(git rev-parse --show-toplevel)/scripts/git-hooks"
GIT_HOOKS_DIR="$(git rev-parse --show-toplevel)/.git/hooks"

# Copy hooks
for hook in "$HOOKS_DIR"/*; do
    hook_name=$(basename "$hook")
    echo "  Installing $hook_name..."
    cp "$hook" "$GIT_HOOKS_DIR/$hook_name"
    chmod +x "$GIT_HOOKS_DIR/$hook_name"
done

echo "✓ Hooks installed successfully!"
echo ""
echo "Installed hooks:"
ls -1 "$GIT_HOOKS_DIR" | grep -v ".sample"
```

**Team members run:**
```bash
git clone <repository>
cd <repository>
./scripts/setup-hooks.sh
```

### Solution 2: Git Config

```bash
# Set hooks directory (Git 2.9+)
git config core.hooksPath scripts/git-hooks

# Now Git uses scripts/git-hooks/ instead of .git/hooks/
```

Add to `.gitconfig` or document in README.

## 🧪 Practice Exercises

### Exercise 1: Create Password Hook

```bash
# Create the pre-commit hook from Part 3
cd ~/network-configs
# Create .git/hooks/pre-commit with password checking

# Test it
echo "username admin password cisco" >> configs/test.cfg
git add configs/test.cfg
git commit -m "Test"

# Should be blocked
```

### Exercise 2: Add Custom Validation

```bash
# Enhance pre-commit hook to check for:
# - "no shutdown" on important interfaces
# - Logging configuration present
# - NTP servers configured

# Test with configs missing these
```

### Exercise 3: Commit Message Template

```bash
# Create commit message template
cat > .gitmessage << 'EOF'
# <type>: <subject>
#
# <body>
#
# Change-ID: CHG#
#
# Types: feat, fix, docs, style, refactor, test, chore
EOF

git config commit.template .gitmessage

# Now every commit opens with template
```

### Exercise 4: Share Hooks

```bash
# Set up shared hooks directory
mkdir scripts/git-hooks
cp .git/hooks/pre-commit scripts/git-hooks/
git add scripts/
git commit -m "Add shared hooks"
git push

# Create setup script
# Test that new clones can install hooks
```

## 📊 Commands Reference

```bash
# Hook locations
.git/hooks/pre-commit           # Before commit
.git/hooks/commit-msg            # Validate commit message
.git/hooks/pre-push              # Before push
.git/hooks/post-commit           # After commit

# Make hook executable
chmod +x .git/hooks/pre-commit

# Bypass hooks (use sparingly!)
git commit --no-verify
git push --no-verify

# Configure hooks directory
git config core.hooksPath scripts/hooks

# View current hooks
ls -la .git/hooks/

# Test hook without committing
.git/hooks/pre-commit
```

## ✅ Verification Checklist

Make sure you can:

- [ ] Create a pre-commit hook
- [ ] Make hooks executable
- [ ] Validate configurations automatically
- [ ] Block commits with security issues
- [ ] Validate commit messages
- [ ] Create pre-push hooks
- [ ] Share hooks with team
- [ ] Bypass hooks when needed

## ❓ Common Issues

### Issue: Hook doesn't run

**Check:**
```bash
# Is it executable?
ls -l .git/hooks/pre-commit

# If not:
chmod +x .git/hooks/pre-commit
```

### Issue: Hook has wrong name

```bash
# Must match exactly (no extension)
.git/hooks/pre-commit     # ✓ Correct
.git/hooks/pre-commit.sh  # ✗ Won't run
.git/hooks/pre-commit.sample  # ✗ Won't run
```

### Issue: Hook syntax error

```bash
# Test hook directly
bash -x .git/hooks/pre-commit

# Or
.git/hooks/pre-commit

# Fix syntax errors
```

### Issue: Shared hooks not working

```bash
# Verify hooks path
git config core.hooksPath

# Set it if needed
git config core.hooksPath scripts/git-hooks

# Ensure hooks are executable
chmod +x scripts/git-hooks/*
```

## 🎯 Best Practices

### Hook Design

✅ **DO:**
- Provide clear error messages
- Use colors for visibility
- Exit with proper codes (0=success, 1=failure)
- Make checks fast (hooks run on every commit)
- Document what hook does
- Provide bypass instructions

❌ **DON'T:**
- Make hooks too strict (frustrates team)
- Slow down every commit with heavy checks
- Forget to make hooks executable
- Hide error messages

### Security Checks

**Check for:**
- Default passwords
- Weak passwords
- Public SNMP communities
- Telnet enabled
- HTTP without HTTPS
- Hard-coded credentials

### Validation Priority

**Errors (block commit):**
- Security issues
- Invalid syntax
- Missing required fields

**Warnings (allow but warn):**
- Style inconsistencies
- Missing documentation
- Suboptimal configurations

## 🎉 Lesson Complete!

You've learned:
✅ Git hooks fundamentals
✅ Creating validation hooks
✅ Security checking automation
✅ Commit message validation
✅ Pre-push protections
✅ Sharing hooks with teams

### Next Steps

**Ready for Lesson 4?** → [Complete Workflow](04-complete-workflow.md)

Learn how to:
- Combine all techniques
- Implement end-to-end change workflow
- Create pre/post upgrade snapshots
- Build production-ready processes

**Or practice more:**
- Add more validation rules
- Create custom hooks for your environment
- Set up hooks for your team
- Integrate with CI/CD

---

**Lesson Duration:** 20 minutes
**Difficulty:** Intermediate → Advanced
**Next:** Complete production workflows
