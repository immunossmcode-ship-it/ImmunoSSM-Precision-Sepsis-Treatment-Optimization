from pathlib import Path
import yaml

def load_config(path):
    with Path(path).open("r", encoding="utf-8") as stream:
        config = yaml.safe_load(stream)
    _reject_unresolved(config)
    return config

def _reject_unresolved(value, path="config"):
    if isinstance(value, dict):
        for key, item in value.items():
            _reject_unresolved(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_unresolved(item, f"{path}[{index}]")
    elif isinstance(value, str) and value.startswith("REPLACE_WITH"):
        raise ValueError(f"Complete required configuration field: {path}")
