#!/usr/bin/env python3
"""
MCP Server with Network Diagnostic Tools
Provides ping, DNS lookup, and port checking capabilities
"""

import subprocess
import socket
import dns.resolver
from typing import Optional
from fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("Network Tools")

@mcp.tool()
def ping(hostname: str, count: int = 4) -> str:
    """
    Check if a host is reachable using ICMP ping.

    Args:
        hostname: The hostname or IP address to ping
        count: Number of ping packets to send (default: 4)

    Returns:
        Ping results including latency and packet loss
    """
    try:
        # Run ping command
        result = subprocess.run(
            ["ping", "-c", str(count), hostname],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            # Parse output for summary
            lines = result.stdout.split('\n')
            summary = [l for l in lines if 'packet loss' in l or 'rtt' in l or 'min/avg/max' in l]
            return f"✓ {hostname} is reachable\n" + "\n".join(summary)
        else:
            return f"✗ {hostname} is not reachable\n{result.stdout}"

    except subprocess.TimeoutExpired:
        return f"✗ Ping to {hostname} timed out"
    except Exception as e:
        return f"✗ Error pinging {hostname}: {str(e)}"


@mcp.tool()
def dns_lookup(hostname: str, record_type: str = "A") -> str:
    """
    Perform DNS lookup for a hostname.

    Args:
        hostname: The hostname to resolve
        record_type: DNS record type (A, AAAA, MX, NS, TXT, CNAME)

    Returns:
        DNS resolution results
    """
    try:
        resolver = dns.resolver.Resolver()

        # Query DNS
        answers = resolver.resolve(hostname, record_type)

        results = [f"DNS lookup for {hostname} ({record_type} records):"]
        for rdata in answers:
            results.append(f"  - {rdata.to_text()}")

        return "\n".join(results)

    except dns.resolver.NXDOMAIN:
        return f"✗ {hostname} does not exist (NXDOMAIN)"
    except dns.resolver.NoAnswer:
        return f"✗ No {record_type} records found for {hostname}"
    except dns.resolver.Timeout:
        return f"✗ DNS query timed out for {hostname}"
    except Exception as e:
        return f"✗ Error resolving {hostname}: {str(e)}"


@mcp.tool()
def check_port(hostname: str, port: int, timeout: float = 3.0) -> str:
    """
    Check if a TCP port is open on a host.

    Args:
        hostname: The hostname or IP address to check
        port: The TCP port number to check
        timeout: Connection timeout in seconds (default: 3.0)

    Returns:
        Port status and connection result
    """
    try:
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        # Try to connect
        result = sock.connect_ex((hostname, port))
        sock.close()

        if result == 0:
            # Try to identify common services
            try:
                service = socket.getservbyport(port, 'tcp')
            except:
                service = "unknown"
            return f"✓ Port {port} is OPEN on {hostname} (service: {service})"
        else:
            return f"✗ Port {port} is CLOSED or filtered on {hostname}"

    except socket.gaierror:
        return f"✗ Could not resolve hostname: {hostname}"
    except socket.timeout:
        return f"✗ Connection to {hostname}:{port} timed out"
    except Exception as e:
        return f"✗ Error checking port: {str(e)}"


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
