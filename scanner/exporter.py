import json
import csv


def export_json(filename, results):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)


def export_csv(filename, results):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(["IP Address", "Hostname", "Open Ports", "Banners"])

        for host in results:
            ports = host["ports"]

            port_text = (
                ", ".join(f"{p['port']}/{p['service']}" for p in ports)
                if ports else "None"
            )
            banner_text = (
                " | ".join(f"{p['port']}: {p['banner']}" for p in ports if p["banner"])
                or "None"
            )

            writer.writerow([host["ip"], host["hostname"], port_text, banner_text])