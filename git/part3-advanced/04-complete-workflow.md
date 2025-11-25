# Lesson 4: Complete Network Change Workflow

Combine all Git techniques into a comprehensive, production-ready network change management workflow.

## 🎯 Objectives

By the end of this lesson, you'll be able to:
- Implement end-to-end change management with Git
- Create pre/post upgrade snapshots
- Compare configurations before and after changes
- Build rollback procedures
- Integrate Git with change tickets
- Document changes automatically
- Create a repeatable workflow for your team

## 📝 What You'll Learn

- Complete change workflow pattern
- Pre/post maintenance snapshots
- Configuration comparison
- Rollback procedures
- Change documentation
- Team integration

## 🔄 Part 1: The Complete Workflow

### Overview

```
Change Request → Planning → Pre-Snapshot → Implementation →
Post-Snapshot → Validation → Documentation → Review
```

### Workflow Steps

**1. Change Planning**
- Create change ticket (CHG00123456)
- Define scope and impact
- Schedule maintenance window

**2. Pre-Change Snapshot**
- Backup all affected device configs
- Create snapshot branch
- Commit with timestamp

**3. Implementation**
- Apply changes to devices
- Test functionality
- Document issues

**4. Post-Change Snapshot**
- Backup configs again
- Create post-snapshot branch
- Commit with timestamp

**5. Validation**
- Compare pre/post configs
- Verify changes applied correctly
- Check for unexpected changes

**6. Documentation**
- Generate change report
- Update change ticket
- Archive for audit

**7. Rollback (if needed)**
- Restore from pre-snapshot
- Test rollback procedure
- Document lessons learned

## 📸 Part 2: Pre/Post Upgrade Snapshots

### Snapshot Script

Create `scripts/snapshot.py`:

