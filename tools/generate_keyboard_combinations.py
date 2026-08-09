import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from KeyboardHidSender import CANONICAL_KEYS


MODIFIER_SETS = [
    [],
    ["SHIFT"],
    ["CTRL"],
    ["ALT"],
    ["ALTGR"],
    ["GUI"],
    ["CTRL", "SHIFT"],
    ["CTRL", "ALT"],
    ["CTRL", "ALTGR"],
    ["ALT", "SHIFT"],
    ["ALTGR", "SHIFT"],
    ["CTRL", "SHIFT", "ALT"],
    ["CTRL", "SHIFT", "ALTGR"],
]

REPEAT_COUNTS = [2, 3, 4, 5, 10, 20, 50, 100]
MODIFIER_ONLY = ["SHIFT", "CTRL", "ALT", "ALTGR", "GUI"]


def combo_name(modifiers: list[str], key: str) -> str:
    if not modifiers:
        return key
    return "_".join([*modifiers, key])


def build_combinations() -> dict[str, dict[str, list[str]]]:
    combos: dict[str, dict[str, list[str]]] = {}

    def add_combo(name: str, modifiers: list[str], keys: list[str], repeat: int = 1) -> None:
        entry: dict[str, list[str] | int] = {
            "modifiers": modifiers,
            "keys": keys,
        }
        if repeat > 1:
            entry["repeat"] = repeat
        combos[name] = entry

    for key in CANONICAL_KEYS:
        for modifiers in MODIFIER_SETS:
            name = combo_name(modifiers, key)
            add_combo(name, modifiers, [key], repeat=1)
            for repeat in REPEAT_COUNTS:
                add_combo(f"{name}_X{repeat}", modifiers, [key], repeat=repeat)

    for modifier in MODIFIER_ONLY:
        add_combo(modifier, [modifier], [], repeat=1)
        for repeat in REPEAT_COUNTS:
            add_combo(f"{modifier}_X{repeat}", [modifier], [], repeat=repeat)

    return combos


def main() -> None:
    output = ROOT / "data" / "keyboard_combinations.json"
    output.parent.mkdir(parents=True, exist_ok=True)

    combos = build_combinations()
    output.write_text(json.dumps(combos, indent=2), encoding="utf-8")
    print(f"Generated {len(combos)} combinations at {output}")


if __name__ == "__main__":
    main()
