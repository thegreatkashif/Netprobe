import ipaddress
import platform
import subprocess
from concurrent.futures import ThreadPoolExecutor
import socket


def validate_network(network: str):
    """
    Validate a network in CIDR notation.
    Returns an IPv4Network object if valid, otherwise None.
    """
    try:
        return ipaddress.ip_network(network, strict=False)
    except ValueError:
        return None


def generate_hosts(network):
    """
    Generate all usable host IP addresses.
    """
    return list(network.hosts())


def is_host_alive(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"

    command = ["ping", param, "1", "-w", "500", str(host)]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    output = result.stdout.lower()

    if platform.system().lower() == "windows":
        return "ttl=" in output
    else:
        return "1 received" in output or "bytes from" in output

def get_hostname(host):
    """
    Resolve the hostname of an IP address.
    Returns 'Unknown' if it cannot be resolved.
    """
    try:
        hostname = socket.gethostbyaddr(str(host))[0]
        return hostname
    except socket.herror:
        return "Unknown"
    except Exception:
        return "Unknown"

def discover_hosts(hosts):
    """
    Discover reachable hosts using multiple threads.
    """

    online_hosts = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(
            lambda host: (host, is_host_alive(host)),
            hosts
        )

        for host, alive in results:
            if alive:
                online_hosts.append(host)

    return online_hosts