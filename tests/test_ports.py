from scanner.ports import scan_ports


def test_scan_localhost():
    ports = scan_ports("127.0.0.1")

    assert isinstance(ports, list)