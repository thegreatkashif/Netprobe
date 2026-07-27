from scanner.network import detect_local_network


def test_detect_network():
    network = detect_local_network()

    assert network is not None