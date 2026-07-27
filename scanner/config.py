import json
import os


DEFAULT_CONFIG = {
    # None means "use scanner.ports.COMMON_PORTS"
    "ports": None,
    "port_timeout": 0.5,
    "port_concurrency": 50,
    "host_concurrency": 200,
    "ping_timeout": 0.5,
    "tcp_timeout": 0.3,
}


def load_config(path=None):
    """
    Load a NetProbe JSON config file and merge it over the defaults.

    Returns a dict with every key in DEFAULT_CONFIG present. Unknown keys
    in the file are kept as-is (ignored by the CLI) rather than rejected,
    so configs can carry forward-compatible extras.

    Raises FileNotFoundError if path is given but doesn't exist, and
    ValueError if the file isn't valid JSON or isn't a JSON object.
    """
    config = dict(DEFAULT_CONFIG)

    if path is None:
        return config

    if not os.path.isfile(path):
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        try:
            user_config = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file '{path}': {e}")

    if not isinstance(user_config, dict):
        raise ValueError(f"Config file '{path}' must contain a JSON object.")

    config.update(user_config)
    return config