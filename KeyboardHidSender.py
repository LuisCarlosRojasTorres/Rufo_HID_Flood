from __future__ import annotations

import time
from pathlib import Path
from typing import Dict, Iterable, List


MODIFIER_MAP: Dict[str, int] = {
    "LCTRL": 0x01,
    "LSHIFT": 0x02,
    "LALT": 0x04,
    "LGUI": 0x08,
    "RCTRL": 0x10,
    "RSHIFT": 0x20,
    "RALT": 0x40,
    "RGUI": 0x80,
    "CTRL": 0x01,
    "SHIFT": 0x02,
    "ALT": 0x04,
    "GUI": 0x08,
    "WIN": 0x08,
}

KEYCODE_MAP: Dict[str, int] = {
    "A": 0x04,
    "B": 0x05,
    "C": 0x06,
    "D": 0x07,
    "E": 0x08,
    "F": 0x09,
    "G": 0x0A,
    "H": 0x0B,
    "I": 0x0C,
    "J": 0x0D,
    "K": 0x0E,
    "L": 0x0F,
    "M": 0x10,
    "N": 0x11,
    "O": 0x12,
    "P": 0x13,
    "Q": 0x14,
    "R": 0x15,
    "S": 0x16,
    "T": 0x17,
    "U": 0x18,
    "V": 0x19,
    "W": 0x1A,
    "X": 0x1B,
    "Y": 0x1C,
    "Z": 0x1D,
    "1": 0x1E,
    "2": 0x1F,
    "3": 0x20,
    "4": 0x21,
    "5": 0x22,
    "6": 0x23,
    "7": 0x24,
    "8": 0x25,
    "9": 0x26,
    "0": 0x27,
    "ENTER": 0x28,
    "ESC": 0x29,
    "BACKSPACE": 0x2A,
    "TAB": 0x2B,
    "SPACE": 0x2C,
    "-": 0x2D,
    "=": 0x2E,
    "[": 0x2F,
    "]": 0x30,
    "\\": 0x31,
    ";": 0x33,
    "'": 0x34,
    "`": 0x35,
    ",": 0x36,
    ".": 0x37,
    "/": 0x38,
    "CAPSLOCK": 0x39,
    "F1": 0x3A,
    "F2": 0x3B,
    "F3": 0x3C,
    "F4": 0x3D,
    "F5": 0x3E,
    "F6": 0x3F,
    "F7": 0x40,
    "F8": 0x41,
    "F9": 0x42,
    "F10": 0x43,
    "F11": 0x44,
    "F12": 0x45,
    "PRINTSCREEN": 0x46,
    "SCROLLLOCK": 0x47,
    "PAUSE": 0x48,
    "INSERT": 0x49,
    "HOME": 0x4A,
    "PAGEUP": 0x4B,
    "DELETE": 0x4C,
    "END": 0x4D,
    "PAGEDOWN": 0x4E,
    "RIGHT": 0x4F,
    "LEFT": 0x50,
    "DOWN": 0x51,
    "UP": 0x52,
}


class KeyboardHidSender:
    """Sends USB HID keyboard reports to a HID gadget endpoint."""

    def __init__(self, device_path: str = "/dev/hidg0", dry_run: bool = False) -> None:
        self.device_path = Path(device_path)
        self.dry_run = dry_run

    def _modifier_byte(self, modifiers: Iterable[str]) -> int:
        value = 0
        for modifier in modifiers:
            if modifier not in MODIFIER_MAP:
                raise KeyError(f"Unknown modifier: {modifier}")
            value |= MODIFIER_MAP[modifier]
        return value

    def _keycode_bytes(self, keys: Iterable[str]) -> List[int]:
        keycodes: List[int] = []
        for key in keys:
            if key not in KEYCODE_MAP:
                raise KeyError(f"Unknown key: {key}")
            keycodes.append(KEYCODE_MAP[key])

        if len(keycodes) > 6:
            raise ValueError("A single HID report supports up to 6 concurrent keys")

        return keycodes + [0x00] * (6 - len(keycodes))

    def build_report(self, modifiers: Iterable[str], keys: Iterable[str]) -> bytes:
        mod = self._modifier_byte(modifiers)
        key_bytes = self._keycode_bytes(keys)
        return bytes([mod, 0x00, *key_bytes])

    def _write_report(self, report: bytes) -> None:
        if self.dry_run:
            print(f"[DRY-RUN] Report ({len(report)} bytes): {report.hex(' ')}")
            return

        if not self.device_path.exists():
            raise FileNotFoundError(
                f"HID device not found at {self.device_path}. "
                "Configure USB HID gadget first (e.g. /dev/hidg0)."
            )

        with self.device_path.open("wb", buffering=0) as hid_dev:
            hid_dev.write(report)

    def send_combination(self, modifiers: Iterable[str], keys: Iterable[str], hold_ms: int = 60) -> None:
        press_report = self.build_report(modifiers, keys)
        release_report = bytes([0x00] * 8)

        self._write_report(press_report)
        time.sleep(max(hold_ms, 0) / 1000)
        self._write_report(release_report)

    def send_named_combination(self, combinations: Dict[str, dict], combo_name: str, hold_ms: int = 60) -> None:
        combo_key = combo_name.upper()
        if combo_key not in combinations:
            available = ", ".join(sorted(combinations.keys()))
            raise KeyError(f"Combination '{combo_name}' not found. Available: {available}")

        combo = combinations[combo_key]
        self.send_combination(combo.get("modifiers", []), combo.get("keys", []), hold_ms=hold_ms)
