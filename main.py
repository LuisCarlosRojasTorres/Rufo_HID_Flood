import argparse
from pathlib import Path

from HidLoader import load_hid_combinations
from KeyboardHidSender import KeyboardHidSender


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Send keyboard HID combinations through USB HID gadget endpoint"
    )
    parser.add_argument(
        "combo",
        help="Combination name from JSON (example: CTRL_ALT_DELETE)",
    )
    parser.add_argument(
        "--json",
        default="data/keyboard_combinations.json",
        help="Path to the combinations JSON file",
    )
    parser.add_argument(
        "--device",
        default="/dev/hidg0",
        help="HID gadget device path",
    )
    parser.add_argument(
        "--hold-ms",
        default=60,
        type=int,
        help="How long to hold keys before release",
    )
    parser.add_argument(
        "--repeat",
        default=None,
        type=int,
        help="Override how many times to repeat the combination",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print HID reports without writing to USB device",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    combos = load_hid_combinations(Path(args.json))
    sender = KeyboardHidSender(device_path=args.device, dry_run=args.dry_run)
    sender.send_named_combination(combos, args.combo, hold_ms=args.hold_ms, repeat=args.repeat)
    print(f"Combination '{args.combo}' sent successfully.")


if __name__ == "__main__":
    main()
