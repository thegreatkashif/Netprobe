import argparse


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

    print(f"Target Network: {args.network}")


if __name__ == "__main__":
    main()