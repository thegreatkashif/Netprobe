import argparse

from scanner.discovery import (
    validate_network,
    generate_hosts,
    discover_hosts,
)


def main():
    parser = argparse.ArgumentParser(
        prog="NetProbe",
        description="A lightweight Python network discovery tool."
    )

    parser.add_argument(
        "network",
        help="Target network in CIDR notation (e.g. 192.168.1.0/24)"
    )

    args = parser.parse_args()

    network = validate_network(args.network)

    if network is None:
        print(f"✗ Invalid network: {args.network}")
        return

    print("✓ Valid Network")
    print(f"Target Network: {network}")

    hosts = generate_hosts(network)

    print("\nScanning...\n")

    online_hosts = discover_hosts(hosts)

    if online_hosts:
        for host in online_hosts:
            print(f"{str(host):<18} Online")
    else:
        print("No online hosts found.")

    print("\nScan Complete")
    print(f"{len(online_hosts)} hosts discovered")


if __name__ == "__main__":
    main()