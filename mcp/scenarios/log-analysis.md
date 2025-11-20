# Real-World Scenario: Network Log Analysis with MCP

## Scenario Overview

You're managing network devices and need to analyze logs efficiently. By creating a custom MCP tool that reads log files, you can use AI to find patterns, identify issues, and summarize findings.

**Prerequisites:** Complete the main [MCP Lab](../README.md) setup first.

---

## Learning Objectives

- Extend your MCP server with file-reading capabilities
- Use AI to analyze network logs
- Identify patterns and anomalies
- Generate actionable reports

---

## The Challenge

Network devices generate massive amounts of log data. Manually reviewing logs is time-consuming. With MCP, you can:
- Let AI search for specific events
- Identify patterns across multiple log entries
- Correlate events
- Generate summaries

---

## Part 1: Create Sample Network Logs

First, let's create realistic network device logs to work with.

### Create Log Files

```bash
# Create logs directory
mkdir -p ~/mcp-lab/logs

# Create a router log
cat > ~/mcp-lab/logs/router01.log << 'EOF'
2025-01-15 08:15:23 INFO: Interface GigabitEthernet0/0 up
2025-01-15 08:15:24 INFO: BGP neighbor 192.168.1.1 established
2025-01-15 09:30:45 WARNING: High CPU utilization (85%)
2025-01-15 09:31:12 WARNING: High CPU utilization (87%)
2025-01-15 09:45:00 INFO: CPU utilization normal (45%)
2025-01-15 10:15:33 ERROR: Interface GigabitEthernet0/1 down
2025-01-15 10:15:35 WARNING: BGP neighbor 192.168.1.2 connection lost
2025-01-15 10:16:00 INFO: Interface GigabitEthernet0/1 up
2025-01-15 10:16:05 INFO: BGP neighbor 192.168.1.2 established
2025-01-15 11:22:18 WARNING: OSPF adjacency timeout with 10.0.0.5
2025-01-15 11:22:45 INFO: OSPF adjacency formed with 10.0.0.5
2025-01-15 12:30:00 INFO: Configuration saved
2025-01-15 13:45:22 ERROR: Authentication failure for user 'admin' from 172.16.0.50
2025-01-15 13:45:30 ERROR: Authentication failure for user 'admin' from 172.16.0.50
2025-01-15 13:45:38 ERROR: Authentication failure for user 'admin' from 172.16.0.50
2025-01-15 13:46:00 CRITICAL: Account 'admin' locked due to multiple failed attempts
2025-01-15 14:00:00 INFO: System health check: OK
2025-01-15 15:30:15 WARNING: Memory utilization high (78%)
2025-01-15 16:00:00 INFO: Daily backup completed successfully
EOF

# Create a firewall log
cat > ~/mcp-lab/logs/firewall01.log << 'EOF'
2025-01-15 08:00:00 INFO: Firewall started
2025-01-15 08:00:05 INFO: Loading ruleset version 2.4.1
2025-01-15 09:15:22 DENY: TCP 203.0.113.50:45678 -> 192.168.1.100:22 (SSH brute force attempt)
2025-01-15 09:15:23 DENY: TCP 203.0.113.50:45679 -> 192.168.1.100:22 (SSH brute force attempt)
2025-01-15 09:15:24 DENY: TCP 203.0.113.50:45680 -> 192.168.1.100:22 (SSH brute force attempt)
2025-01-15 09:15:25 DENY: TCP 203.0.113.50:45681 -> 192.168.1.100:22 (SSH brute force attempt)
2025-01-15 09:15:30 INFO: Added 203.0.113.50 to blocklist
2025-01-15 10:30:45 ALLOW: TCP 192.168.1.50:54321 -> 8.8.8.8:443 (HTTPS)
2025-01-15 10:30:46 ALLOW: TCP 192.168.1.51:54322 -> 1.1.1.1:443 (HTTPS)
2025-01-15 11:00:00 INFO: Connection table: 1,234 active connections
2025-01-15 12:15:33 DENY: UDP 198.51.100.20:53 -> 192.168.1.100:53 (DNS amplification)
2025-01-15 12:15:34 DENY: UDP 198.51.100.21:53 -> 192.168.1.100:53 (DNS amplification)
2025-01-15 12:15:35 DENY: UDP 198.51.100.22:53 -> 192.168.1.100:53 (DNS amplification)
2025-01-15 12:16:00 CRITICAL: Possible DDoS attack detected from subnet 198.51.100.0/24
2025-01-15 12:16:05 INFO: Rate limiting applied to 198.51.100.0/24
2025-01-15 14:00:00 INFO: Hourly statistics: 45,678 packets processed, 234 blocked
2025-01-15 15:45:10 WARNING: Rule 'ALLOW_HTTP' matched 10,000 times in last hour
2025-01-15 16:00:00 INFO: Daily log rotation completed
EOF

# Create a switch log
cat > ~/mcp-lab/logs/switch01.log << 'EOF'
2025-01-15 08:00:00 INFO: Switch startup complete
2025-01-15 08:00:05 INFO: Spanning Tree Protocol: Root bridge elected
2025-01-15 08:15:20 INFO: Port Fa0/1: Link up, 1000Mbps full-duplex
2025-01-15 08:15:21 INFO: Port Fa0/2: Link up, 1000Mbps full-duplex
2025-01-15 09:30:15 WARNING: Port Fa0/10: Excessive CRC errors (1,234 in last minute)
2025-01-15 09:30:45 WARNING: Port Fa0/10: Possible cable issue detected
2025-01-15 10:00:00 ERROR: Port Fa0/10: Link down
2025-01-15 10:05:00 INFO: Port Fa0/10: Link up, 100Mbps half-duplex (degraded)
2025-01-15 11:15:30 WARNING: MAC address table 80% full (8,192 entries)
2025-01-15 12:00:00 INFO: VLAN 10: 45 active hosts
2025-01-15 12:00:01 INFO: VLAN 20: 78 active hosts
2025-01-15 13:30:00 WARNING: Port Fa0/15: Security violation (max MAC addresses exceeded)
2025-01-15 13:30:05 INFO: Port Fa0/15: Disabled due to security policy
2025-01-15 14:00:00 INFO: DHCP Snooping: 234 bindings
2025-01-15 15:00:00 INFO: Port Fa0/24: LACP channel-group formed
2025-01-15 16:00:00 INFO: Configuration auto-save completed
EOF
```

