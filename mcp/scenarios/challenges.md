# MCP Extension Challenges

Advanced exercises to deepen your MCP skills and build production-ready tools.

**Prerequisites:** Complete the main [MCP Lab](../README.md) and at least one scenario lab.

---

## Challenge Categories

- [Beginner Challenges](#beginner-challenges) - Enhance existing tools
- [Intermediate Challenges](#intermediate-challenges) - Build new capabilities
- [Advanced Challenges](#advanced-challenges) - Production-ready integrations
- [Expert Challenges](#expert-challenges) - Complex systems

---

## Beginner Challenges

### Challenge 1: Traceroute Tool

**Objective:** Add a traceroute tool to your MCP server.

**Requirements:**
- Tool name: `traceroute`
- Takes hostname as input
- Returns hop-by-hop path to destination
- Handles timeouts gracefully

**Hints:**
```python
@mcp.tool()
def traceroute(hostname: str, max_hops: int = 30) -> str:
    """Trace network path to a host"""
    # Use subprocess to run: traceroute -m <max_hops> <hostname>
    # Or on Windows: tracert -h <max_hops> <hostname>
    pass
```

**Test with:**
```
Can you trace the route to google.com and explain where the packets are going?
```

---

### Challenge 2: Batch Ping Tool

**Objective:** Create a tool that pings multiple hosts at once.

**Requirements:**
- Tool name: `ping_multiple`
- Takes a list of hostnames
- Pings all of them
- Returns summary of which are up/down

**Test with:**
```
Check if these hosts are reachable: google.com, github.com, amazon.com, microsoft.com
```

---

### Challenge 3: DNS Bulk Lookup

**Objective:** Enhance DNS tool to handle multiple records at once.

**Requirements:**
- Extend existing `dns_lookup` or create `dns_bulk_lookup`
- Query multiple record types for a domain
- Show comprehensive DNS profile

**Test with:**
```
Show me all DNS records for github.com (A, AAAA, MX, TXT, NS)
```

---

### Challenge 4: Network Calculator

**Objective:** Build a subnet calculator tool.

**Requirements:**
- Tool name: `subnet_calc`
- Input: CIDR notation (e.g., 192.168.1.0/24)
- Returns: network address, broadcast, usable IPs, subnet mask

**Python library to use:**
```python
import ipaddress
```

**Test with:**
```
Calculate subnet information for 10.0.0.0/8
```

---

### Challenge 5: Port Range Scanner

**Objective:** Extend port check to scan a range of ports.

**Requirements:**
- Tool name: `scan_ports`
- Input: hostname, start_port, end_port
- Returns: list of open ports
- Security: Limit range (e.g., max 100 ports)

**Test with:**
```
Scan common web ports (80-89) on example.com
```

---

## Intermediate Challenges

### Challenge 6: Log File Statistics

**Objective:** Create a tool that generates statistics from log files.

**Requirements:**
- Tool name: `log_stats`
- Count messages by severity level
- Identify most common errors
- Show time distribution of events

**Test with:**
```
Analyze router01.log and show me statistics about log levels and timing
```

---

### Challenge 7: Configuration Backup Tool

**Objective:** Simulate device configuration backup.

**Requirements:**
- Tool name: `backup_config`
- Takes device hostname
- "Backs up" config to a file with timestamp
- Returns confirmation and file location

**Enhancement:**
- Compare current config with previous backup
- Show what changed

**Test with:**
```
Back up the configuration for router01
```

---

### Challenge 8: IP Geolocation

**Objective:** Add geolocation lookup for IP addresses.

**Requirements:**
- Tool name: `geolocate_ip`
- Takes IP address
- Returns country, city, ISP (use free API like ip-api.com)
- Handle rate limits gracefully

**Python library:**
```python
import requests
```

**Test with:**
```
Where is this IP address located: 8.8.8.8
```

---

### Challenge 9: Network Speed Test

**Objective:** Create a bandwidth testing tool.

**Requirements:**
- Tool name: `speed_test`
- Measure download/upload speed
- Use speedtest-cli library or similar

**Installation:**
```bash
pip install speedtest-cli
```

**Test with:**
```
What's our current internet bandwidth?
```

---

### Challenge 10: SSL Certificate Checker

**Objective:** Check SSL certificate validity and details.

**Requirements:**
- Tool name: `check_ssl`
- Takes hostname and port (default 443)
- Returns: expiration date, issuer, valid/invalid
- Warn if expiring soon (< 30 days)

**Python library:**
```python
import ssl
import socket
from datetime import datetime
```

**Test with:**
```
Check the SSL certificate for github.com
```

---

## Advanced Challenges

### Challenge 11: SNMP Poller

**Objective:** Query network devices via SNMP.

**Requirements:**
- Tool name: `snmp_get`
- Takes hostname, community string, OID
- Returns SNMP value
- Handle SNMPv2c and SNMPv3

**Library:**
```bash
pip install pysnmp
```

**Test with:**
```
Get the system description from router01 via SNMP
```

---

### Challenge 12: Netmiko Integration

**Objective:** Connect to real network devices and run commands.

**Requirements:**
- Tool name: `device_command`
- Takes hostname, device type, command
- Uses Netmiko to connect
- Returns command output
- **Security:** Implement credential management

**Library:**
```bash
pip install netmiko
```

**Test with:**
```
Run 'show version' on router01
```

---

### Challenge 13: Packet Capture Analyzer

**Objective:** Analyze packet capture files.

**Requirements:**
- Tool name: `analyze_pcap`
- Takes path to .pcap file
- Uses scapy or similar
- Returns: protocol distribution, top talkers, suspicious traffic

**Library:**
```bash
pip install scapy
```

**Test with:**
```
Analyze the packet capture and tell me what protocols were used
```

---

### Challenge 14: Network Topology Discovery

**Objective:** Discover network topology using CDP/LLDP.

**Requirements:**
- Tool name: `discover_topology`
- Query devices for neighbor information
- Build topology map
- Return as structured data or Mermaid diagram

**Bonus:** Auto-generate Mermaid diagrams of discovered topology.

---

### Challenge 15: Multi-Site Latency Monitor

**Objective:** Monitor latency between multiple sites.

**Requirements:**
- Tool name: `check_latency_matrix`
- Takes list of sites/IPs
- Pings each from current location
- Returns latency matrix
- Identifies slow links

**Test with:**
```
Check latency to our branch offices: office-a.example.com, office-b.example.com, office-c.example.com
```

---

## Expert Challenges

### Challenge 16: Network Event Correlation

**Objective:** Correlate events across multiple devices and logs.

**Requirements:**
- Tool name: `correlate_events`
- Analyze multiple log files
- Find events happening around same time
- Identify cause-and-effect relationships
- Use time-series analysis

**Test with:**
```
We had an outage at 14:30 yesterday. Correlate events across all devices
around that time and help me identify the root cause.
```

---

### Challenge 17: Configuration Compliance Checker

**Objective:** Check device configs against compliance rules.

**Requirements:**
- Tool name: `check_compliance`
- Takes device config and policy rules
- Validates compliance
- Reports violations
- Suggests remediation

**Example rules:**
- SSH must be enabled
- Telnet must be disabled
- Logging must be configured
- Passwords must be encrypted

---

### Challenge 18: Automated Incident Response

**Objective:** Detect and respond to network incidents automatically.

**Requirements:**
- Tool name: `incident_response`
- Monitor logs in real-time
- Detect patterns (brute force, DDoS, etc.)
- Take automated actions (block IP, alert, etc.)
- Log all actions taken

**Test with:**
```
Monitor firewall01.log for security incidents and take appropriate action
```

---

### Challenge 19: Network Capacity Forecasting

**Objective:** Predict future capacity needs based on trends.

**Requirements:**
- Tool name: `forecast_capacity`
- Analyze historical metrics
- Identify growth trends
- Predict when capacity limits will be hit
- Recommend upgrade timeline

**Libraries:**
```bash
pip install pandas matplotlib scikit-learn
```

---

### Challenge 20: Multi-Vendor API Integration

**Objective:** Create unified interface for multiple network vendors.

**Requirements:**
- Tool name: `unified_device_api`
- Support multiple vendors (Cisco, Juniper, Arista, etc.)
- Abstract vendor differences
- Provide consistent interface
- Handle authentication per vendor

**Operations to support:**
- Get config
- Get status
- Make changes
- Backup config

---

## Bonus Challenges

### Challenge 21: Natural Language Query Interface

**Objective:** Allow complex queries in natural language.

**Example queries:**
```
Show me all devices in Data Center A that have been up for more than 100 days

Which interfaces are down across all switches?

Find devices with high CPU usage in the last hour
```

**Approach:**
- Let the AI parse the natural language
- Combine multiple tool calls
- Format results appropriately

---

### Challenge 22: Network Change Automation

**Objective:** Automate network changes with approval workflow.

**Requirements:**
- Parse change request
- Generate commands needed
- Show preview of changes
- Require approval
- Execute changes
- Verify changes
- Rollback if issues

**Safety first:** Start with read-only commands, then add change capability.

---

### Challenge 23: ML-Based Anomaly Detection

**Objective:** Use machine learning to detect network anomalies.

**Requirements:**
- Collect baseline metrics
- Train anomaly detection model
- Monitor for deviations
- Alert on anomalies
- Suggest possible causes

**Libraries:**
```bash
pip install scikit-learn pandas numpy
```

---

### Challenge 24: ChatOps Integration

**Objective:** Integrate MCP tools with chat platforms.

**Requirements:**
- Connect to Slack/Teams/Discord
- Expose MCP tools via chat commands
- Allow team collaboration
- Log all actions
- Implement access controls

---

### Challenge 25: Full Network Digital Twin

**Objective:** Create a complete digital representation of your network.

**Requirements:**
- Discover all devices automatically
- Map all connections
- Monitor all metrics in real-time
- Simulate changes before applying
- Visualize entire network state
- Track changes over time

**This is a capstone project combining multiple skills!**

---

## Challenge Evaluation Criteria

For each challenge, consider:

### Functionality (40%)
- Does it work correctly?
- Handles errors gracefully?
- Edge cases covered?

### Code Quality (20%)
- Well-structured?
- Documented?
- Follows Python best practices?

### MCP Integration (20%)
- Good tool descriptions?
- Appropriate parameters?
- AI can use it effectively?

### User Experience (20%)
- Easy to use?
- Clear output?
- Helpful error messages?

---

## Submission Ideas

If you complete challenges:

1. **Share with community**
   - Post on GitHub
   - Write blog post
   - Create tutorial

2. **Build a portfolio**
   - Document your solutions
   - Show real-world applications
   - Demonstrate your skills

3. **Contribute back**
   - Improve these labs
   - Add new scenarios
   - Help others learning

---

## Getting Help

**Stuck on a challenge?**

1. Review the main [MCP Lab](../README.md)
2. Check [Troubleshooting Guide](../TROUBLESHOOTING.md)
3. Review scenario labs for examples
4. Break problem into smaller pieces
5. Test each piece independently

**Tips:**
- Start simple, add complexity gradually
- Test thoroughly with different inputs
- Document as you go
- Ask for help when needed

---

## Next Level

Completed these challenges? Consider:

1. **Build a production MCP server** for your organization
2. **Integrate with real network infrastructure**
3. **Develop custom workflows** for your team's needs
4. **Train others** on MCP and AI-assisted operations
5. **Contribute to MCP ecosystem** with new tools/servers

---

## Resources

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [MCP Protocol Spec](https://modelcontextprotocol.io/)
- [Python Network Programming](https://docs.python.org/3/library/socket.html)
- [Netmiko Documentation](https://github.com/ktbyers/netmiko)
- [Scapy Documentation](https://scapy.net/)

---

**Happy Building!**

Share your solutions and help others learn. Network engineering + AI is the future!
