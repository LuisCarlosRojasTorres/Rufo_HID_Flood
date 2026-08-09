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
    "ALTGR": 0x40,
    "ALT_GR": 0x40,
    "ISO_LEVEL3_SHIFT": 0x40,
    "GUI": 0x08,
    "WIN": 0x08,
    "WINDOWS": 0x08,
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
    "MINUS": 0x2D,
    "-": 0x2D,
    "EQUAL": 0x2E,
    "=": 0x2E,
    "LEFTBRACE": 0x2F,
    "[": 0x2F,
    "RIGHTBRACE": 0x30,
    "]": 0x30,
    "BACKSLASH": 0x31,
    "\\": 0x31,
    "NONUSHASH": 0x32,
    "SEMICOLON": 0x33,
    ";": 0x33,
    "APOSTROPHE": 0x34,
    "'": 0x34,
    "GRAVE": 0x35,
    "`": 0x35,
    "COMMA": 0x36,
    ",": 0x36,
    "DOT": 0x37,
    ".": 0x37,
    "SLASH": 0x38,
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
    "NUMLOCK": 0x53,
    "KPSLASH": 0x54,
    "KPASTERISK": 0x55,
    "KPMINUS": 0x56,
    "KPPLUS": 0x57,
    "KPENTER": 0x58,
    "KP1": 0x59,
    "KP2": 0x5A,
    "KP3": 0x5B,
    "KP4": 0x5C,
    "KP5": 0x5D,
    "KP6": 0x5E,
    "KP7": 0x5F,
    "KP8": 0x60,
    "KP9": 0x61,
    "KP0": 0x62,
    "KPDOT": 0x63,
    "NONUSBACKSLASH": 0x64,
    "COMPOSE": 0x65,
    "POWER": 0x66,
    "KPEQUAL": 0x67,
    "F13": 0x68,
    "F14": 0x69,
    "F15": 0x6A,
    "F16": 0x6B,
    "F17": 0x6C,
    "F18": 0x6D,
    "F19": 0x6E,
    "F20": 0x6F,
    "F21": 0x70,
    "F22": 0x71,
    "F23": 0x72,
    "F24": 0x73,
    "OPEN": 0x74,
    "HELP": 0x75,
    "PROPS": 0x76,
    "FRONT": 0x77,
    "STOP": 0x78,
    "AGAIN": 0x79,
    "UNDO": 0x7A,
    "CUT": 0x7B,
    "COPY": 0x7C,
    "PASTE": 0x7D,
    "FIND": 0x7E,
    "MUTE": 0x7F,
    "VOLUMEUP": 0x80,
    "VOLUMEDOWN": 0x81,
    "LOCKINGCAPSLOCK": 0x82,
    "LOCKINGNUMLOCK": 0x83,
    "LOCKINGSCROLLLOCK": 0x84,
    "KPCOMMA": 0x85,
    "KPEQUALSIGN": 0x86,
    "INTL1": 0x87,
    "INTL2": 0x88,
    "INTL3": 0x89,
    "INTL4": 0x8A,
    "INTL5": 0x8B,
    "INTL6": 0x8C,
    "INTL7": 0x8D,
    "INTL8": 0x8E,
    "INTL9": 0x8F,
    "LANG1": 0x90,
    "LANG2": 0x91,
    "LANG3": 0x92,
    "LANG4": 0x93,
    "LANG5": 0x94,
    "LANG6": 0x95,
    "LANG7": 0x96,
    "LANG8": 0x97,
    "LANG9": 0x98,
    "ALTERASE": 0x99,
    "SYSREQ": 0x9A,
    "CANCEL": 0x9B,
    "CLEAR": 0x9C,
    "PRIOR": 0x9D,
    "RETURN": 0x9E,
    "SEPARATOR": 0x9F,
    "OUT": 0xA0,
    "OPER": 0xA1,
    "CLEARAGAIN": 0xA2,
    "CRSEL": 0xA3,
    "EXSEL": 0xA4,
}

CANONICAL_KEYS: List[str] = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
    "ENTER", "ESC", "BACKSPACE", "TAB", "SPACE",
    "MINUS", "EQUAL", "LEFTBRACE", "RIGHTBRACE", "BACKSLASH", "NONUSHASH",
    "SEMICOLON", "APOSTROPHE", "GRAVE", "COMMA", "DOT", "SLASH", "CAPSLOCK",
    "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
    "PRINTSCREEN", "SCROLLLOCK", "PAUSE", "INSERT", "HOME", "PAGEUP", "DELETE", "END", "PAGEDOWN",
    "RIGHT", "LEFT", "DOWN", "UP",
    "NUMLOCK", "KPSLASH", "KPASTERISK", "KPMINUS", "KPPLUS", "KPENTER",
    "KP1", "KP2", "KP3", "KP4", "KP5", "KP6", "KP7", "KP8", "KP9", "KP0", "KPDOT",
    "NONUSBACKSLASH", "COMPOSE", "POWER", "KPEQUAL",
    "F13", "F14", "F15", "F16", "F17", "F18", "F19", "F20", "F21", "F22", "F23", "F24",
    "OPEN", "HELP", "PROPS", "FRONT", "STOP", "AGAIN", "UNDO", "CUT", "COPY", "PASTE", "FIND",
    "MUTE", "VOLUMEUP", "VOLUMEDOWN", "LOCKINGCAPSLOCK", "LOCKINGNUMLOCK", "LOCKINGSCROLLLOCK",
    "KPCOMMA", "KPEQUALSIGN", "INTL1", "INTL2", "INTL3", "INTL4", "INTL5", "INTL6", "INTL7", "INTL8", "INTL9",
    "LANG1", "LANG2", "LANG3", "LANG4", "LANG5", "LANG6", "LANG7", "LANG8", "LANG9",
    "ALTERASE", "SYSREQ", "CANCEL", "CLEAR", "PRIOR", "RETURN", "SEPARATOR", "OUT", "OPER", "CLEARAGAIN", "CRSEL", "EXSEL"
]


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