---

## Part 2: Add Log Analysis Tool to MCP Server

Now extend your MCP server with log reading capabilities.

### Update network_tools.py

Add this new tool to your existing [~/mcp-lab/tools/network_tools.py](../tools/network_tools.py):

```python
import os

@mcp.tool()
def read_log_file(filename: str, search_term: str = "", lines: int = 0) -> str:
    """
    Read and search network device log files.

    Args:
        filename: Name of the log file (e.g., 'router01.log', 'firewall01.log', 'switch01.log')
        search_term: Optional search term to filter log entries (case-insensitive)
        lines: Optional limit on number of lines to return (0 = all lines)

    Returns:
        Log file contents, optionally filtered by search term
    """
    try:
        # Base log directory
        log_dir = os.path.expanduser("~/mcp-lab/logs")
        log_path = os.path.join(log_dir, filename)

        # Security check: ensure file is within log directory
        real_log_path = os.path.realpath(log_path)
        real_log_dir = os.path.realpath(log_dir)
        if not real_log_path.startswith(real_log_dir):
            return f"✗ Security error: Access denied to {filename}"

        # Check if file exists
        if not os.path.exists(real_log_path):
            available = os.listdir(log_dir)
            return f"✗ File not found: {filename}\n\nAvailable logs:\n" + "\n".join(f"  - {f}" for f in available)

        # Read file
        with open(real_log_path, 'r') as f:
            log_lines = f.readlines()

        # Filter by search term if provided
        if search_term:
            search_lower = search_term.lower()
            log_lines = [line for line in log_lines if search_lower in line.lower()]

        # Limit lines if specified
        if lines > 0:
            log_lines = log_lines[:lines]

        # Format output
        result = f"Log file: {filename}\n"
        if search_term:
            result += f"Filtered by: '{search_term}'\n"
        result += f"Entries: {len(log_lines)}\n"
        result += "-" * 60 + "\n"
        result += "".join(log_lines)

        return result

    except Exception as e:
        return f"✗ Error reading log file: {str(e)}"
```

**Save the updated file and restart your MCP server:**

```bash
# Test the updated server
cd ~/mcp-lab/tools
source ~/mcp-lab/venv/bin/activate
python3 network_tools.py
# Should now show 4 tools including read_log_file
```

---

## Part 3: Analyze Logs with AI

Now use your AI assistant to analyze the logs.

### Exercise 1: Find Critical Events

**Prompt:**
```
Read the router01.log file and show me all ERROR and CRITICAL level messages.
What issues should I be concerned about?
```

**Expected AI behavior:**
- Uses `read_log_file` with search term "ERROR" or "CRITICAL"
- Identifies authentication failures and account lockout
- Highlights interface down event
- Summarizes security concern

### Exercise 2: Investigate Security Incident

**Prompt:**
```
Someone reported suspicious authentication attempts around 13:45.
Can you check router01.log for authentication-related events and
summarize what happened?
```

**Expected AI behavior:**
- Searches for "authentication"
- Identifies the pattern of failed attempts
- Notes the account lockout
- Suggests this is a brute-force attempt

### Exercise 3: Correlate Across Multiple Devices

**Prompt:**
```
I see an interface went down on router01 around 10:15.
Can you check if there are any related events in the other log files
around that time? Maybe the switch or firewall noticed something?
```