```python
#!/usr/bin/env python3
"""
Pre/Post maintenance snapshot tool
Creates timestamped Git branches with device configurations
"""

import sys
import subprocess
from datetime import datetime
import argparse

class SnapshotTool:
    def __init__(self, snapshot_type, change_id=None, description=None):
        self.snapshot_type = snapshot_type  # 'pre' or 'post'
        self.change_id = change_id
        self.description = description
        self.timestamp = datetime.now().strftime('%Y%m%d-%H%M')
        self.branch_name = None

    def run_command(self, command, check=True):
        """Run shell command and return output"""
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=check
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {' '.join(command)}")
            print(f"Error: {e.stderr}")
            sys.exit(1)

    def create_branch_name(self):
        """Generate snapshot branch name"""
        base = f"{self.snapshot_type}-{self.timestamp}"

        if self.change_id:
            self.branch_name = f"{base}-{self.change_id}"
        else:
            self.branch_name = base

        return self.branch_name

    def ensure_clean_state(self):
        """Ensure working directory is clean"""
        status = self.run_command(['git', 'status', '--porcelain'])

        if status:
            print("⚠️  Warning: Uncommitted changes detected:")
            print(status)
            print("\nCommit or stash changes before creating snapshot.")

            response = input("\nContinue anyway? (y/N): ")
            if response.lower() != 'y':
                print("Snapshot cancelled.")
                sys.exit(0)

    def backup_configs(self):
        """Run backup script to get latest configs"""
        print("\n📡 Backing up device configurations...")

        # Check if backup script exists
        try:
            self.run_command(['python3', 'backup_configs.py'])
            print("✓ Configurations backed up successfully")
        except:
            print("⚠️  Warning: Could not run backup_configs.py")
            print("   Continuing with existing configurations...")

    def create_snapshot_branch(self):
        """Create and checkout snapshot branch"""
        print(f"\n🌿 Creating snapshot branch: {self.branch_name}")

        self.run_command(['git', 'checkout', '-b', self.branch_name])
        print(f"✓ Switched to branch '{self.branch_name}'")

    def commit_snapshot(self):
        """Commit snapshot"""
        print("\n📝 Committing snapshot...")

        # Create detailed commit message
        timestamp_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        message_parts = [
            f"{self.snapshot_type.upper()} snapshot - {timestamp_str}"
        ]

        if self.change_id:
            message_parts.append(f"\nChange ID: {self.change_id}")

        if self.description:
            message_parts.append(f"\n{self.description}")

        message_parts.append(f"\nSnapshot branch: {self.branch_name}")

        commit_message = "\n".join(message_parts)

        # Stage all config changes
        self.run_command(['git', 'add', 'configs/'])

        # Check if there are changes to commit
        status = self.run_command(['git', 'status', '--porcelain'])

        if not status:
            print("○ No configuration changes to commit")
        else:
            self.run_command(['git', 'commit', '-m', commit_message])
            print("✓ Snapshot committed")

    def push_snapshot(self):
        """Push snapshot branch to remote"""
        print("\n📤 Pushing snapshot to remote...")

        self.run_command(['git', 'push', '-u', 'origin', self.branch_name])
        print(f"✓ Snapshot pushed to origin/{self.branch_name}")

    def display_summary(self):
        """Display snapshot summary"""
        print("\n" + "="*60)
        print("SNAPSHOT COMPLETE")
        print("="*60)
        print(f"Type: {self.snapshot_type.upper()}")
        print(f"Branch: {self.branch_name}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        if self.change_id:
            print(f"Change ID: {self.change_id}")

        print("\nNext steps:")

        if self.snapshot_type == 'pre':
            print("  1. Perform your maintenance/changes")
            print("  2. Run post-snapshot:")
            if self.change_id:
                print(f"     python3 scripts/snapshot.py post --change-id {self.change_id}")
            else:
                print(f"     python3 scripts/snapshot.py post")
            print("  3. Compare snapshots:")
            print(f"     git diff {self.branch_name} <post-branch-name>")
        else:
            print("  1. Review changes:")
            print(f"     git log {self.branch_name}")
            print("  2. Compare with pre-snapshot:")
            print(f"     git diff <pre-branch-name> {self.branch_name}")
            print("  3. Return to main:")
            print("     git checkout main")

        print("="*60)

    def run(self):
        """Execute snapshot workflow"""
        print("="*60)
        print(f"CREATING {self.snapshot_type.upper()} SNAPSHOT")
        print("="*60)

        # Generate branch name
        self.create_branch_name()

        # Check working directory state
        self.ensure_clean_state()

        # Backup configurations
        self.backup_configs()

        # Create snapshot branch
        self.create_snapshot_branch()

        # Commit snapshot
        self.commit_snapshot()

        # Push to remote
        try:
            self.push_snapshot()
        except:
            print("⚠️  Could not push to remote (check connection)")

        # Display summary
        self.display_summary()


def main():
    parser = argparse.ArgumentParser(
        description='Create pre/post maintenance snapshots'
    )

    parser.add_argument(
        'snapshot_type',
        choices=['pre', 'post'],
        help='Type of snapshot (pre or post)'
    )

    parser.add_argument(
        '--change-id',
        help='Change ticket ID (e.g., CHG0012345)'
    )

    parser.add_argument(
        '--description',
        help='Description of the change'
    )

    args = parser.parse_args()

    snapshot = SnapshotTool(
        args.snapshot_type,
        args.change_id,
        args.description
    )

    snapshot.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSnapshot cancelled by user")
        sys.exit(1)
```

Make it executable:

```bash
chmod +x scripts/snapshot.py
```

### Using the Snapshot Tool

**Before maintenance:**

```bash
cd ~/network-configs

# Create pre-snapshot
python3 scripts/snapshot.py pre \
    --change-id CHG0012345 \
    --description "IOS upgrade from 15.2 to 15.7"
```

**Output:**
```
============================================================
CREATING PRE SNAPSHOT
============================================================

📡 Backing up device configurations...
✓ Configurations backed up successfully

🌿 Creating snapshot branch: pre-20240115-1430-CHG0012345
✓ Switched to branch 'pre-20240115-1430-CHG0012345'

📝 Committing snapshot...
✓ Snapshot committed

📤 Pushing snapshot to remote...
✓ Snapshot pushed to origin/pre-20240115-1430-CHG0012345

============================================================
SNAPSHOT COMPLETE
============================================================
Type: PRE
Branch: pre-20240115-1430-CHG0012345
Timestamp: 2024-01-15 14:30:00
Change ID: CHG0012345

Next steps:
  1. Perform your maintenance/changes
  2. Run post-snapshot:
     python3 scripts/snapshot.py post --change-id CHG0012345
  3. Compare snapshots:
     git diff pre-20240115-1430-CHG0012345 <post-branch-name>
============================================================
```

