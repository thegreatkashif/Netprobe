# NetProbe

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-2.0.0-orange)

A lightweight Python network discovery and port scanning tool.

## Features

- Automatic local network detection
- CIDR network scanning
- Async host discovery (asyncio, high concurrency)
- Hybrid ICMP + TCP host detection
- Hostname resolution
- Async port scanning with service name + banner detection
- JSON config file support (ports, timeouts, concurrency)
- Progress bar
- Colored terminal output
- Verbose / quiet output modes
- Robust error handling (bad hosts don't crash the scan, Ctrl+C exits cleanly)
- JSON export
- CSV export
- Styled HTML report export

## Installation

```bash
git clone https://github.com/<your-username>/NetProbe.git
cd NetProbe

pip install -r requirements.txt
```

## Usage

### Automatic Scan

```bash
python netprobe.py --auto
```

### Scan Specific Network

```bash
python netprobe.py 192.168.1.0/24
```

### Export JSON

```bash
python netprobe.py --auto --json results.json
```

### Export CSV

```bash
python netprobe.py --auto --csv results.csv
```

### Export HTML Report

```bash
python netprobe.py --auto --html report.html
```

Generates a self-contained, styled HTML report with a summary panel (network, hosts scanned/online, duration) and a table of hosts, open ports, services, and banners. Open it in any browser.

### Use a Config File

Copy `netprobe.example.json` to `netprobe.json` (or any name) and adjust ports/timeouts/concurrency:

```bash
python netprobe.py 192.168.1.0/24 --config netprobe.json
```

```json
{
    "ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 8080],
    "port_timeout": 0.5,
    "port_concurrency": 50,
    "host_concurrency": 200,
    "ping_timeout": 0.5,
    "tcp_timeout": 0.3
}
```

`ports: null` (the default) uses the built-in common port list.

### Verbose / Quiet Modes

```bash
python netprobe.py 192.168.1.0/24 --verbose   # show resolved config before scanning
python netprobe.py 192.168.1.0/24 --quiet     # only print the final summary
```

### Combine Everything

```bash
python netprobe.py --auto --config netprobe.json --json results.json --csv results.csv --html report.html -v
```

## All CLI Options

usage: NetProbe [-h] [--version] [--auto] [--json FILE] [--csv FILE]
[--config FILE] [--html FILE] [-v] [-q]
[network]

A lightweight Python network discovery tool.

positional arguments:
network Target network in CIDR format (e.g. 192.168.1.0/24)

options:
-h, --help show this help message and exit
--version show program's version number and exit
--auto Automatically detect and scan the local network
--json FILE Export scan results to a JSON file
--csv FILE Export scan results to a CSV file
--config FILE Path to a JSON config file (ports, timeouts, concurrency)
--html FILE Export scan results to a styled HTML report
-v, --verbose Show extra scan details (resolved config, timeouts,
concurrency)
-q, --quiet Only print the final summary (suppress progress bar and
per-host output)


## Example Output

```text
✓ Valid Network
Detected Network: 192.168.31.0/24

Scanning Hosts: 100%|████████████████████| 254/254

IP Address         Hostname                  Open Ports
----------------------------------------------------------------------
192.168.31.1       Router                    80/HTTP, 443/HTTPS
    └─ 80: HTTP/1.1 401 Unauthorized
192.168.31.149     LENOVO                    None

Scan Complete
Hosts discovered : 2
Time taken       : 0.41 seconds
```

## Project Structure

NetProbe/
├── scanner/
│ ├── config.py
│ ├── discovery.py
│ ├── exporter.py
│ ├── network.py
│ └── ports.py
├── tests/
│ ├── test_discovery.py
│ ├── test_exporter.py
│ ├── test_network.py
│ └── test_ports.py
├── netprobe.py
├── netprobe.example.json
├── requirements.txt
└── README.md


## Technologies

- Python
- asyncio
- socket
- ipaddress
- colorama
- tqdm
- psutil

## Changelog

### v2.0.0

- Async host discovery (asyncio instead of a thread pool) for much higher concurrency
- Async port scanning + service/banner detection; expanded common port list
- JSON config file support (`--config`) for ports, timeouts, and concurrency
- Styled HTML report export (`--html`)
- `-v/--verbose` and `-q/--quiet` output modes
- More robust error handling: a failing host no longer aborts the whole scan, and Ctrl+C exits cleanly

### v1.0.0

- Initial release: CIDR scanning, threaded discovery, common port scanning, JSON/CSV export

## License

MIT License