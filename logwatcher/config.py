"""Load settings from config.yaml."""

import yaml

DEFAULTS = {
    "failed_login_threshold": 5,
    "top_n": 5,
}


def load_config(path):
    try:
        with open(path, encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}
    except FileNotFoundError:
        raise FileNotFoundError(f"config file not found: {path}") from None

    return {**DEFAULTS, **data}
