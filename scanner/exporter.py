import json
import csv
import html
from datetime import datetime


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


def _escape(value):
    return html.escape(str(value), quote=True)


def _render_ports(ports):
    if not ports:
        return '<span class="muted">None</span>'

    rows = []
    for p in ports:
        badge = f'<span class="badge">{_escape(p["port"])}/{_escape(p["service"])}</span>'
        if p["banner"]:
            badge += f'<div class="banner">{_escape(p["banner"])}</div>'
        rows.append(badge)

    return "".join(rows)


def export_html(filename, results, meta=None):
    """
    Write a self-contained, styled HTML scan report.

    meta is an optional dict that may include: network, duration_seconds,
    hosts_scanned. Any missing keys are simply omitted from the summary.
    """
    meta = meta or {}

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    online_count = len(results)

    summary_items = [
        ("Generated", generated_at),
        ("Target network", meta.get("network", "-")),
        ("Hosts scanned", meta.get("hosts_scanned", "-")),
        ("Hosts online", online_count),
        (
            "Duration",
            f"{meta['duration_seconds']:.2f}s" if "duration_seconds" in meta else "-",
        ),
    ]

    summary_html = "".join(
        f'<div class="stat"><div class="stat-label">{_escape(label)}</div>'
        f'<div class="stat-value">{_escape(value)}</div></div>'
        for label, value in summary_items
    )

    if results:
        rows_html = "".join(
            "<tr>"
            f'<td class="mono">{_escape(host["ip"])}</td>'
            f'<td>{_escape(host["hostname"])}</td>'
            f'<td>{_render_ports(host["ports"])}</td>'
            "</tr>"
            for host in results
        )
        table_html = f"""
        <table>
            <thead>
                <tr><th>IP Address</th><th>Hostname</th><th>Open Ports</th></tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
        """
    else:
        table_html = '<p class="muted">No online hosts found.</p>'

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>NetProbe Scan Report</title>
<style>
    :root {{
        --bg: #0f1117;
        --panel: #161925;
        --border: #262b3d;
        --text: #e6e8ef;
        --muted: #8b90a5;
        --accent: #4fd1c5;
        --accent-dim: #1f4a47;
    }}
    body {{
        margin: 0;
        padding: 40px 24px;
        background: var(--bg);
        color: var(--text);
        font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    .container {{
        max-width: 960px;
        margin: 0 auto;
    }}
    h1 {{
        margin: 0 0 4px;
        font-size: 28px;
    }}
    .subtitle {{
        color: var(--muted);
        margin-bottom: 28px;
    }}
    .summary {{
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-bottom: 32px;
    }}
    .stat {{
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 14px 18px;
        min-width: 140px;
        flex: 1;
    }}
    .stat-label {{
        color: var(--muted);
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }}
    .stat-value {{
        font-size: 20px;
        font-weight: 600;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 10px;
        overflow: hidden;
    }}
    th, td {{
        text-align: left;
        padding: 12px 16px;
        border-bottom: 1px solid var(--border);
        vertical-align: top;
    }}
    th {{
        color: var(--muted);
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    tr:last-child td {{
        border-bottom: none;
    }}
    .mono {{
        font-family: "SF Mono", Consolas, monospace;
    }}
    .badge {{
        display: inline-block;
        background: var(--accent-dim);
        color: var(--accent);
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 12px;
        margin: 2px 4px 2px 0;
        font-family: "SF Mono", Consolas, monospace;
    }}
    .banner {{
        color: var(--muted);
        font-size: 12px;
        margin: 2px 0 6px 2px;
    }}
    .muted {{
        color: var(--muted);
    }}
    footer {{
        margin-top: 28px;
        color: var(--muted);
        font-size: 12px;
    }}
</style>
</head>
<body>
<div class="container">
    <h1>NetProbe Scan Report</h1>
    <div class="subtitle">Generated by NetProbe</div>

    <div class="summary">
        {summary_html}
    </div>

    {table_html}

    <footer>NetProbe &mdash; lightweight Python network discovery tool</footer>
</div>
</body>
</html>
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_doc)