import argparse
import time

from scanner.discovery import (
    validate_network,
    generate_hosts,
    discover_hosts,
    get_hostname,
)
from scanner.ports import scan_ports
from scanner.network import detect_local_network
from scanner.exporter import export_json, export_csv


def main():
    parser = argparse.ArgumentParser(
        prog="NetProbe",
        description="A lightweight Python network discovery tool."
    )

    parser.add_argument(
        "network",
        nargs="?",
        help="Target network in CIDR format (e.g. 192.168.1.0/24)"
    )

    parser.add_argument(
        "--auto",
        action="store_true",
        help="Automatically detect and scan the local network"
    )

    parser.add_argument(
        "--json",
        metavar="FILE",
        help="Export scan results to a JSON file"
    )

    parser.add_argument(
        "--csv",
        metavar="FILE",
        help="Export scan results to a CSV file"
    )

    args = parser.parse_args()

    # Determine target network
    if args.auto:
        network = detect_local_network()
    else:
        if args.network is None:
            parser.error("Please provide a network or use --auto.")
        network = validate_network(args.network)

    if network is None:
        print(f"✗ Invalid network: {args.network}")
        return

    print("✓ Valid Network")

    if args.auto:
        print(f"Detected Network: {network}")
    else:
        print(f"Target Network: {network}")

    hosts = generate_hosts(network)

    print("\nScanning...\n")

    start = time.perf_counter()

    online_hosts = discover_hosts(hosts)

    end = time.perf_counter()

    results = []

    if online_hosts:
        print(f"{'IP Address':<18} {'Hostname':<25} {'Open Ports'}")
        print("-" * 70)

        for host in online_hosts:
            hostname = get_hostname(host)
            ports = scan_ports(host)

            port_text = ", ".join(map(str, ports)) if ports else "None"

            print(f"{str(host):<18} {hostname:<25} {port_text}")

            results.append(
                {
                    "ip": str(host),
                    "hostname": hostname,
                    "ports": ports,
                }
            )

    else:
        print("No online hosts found.")

    print("\nScan Complete")
    print(f"Hosts discovered : {len(online_hosts)}")
    print(f"Time taken       : {end - start:.2f} seconds")

    if args.json:
        export_json(args.json, results)
        print(f"\n✓ JSON report saved to '{args.json}'")

    if args.csv:
        export_csv(args.csv, results)
        print(f"✓ CSV report saved to '{args.csv}'")


if __name__ == "__main__":
    main()