**After maintenance:**

```bash
# Perform maintenance...
# (upgrade IOS, apply configs, etc.)

# Create post-snapshot
python3 scripts/snapshot.py post \
    --change-id CHG0012345 \
    --description "Post-IOS upgrade verification"
```

## 📊 Part 3: Configuration Comparison

### Compare Pre/Post Snapshots

```bash
# List snapshot branches
git branch | grep -E "(pre|post)-"

# Output:
#   pre-20240115-1430-CHG0012345
#   post-20240115-1530-CHG0012345

# Compare snapshots
git diff pre-20240115-1430-CHG0012345 post-20240115-1530-CHG0012345
```

### Generate Change Report

Create `scripts/compare_snapshots.py`:

```python
#!/usr/bin/env python3
"""
Compare pre/post snapshots and generate change report
"""

import subprocess
import sys
import argparse
from datetime import datetime

def run_git_command(command):
    """Execute git command and return output"""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        sys.exit(1)

def get_changed_files(pre_branch, post_branch):
    """Get list of files that changed"""
    result = run_git_command([
        'git', 'diff', '--name-only',
        pre_branch, post_branch
    ])
    return [f for f in result.split('\n') if f]

def get_file_diff(pre_branch, post_branch, filename):
    """Get diff for specific file"""
    result = run_git_command([
        'git', 'diff',
        f'{pre_branch}:{filename}',
        f'{post_branch}:{filename}'
    ])
    return result

def generate_report(pre_branch, post_branch, output_file=None):
    """Generate comprehensive change report"""

    report = []
    report.append("="*70)
    report.append("NETWORK CONFIGURATION CHANGE REPORT")
    report.append("="*70)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Pre-snapshot:  {pre_branch}")
    report.append(f"Post-snapshot: {post_branch}")
    report.append("="*70)
    report.append("")

    # Get changed files
    changed_files = get_changed_files(pre_branch, post_branch)

    if not changed_files:
        report.append("No configuration changes detected.")
    else:
        report.append(f"Configuration Changes: {len(changed_files)} file(s)")
        report.append("")

        for filename in changed_files:
            report.append("-"*70)
            report.append(f"File: {filename}")
            report.append("-"*70)

            # Get diff
            diff = get_file_diff(pre_branch, post_branch, filename)

            # Parse diff to show changes
            added_lines = []
            removed_lines = []

            for line in diff.split('\n'):
                if line.startswith('+') and not line.startswith('+++'):
                    added_lines.append(line[1:])
                elif line.startswith('-') and not line.startswith('---'):
                    removed_lines.append(line[1:])

            if removed_lines:
                report.append("\nRemoved lines:")
                for line in removed_lines:
                    report.append(f"  - {line}")

            if added_lines:
                report.append("\nAdded lines:")
                for line in added_lines:
                    report.append(f"  + {line}")

            report.append("")

    report.append("="*70)
    report.append("END OF REPORT")
    report.append("="*70)

    # Output report
    report_text = '\n'.join(report)

    if output_file:
        with open(output_file, 'w') as f:
            f.write(report_text)
        print(f"✓ Report saved to: {output_file}")
    else:
        print(report_text)

def main():
    parser = argparse.ArgumentParser(
        description='Compare pre/post snapshots'
    )

    parser.add_argument('pre_branch', help='Pre-snapshot branch name')
    parser.add_argument('post_branch', help='Post-snapshot branch name')
    parser.add_argument('-o', '--output', help='Output file for report')

    args = parser.parse_args()

    generate_report(args.pre_branch, args.post_branch, args.output)

if __name__ == '__main__':
    main()
```

Make executable:

```bash
chmod +x scripts/compare_snapshots.py
```

### Generate Report

```bash
python3 scripts/compare_snapshots.py \
    pre-20240115-1430-CHG0012345 \
    post-20240115-1530-CHG0012345 \
    -o change-report-CHG0012345.txt
```

