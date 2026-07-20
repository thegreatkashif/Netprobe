import argparse
import time

from scanner.discovery import (
    validate_network,
    generate_hosts,
    discover_hosts,
    get_hostname,
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

    start = time.perf_counter()

    online_hosts = discover_hosts(hosts)

    end = time.perf_counter()

    if online_hosts:
        print(f"{'IP Address':<18} Hostname")
        print("-" * 40)

        for host in online_hosts:
            hostname = get_hostname(host)
            print(f"{str(host):<18} {hostname}")
    else:
        print("No online hosts found.")

    print("\nScan Complete")
    print(f"{len(online_hosts)} hosts discovered")
    print(f"Scan completed in {end - start:.2f} seconds")


if __name__ == "__main__":
    main()