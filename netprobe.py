import argparse
from scanner.discovery import validate_network
from scanner.discovery import generate_hosts



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

    print("\nHosts:")

    for host in hosts:
        print(host)
 
    print(f"\nTotal Hosts: {len(hosts)}")


if __name__ == "__main__":
    main()