__version__ = "2.0.0"


import argparse
import time

from colorama import Fore, Style, init

from scanner.discovery import (
    validate_network,
    generate_hosts,
    discover_hosts,
    get_hostname,
)
from scanner.ports import scan_ports
from scanner.network import detect_local_network
from scanner.exporter import export_json, export_csv
from scanner.config import load_config

# Initialize Colorama
init(autoreset=True)


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
    "--version",
    action="version",
    version=f"%(prog)s {__version__}"
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

    parser.add_argument(
        "--config",
        metavar="FILE",
        help="Path to a JSON config file (ports, timeouts, concurrency)"
    )

    args = parser.parse_args()

    try:
        config = load_config(args.config)
    except (FileNotFoundError, ValueError) as e:
        print(Fore.RED + f"✗ {e}")
        return

    # Determine target network
    if args.auto:
        network = detect_local_network()
    else:
        if args.network is None:
            parser.error("Please provide a network or use --auto.")
        network = validate_network(args.network)

    if network is None:
        print(Fore.RED + f"✗ Invalid network: {args.network}")
        return

    print(Fore.GREEN + "✓ Valid Network")

    if args.auto:
        print(Fore.CYAN + f"Detected Network: {network}")
    else:
        print(Fore.CYAN + f"Target Network: {network}")

    hosts = generate_hosts(network)

    print(Fore.YELLOW + "\nScanning...\n")

    start = time.perf_counter()

    online_hosts = discover_hosts(
        hosts,
        max_concurrency=config["host_concurrency"],
        ping_timeout=config["ping_timeout"],
        tcp_timeout=config["tcp_timeout"],
    )

    end = time.perf_counter()

    results = []

    if online_hosts:
        print(
            Fore.MAGENTA
            + f"{'IP Address':<18} {'Hostname':<25} {'Open Ports'}"
        )
        print("-" * 70)

        for host in online_hosts:
            hostname = get_hostname(host)
            ports = scan_ports(
                host,
                ports=config["ports"],
                timeout=config["port_timeout"],
                max_concurrency=config["port_concurrency"],
            )

            port_text = (
                ", ".join(f"{p['port']}/{p['service']}" for p in ports)
                if ports else "None"
            )

            print(
                Fore.GREEN
                + f"{str(host):<18}"
                + Style.RESET_ALL
                + f"{hostname:<25} {port_text}"
            )

            for p in ports:
                if p["banner"]:
                    print(Fore.BLUE + f"    └─ {p['port']}: {p['banner']}")

            results.append(
                {
                    "ip": str(host),
                    "hostname": hostname,
                    "ports": ports,
                }
            )

    else:
        print(Fore.RED + "No online hosts found.")

    print(Fore.CYAN + "\nScan Complete")
    print(Fore.GREEN + f"Hosts discovered : {len(online_hosts)}")
    print(Fore.GREEN + f"Time taken       : {end - start:.2f} seconds")

    if args.json:
        export_json(args.json, results)
        print(Fore.GREEN + f"\n✓ JSON report saved to '{args.json}'")

    if args.csv:
        export_csv(args.csv, results)
        print(Fore.GREEN + f"✓ CSV report saved to '{args.csv}'")


if __name__ == "__main__":
    main()