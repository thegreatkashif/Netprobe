import ipaddress


def validate_network(network: str):
    """
    Validate a network in CIDR notation.
    Returns an IPv4Network object if valid.
    """

    try:
        return ipaddress.ip_network(network, strict=False)

    except ValueError:
        return None

def generate_hosts(network):
    """
    Generate all usable host IP addresses in the network.
    """

    return list(network.hosts())