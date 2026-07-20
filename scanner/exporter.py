import json
import csv


def export_json(filename, results):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)


def export_csv(filename, results):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(["IP Address", "Hostname", "Open Ports"])

        for host in results:
            writer.writerow([
                host["ip"],
                host["hostname"],
                ", ".join(map(str, host["ports"])) if host["ports"] else "None"
            ])