import socket
import ipaddress
import psutil


def detect_local_network():
    """
    Automatically detect the active IPv4 network and subnet mask.
    """

    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]

    
    for _, addresses in psutil.net_if_addrs().items():
        for addr in addresses:
            if addr.family == socket.AF_INET and addr.address == local_ip:
                network = ipaddress.IPv4Network(
                    f"{addr.address}/{addr.netmask}",
                    strict=False
                )
                return network

    return None