**Expected AI behavior:**
- Reads multiple log files
- Searches for events around 10:15
- Correlates timing
- Provides unified timeline

### Exercise 4: Identify Attack Patterns

**Prompt:**
```
Review the firewall01.log and identify any security threats or attacks.
What types of attacks were detected and how were they handled?
```

**Expected AI behavior:**
- Identifies SSH brute force attempt
- Identifies DNS amplification / DDoS attack
- Notes the firewall's response (blocklisting, rate limiting)
- Summarizes threat landscape

### Exercise 5: Hardware Issues

**Prompt:**
```
Are there any hardware or physical layer issues in switch01.log?
Look for errors, degraded performance, or unusual behavior.
```

**Expected AI behavior:**
- Finds CRC errors on port Fa0/10
- Identifies link degradation (full-duplex to half-duplex)
- Notes security violation on Fa0/15
- Suggests cable issues on Fa0/10

### Exercise 6: Generate Daily Summary

**Prompt:**
```
Generate a daily summary report for all three network devices.
Include:
- Critical issues that need immediate attention
- Warnings that should be monitored
- Notable events
- Overall system health
```

**Expected AI behavior:**
- Reads all three log files
- Categorizes issues by severity
- Provides prioritized action items
- Formats as a readable report

---

## Part 4: Advanced Analysis

### Pattern Detection

**Prompt:**
```
Analyze router01.log for any patterns or recurring issues.
Are there any problems that keep happening?
```

**Look for:**
- Repeated warnings (CPU, memory)
- Flapping interfaces
- Protocol instability

### Timeline Reconstruction

**Prompt:**
```
Create a timeline of all events across all devices between 12:00 and 13:00.
Sort chronologically and highlight any correlations.
```

### Capacity Planning

**Prompt:**
```
Based on the logs, are there any capacity or resource concerns?
Look at CPU, memory, connection tables, MAC address tables, etc.
```

---

## Part 5: Create Custom Log Analysis Workflows

### Workflow 1: Security Audit

Create a comprehensive security check:

**Prompt:**
```
Perform a security audit of all log files. Look for:
1. Authentication failures
2. Blocked connection attempts
3. Security violations
4. Unusual access patterns
5. Account lockouts

Prioritize findings by risk level.
```

### Workflow 2: Performance Review

**Prompt:**
```
Analyze all logs for performance indicators:
- CPU/Memory utilization warnings
- Link degradation
- Connection table usage
- Any timeouts or delays

Identify bottlenecks or capacity issues.
```

### Workflow 3: Change Impact Analysis

**Prompt:**
```
A configuration change was made around 12:00.
Review logs from 11:45 to 12:15 across all devices
to identify any impact or issues from the change.
```

---

## Real-World Applications

### 1. Automated Daily Reports

Set up a daily prompt to generate reports:
```
Review yesterday's logs and send me:
- Top 3 issues requiring attention
- Security summary
- Performance metrics
- Any anomalies detected
```

### 2. Incident Response

During an outage:
```
We lost connectivity at 14:30. Search all logs around
that time (14:20-14:40) and help me identify the root cause.
```

### 3. Compliance Auditing

For regulatory requirements:
```
Extract all authentication events from the past week.
I need a report showing who accessed what and when
for our compliance audit.
```

### 4. Proactive Monitoring

Before issues escalate:
```
Check today's logs for any warning signs of potential
problems: degraded performance, repeated errors, or
concerning patterns that might lead to bigger issues.
```

---

## Key Insights

### What You Learned

1. **Extend MCP Tools** - Adding new capabilities is straightforward
2. **AI Pattern Recognition** - AI excels at finding patterns in logs
3. **Natural Language Queries** - No need to remember grep syntax
4. **Cross-Device Correlation** - AI can correlate events across multiple sources
5. **Contextual Analysis** - AI understands network context and severity

### MCP Advantages for Log Analysis

**Traditional approach:**
```bash
grep -i error router01.log
grep -i error firewall01.log
grep -i error switch01.log
# Manual correlation and analysis
```

**With MCP:**
```
Show me all errors across all devices and explain their
relationship to each other
```

The AI:
- Searches all files automatically
- Understands context and relationships
- Provides analysis, not just raw data
- Suggests actions based on findings

---

## Extension Ideas

### Add More Log Sources
- Syslog server logs
- Application logs
- SNMP trap logs
- NetFlow/sFlow analysis

### Enhance the Tool
Add features like:
- Date range filtering
- Regex pattern matching
- Log aggregation across multiple files
- Export findings to CSV/JSON

### Automate Analysis
- Schedule periodic checks
- Alert on critical patterns
- Generate automatic reports
- Track trends over time

---

## Next Steps

- Try [Automated Documentation Lab](automated-docs.md)
- Challenge yourself with [Extension Challenges](challenges.md)
- Build your own custom log analysis tools

---

**Questions or Issues?** See the [Troubleshooting Guide](../TROUBLESHOOTING.md)
