from scanner.discovery import validate_network, generate_hosts


def test_validate_network_valid():
    network = validate_network("192.168.1.0/24")
    assert str(network) == "192.168.1.0/24"


def test_validate_network_invalid():
    assert validate_network("abc") is None


def test_generate_hosts():
    hosts = generate_hosts(validate_network("192.168.1.0/30"))
    assert len(hosts) == 2