**Output file contains:**
```
======================================================================
NETWORK CONFIGURATION CHANGE REPORT
======================================================================
Generated: 2024-01-15 15:45:00
Pre-snapshot:  pre-20240115-1430-CHG0012345
Post-snapshot: post-20240115-1530-CHG0012345
======================================================================

Configuration Changes: 3 file(s)

----------------------------------------------------------------------
File: configs/SW-CORE-01.cfg
----------------------------------------------------------------------

Removed lines:
  - version 15.2

Added lines:
  + version 15.7
  + service timestamps debug datetime msec
  + service timestamps log datetime msec

----------------------------------------------------------------------
File: configs/SW-ACCESS-01.cfg
----------------------------------------------------------------------
...
```

## 🔙 Part 4: Rollback Procedures

### Quick Rollback Script

Create `scripts/rollback.py`:

```python
#!/usr/bin/env python3
"""
Rollback to previous configuration snapshot
"""

import subprocess
import sys
import argparse

def run_command(command):
    """Execute command"""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        sys.exit(1)

def get_snapshot_branches():
    """List available snapshot branches"""
    result = run_command(['git', 'branch', '-a'])
    branches = [
        b.strip().replace('* ', '')
        for b in result.split('\n')
        if 'pre-' in b or 'post-' in b
    ]
    return branches

def rollback(snapshot_branch):
    """Rollback configurations to snapshot"""

    print("="*60)
    print("CONFIGURATION ROLLBACK")
    print("="*60)
    print(f"Target snapshot: {snapshot_branch}")
    print("")

    # Confirm
    print("⚠️  WARNING: This will restore configurations to the snapshot state.")
    print("   Any changes made after the snapshot will be lost.")
    print("")

    response = input("Continue with rollback? (yes/NO): ")

    if response.lower() != 'yes':
        print("\nRollback cancelled.")
        sys.exit(0)

    print("\n📂 Extracting configurations from snapshot...")

    # Create rollback branch
    timestamp = subprocess.run(
        ['date', '+%Y%m%d-%H%M'],
        capture_output=True,
        text=True
    ).stdout.strip()

    rollback_branch = f"rollback-{timestamp}"

    run_command(['git', 'checkout', '-b', rollback_branch])
    print(f"✓ Created rollback branch: {rollback_branch}")

    # Restore configs from snapshot
    print(f"\n📋 Restoring configurations from {snapshot_branch}...")

    run_command([
        'git', 'checkout', snapshot_branch, '--', 'configs/'
    ])

    print("✓ Configurations restored")

    # Commit rollback
    print("\n📝 Committing rollback...")

    commit_msg = f"""Rollback to snapshot: {snapshot_branch}

Restored configurations to state at: {snapshot_branch}
Rollback performed at: {timestamp}
Rollback branch: {rollback_branch}
"""

    run_command(['git', 'add', 'configs/'])
    run_command(['git', 'commit', '-m', commit_msg])

    print("✓ Rollback committed")

    # Summary
    print("\n" + "="*60)
    print("ROLLBACK COMPLETE")
    print("="*60)
    print(f"Rollback branch: {rollback_branch}")
    print("")
    print("Next steps:")
    print("  1. Review restored configurations:")
    print("     git diff HEAD~1")
    print("  2. Deploy configurations to devices")
    print("  3. Verify operation")
    print("  4. Merge rollback to main if successful:")
    print("     git checkout main")
    print(f"     git merge {rollback_branch}")
    print("="*60)

def main():
    parser = argparse.ArgumentParser(
        description='Rollback to configuration snapshot'
    )

    parser.add_argument(
        'snapshot_branch',
        nargs='?',
        help='Snapshot branch to rollback to'
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='List available snapshots'
    )

    args = parser.parse_args()

    if args.list:
        print("\nAvailable snapshots:")
        branches = get_snapshot_branches()
        for branch in branches:
            print(f"  {branch}")
        print("")
        sys.exit(0)

    if not args.snapshot_branch:
        print("Error: Please specify a snapshot branch to rollback to")
        print("Use --list to see available snapshots")
        sys.exit(1)

    rollback(args.snapshot_branch)

if __name__ == '__main__':
    main()
```

Make executable:

```bash
chmod +x scripts/rollback.py
```

### Using Rollback

```bash
# List available snapshots
python3 scripts/rollback.py --list

# Rollback to specific snapshot
python3 scripts/rollback.py pre-20240115-1430-CHG0012345
```

