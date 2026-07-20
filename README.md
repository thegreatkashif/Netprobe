# NetProbe

A lightweight Python network discovery and port scanning tool.

## Features

- Automatic local network detection
- CIDR network scanning
- Multi-threaded host discovery
- Hybrid ICMP + TCP host detection
- Hostname resolution
- Common TCP port scanning
- Progress bar
- Colored terminal output
- JSON export
- CSV export

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

## Example Output

```text
✓ Valid Network
Detected Network: 192.168.31.0/24

Scanning Hosts: 100%|████████████████████| 254/254

IP Address         Hostname                  Open Ports
----------------------------------------------------------------------
192.168.31.1       Router                    80,443
192.168.31.149     LENOVO                    None

Scan Complete
Hosts discovered : 2
Time taken       : 1.12 seconds
```

## Project Structure

```
NetProbe/
├── scanner/
│   ├── discovery.py
│   ├── exporter.py
│   ├── network.py
│   └── ports.py
├── netprobe.py
├── requirements.txt
└── README.md
```

## Technologies

- Python
- socket
- ipaddress
- concurrent.futures
- colorama
- tqdm
- psutil

## License

MIT License