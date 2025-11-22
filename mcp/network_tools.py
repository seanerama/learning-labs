#!/usr/bin/env python3
"""
MCP Server with Network Diagnostic Tools
Provides ping, DNS lookup, and port checking capabilities for network engineers.
"""

import subprocess
import socket
import asyncio
import logging
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("Network Tools")


@mcp.tool()
async def ping(hostname: str, count: int = 4) -> str:
    """
    Check if a host is reachable using ICMP ping.

    Args:
        hostname: The hostname or IP address to ping (e.g., "google.com", "8.8.8.8")
        count: Number of ping packets to send (default: 4)

    Returns:
        Ping results including latency and packet loss information
    """
    try:
        logger.info(f"Pinging {hostname} with {count} packets")

        # Run ping command asynchronously
        process = await asyncio.create_subprocess_exec(
            "ping", "-c", str(count), hostname,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=15)
        output = stdout.decode()

        if process.returncode == 0:
            # Parse output for summary
            lines = output.split('\n')
            summary = [l for l in lines if 'packet loss' in l or 'rtt' in l or 'min/avg/max' in l]
            result = f"✓ {hostname} is reachable\n" + "\n".join(summary)
            logger.info(f"Ping successful: {hostname}")
            return result
        else:
            result = f"✗ {hostname} is not reachable\n{output}"
            logger.warning(f"Ping failed: {hostname}")
            return result

    except asyncio.TimeoutError:
        error_msg = f"✗ Ping to {hostname} timed out"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"✗ Error pinging {hostname}: {str(e)}"
        logger.error(error_msg)
        return error_msg


@mcp.tool()
async def dns_lookup(hostname: str, record_type: str = "A") -> str:
    """
    Perform DNS lookup for a hostname.

    Args:
        hostname: The hostname to resolve (e.g., "github.com", "google.com")
        record_type: DNS record type - A, AAAA, MX, NS, TXT, or CNAME (default: "A")

    Returns:
        DNS resolution results showing IP addresses or other record data
    """
    try:
        logger.info(f"DNS lookup for {hostname} ({record_type} records)")

        # Import dns.resolver here to handle if dnspython isn't installed
        try:
            import dns.resolver
        except ImportError:
            return "Error: dnspython not installed. Run: pip install dnspython"

        resolver = dns.resolver.Resolver()
        answers = resolver.resolve(hostname, record_type)

        results = [f"DNS lookup for {hostname} ({record_type} records):"]
        for rdata in answers:
            results.append(f"  - {rdata.to_text()}")

        result = "\n".join(results)
        logger.info(f"DNS lookup successful: {hostname}")
        return result

    except dns.resolver.NXDOMAIN:
        error_msg = f"✗ {hostname} does not exist (NXDOMAIN)"
        logger.warning(error_msg)
        return error_msg
    except dns.resolver.NoAnswer:
        error_msg = f"✗ No {record_type} records found for {hostname}"
        logger.warning(error_msg)
        return error_msg
    except dns.resolver.Timeout:
        error_msg = f"✗ DNS query timed out for {hostname}"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"✗ Error resolving {hostname}: {str(e)}"
        logger.error(error_msg)
        return error_msg


@mcp.tool()
async def check_port(hostname: str, port: int, timeout: float = 3.0) -> str:
    """
    Check if a TCP port is open on a host.

    Args:
        hostname: The hostname or IP address to check (e.g., "google.com", "192.168.1.1")
        port: The TCP port number to check (e.g., 80, 443, 22)
        timeout: Connection timeout in seconds (default: 3.0)

    Returns:
        Port status indicating if the port is open, closed, or filtered
    """
    try:
        logger.info(f"Checking port {port} on {hostname}")

        # Use asyncio for non-blocking socket connection
        loop = asyncio.get_event_loop()

        def check_socket():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((hostname, port))
            sock.close()
            return result

        result = await loop.run_in_executor(None, check_socket)

        if result == 0:
            # Try to identify common services
            try:
                service = socket.getservbyport(port, 'tcp')
            except (OSError, socket.error):
                service = "unknown"

            result_msg = f"✓ Port {port} is OPEN on {hostname} (service: {service})"
            logger.info(result_msg)
            return result_msg
        else:
            result_msg = f"✗ Port {port} is CLOSED or filtered on {hostname}"
            logger.info(result_msg)
            return result_msg

    except socket.gaierror:
        error_msg = f"✗ Could not resolve hostname: {hostname}"
        logger.error(error_msg)
        return error_msg
    except socket.timeout:
        error_msg = f"✗ Connection to {hostname}:{port} timed out"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"✗ Error checking port: {str(e)}"
        logger.error(error_msg)
        return error_msg


if __name__ == "__main__":
    import os

    port = int(os.getenv("MCP_SERVER_PORT", "8000"))
    logger.info(f"Starting Network Tools MCP server")
    logger.info(f"Available tools: ping, dns_lookup, check_port")

    # FastMCP uses its own run method
    mcp.run()