## 📋 Part 5: Complete Workflow Example

### Full Change Lifecycle

**Step 1: Change Planning**

```bash
cd ~/network-configs

# Ensure main is up to date
git checkout main
git pull

# Document the change
CHANGE_ID="CHG0012345"
DESCRIPTION="Upgrade IOS from 15.2 to 15.7 on core switches"
```

**Step 2: Pre-Change Snapshot**

```bash
# Create pre-snapshot
python3 scripts/snapshot.py pre \
    --change-id $CHANGE_ID \
    --description "$DESCRIPTION"

# Verify snapshot created
git log -1
```

**Step 3: Perform Maintenance**

```bash
# (In real scenario, you'd connect to devices and upgrade IOS)
# For this example, simulate config changes

# Edit the config file
nano configs/SW-CORE-01.cfg
```

**Simulate the IOS upgrade changes:**

1. Find the line with the version (near the top):
```
version 15.2
```

2. Change it to:
```
version 15.7
```

3. Add these new features at the end of the file (before the `end` statement):
```
service timestamps debug datetime msec
service timestamps log datetime msec
```

**Save and exit** (nano: Ctrl+X, then Y, then Enter)

**Step 4: Post-Change Snapshot**

```bash
# Create post-snapshot
python3 scripts/snapshot.py post \
    --change-id $CHANGE_ID \
    --description "Post-upgrade verification - all systems operational"
```

**Step 5: Generate Change Report**

```bash
# Get branch names
PRE_BRANCH=$(git branch | grep "pre-.*$CHANGE_ID" | tr -d ' *')
POST_BRANCH=$(git branch | grep "post-.*$CHANGE_ID" | tr -d ' *')

# Generate report
python3 scripts/compare_snapshots.py \
    $PRE_BRANCH \
    $POST_BRANCH \
    -o "reports/change-report-$CHANGE_ID.txt"

# Review report
cat "reports/change-report-$CHANGE_ID.txt"
```

**Step 6: Verification**

```bash
# View exact changes
git diff $PRE_BRANCH $POST_BRANCH

# Check specific file
git diff $PRE_BRANCH:configs/SW-CORE-01.cfg \
         $POST_BRANCH:configs/SW-CORE-01.cfg
```

**Step 7: Merge to Main (If Successful)**

```bash
git checkout main
git merge $POST_BRANCH -m "Completed $CHANGE_ID: IOS upgrade successful"
git push
```

**Step 8: Cleanup**

```bash
# Delete local snapshot branches (keep remote for audit)
git branch -d $PRE_BRANCH
git branch -d $POST_BRANCH

# Or keep them for audit trail
# (recommended for compliance)
```

### If Rollback Needed

```bash
# Rollback to pre-snapshot
python3 scripts/rollback.py $PRE_BRANCH

# Review what would be restored
git diff HEAD~1

# Deploy restored configs to devices
# ...

# Merge rollback to main
git checkout main
git merge rollback-$(date +%Y%m%d-%H%M)
git push

# Document in change ticket
echo "Rollback performed due to [reason]" >> "reports/change-report-$CHANGE_ID.txt"
```

## 🧪 Practice Exercise: Complete Change

**Exercise: Complete maintenance workflow**

```bash
cd ~/network-configs

# 1. Plan change
CHANGE_ID="CHG0099999"
echo "Planned: Add VLANs 100-110 for new building"

# 2. Pre-snapshot
python3 scripts/snapshot.py pre --change-id $CHANGE_ID

# 3. Make changes
for vlan in {100..110}; do
    echo "vlan $vlan" >> configs/SW-CORE-01.cfg
    echo " name BUILDING-B-VLAN-$vlan" >> configs/SW-CORE-01.cfg
done

# 4. Post-snapshot
python3 scripts/snapshot.py post --change-id $CHANGE_ID

# 5. Generate report
PRE=$(git branch | grep "pre-.*$CHANGE_ID" | tr -d ' *')
POST=$(git branch | grep "post-.*$CHANGE_ID" | tr -d ' *')

mkdir -p reports
python3 scripts/compare_snapshots.py $PRE $POST \
    -o "reports/change-report-$CHANGE_ID.txt"

# 6. Review
cat "reports/change-report-$CHANGE_ID.txt"

# 7. Merge to main
git checkout main
git merge $POST -m "Completed $CHANGE_ID"

# 8. View history
git log --oneline --graph -10
```

