import asyncio
import ipaddress
import platform
import socket

from tqdm import tqdm

COMMON_PROBE_PORTS = (22, 80, 443, 445, 3389)


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


async def _ping_alive(host, timeout=0.5):
    """
    Async ICMP liveness check via the system ping binary.
    """
    system = platform.system().lower()

    if system == "windows":
        command = ["ping", "-n", "1", "-w", str(int(timeout * 1000)), str(host)]
    else:
        command = ["ping", "-c", "1", "-W", str(max(1, int(timeout))), str(host)]

    try:
        proc = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
        )
        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=timeout + 1)
    except (asyncio.TimeoutError, OSError):
        return False

    output = stdout.decode(errors="ignore").lower()

    if system == "windows":
        return "ttl=" in output
    return "1 received" in output or "bytes from" in output


async def _tcp_probe(host, ports=COMMON_PROBE_PORTS, timeout=0.3):
    """
    Returns True if any common TCP port accepts a connection.
    """
    for port in ports:
        try:
            _, writer = await asyncio.wait_for(
                asyncio.open_connection(str(host), port), timeout=timeout
            )
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass
            return True
        except (asyncio.TimeoutError, OSError):
            continue

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


async def _check_host(host, semaphore):
    async with semaphore:
        if await _ping_alive(host):
            return host

        if await _tcp_probe(host):
            return host

        return None


async def _discover_hosts_async(hosts, max_concurrency=200):
    semaphore = asyncio.Semaphore(max_concurrency)
    tasks = [asyncio.ensure_future(_check_host(host, semaphore)) for host in hosts]

    online_hosts = []

    for coro in tqdm(
        asyncio.as_completed(tasks),
        total=len(tasks),
        desc="Scanning Hosts",
        unit="host",
    ):
        result = await coro
        if result is not None:
            online_hosts.append(result)

    return online_hosts


def discover_hosts(hosts):
    """
    Discover which hosts are online. Sync entry point that runs the
    asyncio-based scan underneath for much higher concurrency than the
    old thread-pool implementation.
    """
    return asyncio.run(_discover_hosts_async(hosts))