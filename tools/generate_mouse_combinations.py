import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REPEAT_COUNTS = [2, 3, 4, 5, 10, 20, 50, 100]

BUTTON_SETS = {
    "LEFT_CLICK": ["LEFT"],
    "RIGHT_CLICK": ["RIGHT"],
    "MIDDLE_CLICK": ["MIDDLE"],
    "BACK_CLICK": ["BACK"],
    "FORWARD_CLICK": ["FORWARD"],
    "LEFT_RIGHT_CLICK": ["LEFT", "RIGHT"],
    "LEFT_MIDDLE_CLICK": ["LEFT", "MIDDLE"],
    "RIGHT_MIDDLE_CLICK": ["RIGHT", "MIDDLE"],
}

MOVE_ACTIONS = {
    "MOVE_UP_10": (0, -10),
    "MOVE_DOWN_10": (0, 10),
    "MOVE_LEFT_10": (-10, 0),
    "MOVE_RIGHT_10": (10, 0),
    "MOVE_UP_50": (0, -50),
    "MOVE_DOWN_50": (0, 50),
    "MOVE_LEFT_50": (-50, 0),
    "MOVE_RIGHT_50": (50, 0),
    "MOVE_UP_LEFT_20": (-20, -20),
    "MOVE_UP_RIGHT_20": (20, -20),
    "MOVE_DOWN_LEFT_20": (-20, 20),
    "MOVE_DOWN_RIGHT_20": (20, 20),
}

SCROLL_ACTIONS = {
    "SCROLL_UP_1": 1,
    "SCROLL_DOWN_1": -1,
    "SCROLL_UP_3": 3,
    "SCROLL_DOWN_3": -3,
    "SCROLL_UP_10": 10,
    "SCROLL_DOWN_10": -10,
}


def add_with_repeats(
    actions: dict[str, dict],
    base_name: str,
    buttons: list[str],
    move_x: int,
    move_y: int,
    wheel: int,
) -> None:
    actions[base_name] = {
        "buttons": buttons,
        "move_x": move_x,
        "move_y": move_y,
        "wheel": wheel,
    }
    for repeat in REPEAT_COUNTS:
        actions[f"{base_name}_X{repeat}"] = {
            "buttons": buttons,
            "move_x": move_x,
            "move_y": move_y,
            "wheel": wheel,
            "repeat": repeat,
        }


def build_mouse_actions() -> dict[str, dict]:
    actions: dict[str, dict] = {}

    for name, buttons in BUTTON_SETS.items():
        add_with_repeats(actions, name, buttons, 0, 0, 0)

    for name, movement in MOVE_ACTIONS.items():
        add_with_repeats(actions, name, [], movement[0], movement[1], 0)

    for name, wheel in SCROLL_ACTIONS.items():
        add_with_repeats(actions, name, [], 0, 0, wheel)

    add_with_repeats(actions, "DRAG_LEFT_START", ["LEFT"], 0, 0, 0)
    add_with_repeats(actions, "DRAG_RIGHT_START", ["RIGHT"], 0, 0, 0)

    return actions


def main() -> None:
    output = ROOT / "data" / "mouse_combinations.json"
    output.parent.mkdir(parents=True, exist_ok=True)

    actions = build_mouse_actions()
    output.write_text(json.dumps(actions, indent=2), encoding="utf-8")
    print(f"Generated {len(actions)} mouse actions at {output}")


if __name__ == "__main__":
    main()
