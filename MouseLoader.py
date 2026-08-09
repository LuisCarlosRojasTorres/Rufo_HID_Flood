import json
from pathlib import Path
from typing import Any, Dict


def load_mouse_combinations(json_path: str | Path) -> Dict[str, dict[str, Any]]:
    """Load mouse HID actions from a JSON file."""
    path = Path(json_path)
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object/dictionary")

    normalized: Dict[str, dict[str, Any]] = {}
    for action_name, action in data.items():
        if not isinstance(action_name, str):
            raise ValueError("Action names must be strings")
        if not isinstance(action, dict):
            raise ValueError(f"Action '{action_name}' must be an object")

        buttons = action.get("buttons", [])
        move_x = action.get("move_x", 0)
        move_y = action.get("move_y", 0)
        wheel = action.get("wheel", 0)
        repeat = action.get("repeat", 1)

        if not isinstance(buttons, list) or not all(isinstance(b, str) for b in buttons):
            raise ValueError(f"'{action_name}.buttons' must be a list of strings")
        if not isinstance(move_x, int):
            raise ValueError(f"'{action_name}.move_x' must be an integer")
        if not isinstance(move_y, int):
            raise ValueError(f"'{action_name}.move_y' must be an integer")
        if not isinstance(wheel, int):
            raise ValueError(f"'{action_name}.wheel' must be an integer")
        if not isinstance(repeat, int) or repeat < 1:
            raise ValueError(f"'{action_name}.repeat' must be an integer >= 1")

        normalized[action_name.upper()] = {
            "buttons": [b.upper() for b in buttons],
            "move_x": move_x,
            "move_y": move_y,
            "wheel": wheel,
            "repeat": repeat,
        }

    return normalized
