import json

from scanner.exporter import export_json


def test_export_json(tmp_path):
    file = tmp_path / "results.json"

    data = [
        {
            "ip": "127.0.0.1",
            "hostname": "localhost",
            "ports": [80]
        }
    ]

    export_json(file, data)

    with open(file, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    assert loaded == data