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

def tcp_probe(host):
    """
    Returns True if any common TCP port accepts a connection.
    """

    common_ports = [22, 80, 443, 445, 3389]

    for port in common_ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.3)

                if sock.connect_ex((str(host), port)) == 0:
                    return True

        except OSError:
            pass

    return False


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
    online_hosts = []

    def check(host):
        if is_host_alive(host):
            return host

        if tcp_probe(host):
            return host

        return None

    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(check, hosts)

        for result in results:
            if result is not None:
                online_hosts.append(result)

    return online_hosts