## 📊 Commands Reference

```bash
# Snapshot workflow
python3 scripts/snapshot.py pre --change-id CHG123
python3 scripts/snapshot.py post --change-id CHG123

# Compare snapshots
git diff pre-branch post-branch
python3 scripts/compare_snapshots.py pre-branch post-branch -o report.txt

# Rollback
python3 scripts/rollback.py --list
python3 scripts/rollback.py pre-branch-name

# View snapshot branches
git branch | grep -E "(pre|post)-"

# Cleanup old snapshots
git branch -d snapshot-branch-name

# Archive to main
git checkout main
git merge post-branch
git push
```

## ✅ Verification Checklist

Make sure you can:

- [ ] Create pre-maintenance snapshot
- [ ] Perform changes
- [ ] Create post-maintenance snapshot
- [ ] Compare pre/post configurations
- [ ] Generate change report
- [ ] Rollback if needed
- [ ] Merge successful changes to main
- [ ] Document complete change process

## ❓ Common Issues

### Issue: Snapshot script fails

**Check:**
```bash
# Python version
python3 --version

# Git status
git status

# Backup script exists
ls -l backup_configs.py
```

### Issue: Can't find snapshot branches

**Solution:**
```bash
# Fetch all branches
git fetch --all

# List remote snapshot branches
git branch -r | grep -E "(pre|post)-"

# Checkout remote snapshot
git checkout -b pre-local origin/pre-remote-branch
```

### Issue: Merge conflicts after rollback

**Solution:**
```bash
# Abort merge
git merge --abort

# Use rollback script which creates new branch
python3 scripts/rollback.py pre-branch

# Review changes before merging
git diff main rollback-branch
```

## 🎯 Best Practices

### Change Management

✅ **DO:**
- Always create pre-snapshot before changes
- Document change ID in all snapshots
- Generate comparison reports
- Test rollback procedures
- Keep snapshots for audit (30-90 days)
- Archive completed changes to main

❌ **DON'T:**
- Skip pre-snapshots ("just a quick change")
- Delete snapshots immediately
- Make changes without change tickets
- Forget to create post-snapshot

### Documentation

✅ **DO:**
- Include change ticket references
- Describe what changed and why
- Note any issues encountered
- Document rollback procedures
- Archive reports for compliance

### Rollback Planning

✅ **DO:**
- Test rollback before maintenance
- Time-bound: decide rollback criteria
- Document rollback procedure
- Have rollback configs ready
- Practice rollback in lab

## 🎉 Lesson Complete!

You've learned:
✅ Complete network change workflow
✅ Pre/post maintenance snapshots
✅ Configuration comparison
✅ Rollback procedures
✅ Change documentation
✅ Production-ready processes

## 🎓 Part 3 Complete!

You've mastered advanced Git concepts:
✅ Automated configuration backups
✅ Interactive rebase for clean history
✅ Git hooks for validation
✅ Complete network change workflow

## 🏆 Lab Complete!

### What You've Accomplished

**Part 1: Single Developer Basics**
- Repository management
- Basic Git workflow
- Remote backups
- History navigation

**Part 2: Collaborative Development**
- Branching strategies
- Merging and conflicts
- Pull requests
- Team synchronization

**Part 3: Advanced Concepts**
- Automated backups
- History cleanup
- Validation hooks
- Professional workflows

### Next Steps

**Apply to Your Environment:**
1. Set up automated backups for your devices
2. Implement validation hooks
3. Create team change workflow
4. Integrate with change management system

**Integrate with Other Labs:**
- **Ansible Lab:** Version control playbooks
- **Python Lab:** Enhance automation scripts
- **Docker Lab:** Containerize backup tools

**Further Learning:**
- CI/CD integration (GitHub Actions, GitLab CI)
- Advanced Git techniques
- Configuration management at scale
- Infrastructure as Code

---

**Congratulations!** You now have professional Git skills for network automation!

**Lab Duration:** 5 hours total
**Skills Level:** Beginner → Advanced
**Real-world ready:** ✓

Keep practicing and applying these workflows to your daily network operations!
