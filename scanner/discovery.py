import ipaddress
import platform
import subprocess


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
    """
    Returns True if the host responds to a ping.
    """
    param = "-n" if platform.system().lower() == "windows" else "-c"

    command = ["ping", param, "1", str(host)]

    result = subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return result.returncode == 0


def discover_hosts(hosts):
    """
    Return all reachable hosts.
    """
    online_hosts = []

    for host in hosts:
        if is_host_alive(host):
            online_hosts.append(host)

    return online_hosts