import socket


COMMON_PORTS = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    3389: "RDP",
    445: "SMB",
}


def scan_ports(host):
    open_ports = []

    for port in COMMON_PORTS:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)

        try:
            if sock.connect_ex((str(host), port)) == 0:
                open_ports.append(port)
        finally:
            sock.close()

    return open_ports