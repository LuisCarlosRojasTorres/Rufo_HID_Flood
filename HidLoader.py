import json
from pathlib import Path
from typing import Any, Dict


def load_hid_combinations(json_path: str | Path) -> Dict[str, dict[str, Any]]:
    """Load keyboard HID combinations from a JSON file.

    Expected shape:
    {
      "COMBO_NAME": {
        "modifiers": ["CTRL", "ALT"],
        "keys": ["DELETE"]
      }
    }
    """
    path = Path(json_path)
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object/dictionary")

    normalized: Dict[str, dict[str, Any]] = {}
    for combo_name, combo in data.items():
        if not isinstance(combo_name, str):
            raise ValueError("Combination names must be strings")
        if not isinstance(combo, dict):
            raise ValueError(f"Combination '{combo_name}' must be an object")

        modifiers = combo.get("modifiers", [])
        keys = combo.get("keys", [])
        repeat = combo.get("repeat", 1)

        if not isinstance(modifiers, list) or not all(isinstance(m, str) for m in modifiers):
            raise ValueError(f"'{combo_name}.modifiers' must be a list of strings")
        if not isinstance(keys, list) or not all(isinstance(k, str) for k in keys):
            raise ValueError(f"'{combo_name}.keys' must be a list of strings")
        if not isinstance(repeat, int) or repeat < 1:
            raise ValueError(f"'{combo_name}.repeat' must be an integer >= 1")

        normalized[combo_name.upper()] = {
            "modifiers": [m.upper() for m in modifiers],
            "keys": [k.upper() for k in keys],
            "repeat": repeat,
        }

    return normalized
