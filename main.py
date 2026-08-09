import argparse
from pathlib import Path

from HidLoader import load_hid_combinations
from KeyboardHidSender import KeyboardHidSender
from MouseHidSender import MouseHidSender
from MouseLoader import load_mouse_combinations


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Send keyboard or mouse HID actions through USB HID gadget endpoint"
    )
    parser.add_argument(
        "combo",
        nargs="?",
        default=None,
        help="Combination name from JSON (example: CTRL_ALT_DELETE)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Send all entries from JSON sequentially",
    )
    parser.add_argument(
        "--target",
        choices=["keyboard", "mouse"],
        default="keyboard",
        help="Target HID type to send",
    )
    parser.add_argument(
        "--menu",
        action="store_true",
        help="Open interactive menu to choose keyboard or mouse batch sending",
    )
    parser.add_argument(
        "--json",
        default=None,
        help="Path to the JSON file (default depends on --target)",
    )
    parser.add_argument(
        "--device",
        default=None,
        help="HID gadget device path (default depends on --target)",
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
        "--safe-max-repeat",
        default=20,
        type=int,
        help="Safety cap for repeat count (set -1 to disable cap)",
    )
    parser.add_argument(
        "--allow-high-repeat",
        action="store_true",
        help="Allow repeat values above --safe-max-repeat",
    )
    parser.add_argument(
        "--between-ms",
        default=0,
        type=int,
        help="Delay between combinations when using --all",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print HID reports without writing to USB device",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.menu:
        print("Select batch mode:")
        print("1) Send all keyboard combinations")
        print("2) Send all mouse actions")
        selected = input("Option [1-2]: ").strip()
        if selected == "1":
            args.target = "keyboard"
            args.all = True
        elif selected == "2":
            args.target = "mouse"
            args.all = True
        else:
            raise SystemExit("Invalid menu option. Use 1 or 2.")

    if not args.all and not args.combo:
        raise SystemExit("Provide COMBO name or use --all")

    if args.target == "keyboard":
        json_path = args.json or "data/keyboard_combinations.json"
        device_path = args.device or "/dev/hidg0"
        combos = load_hid_combinations(Path(json_path))
        sender = KeyboardHidSender(device_path=device_path, dry_run=args.dry_run)
    else:
        json_path = args.json or "data/mouse_combinations.json"
        device_path = args.device or "/dev/hidg1"
        combos = load_mouse_combinations(Path(json_path))
        sender = MouseHidSender(device_path=device_path, dry_run=args.dry_run)

    safe_max_repeat = None if args.safe_max_repeat < 0 else args.safe_max_repeat
    if args.all:
        if args.target == "keyboard":
            sender.send_all_combinations(
                combos,
                hold_ms=args.hold_ms,
                repeat=args.repeat,
                safe_max_repeat=safe_max_repeat,
                allow_high_repeat=args.allow_high_repeat,
                between_ms=args.between_ms,
            )
            print("All keyboard combinations sent successfully.")
        else:
            sender.send_all_actions(
                combos,
                hold_ms=args.hold_ms,
                repeat=args.repeat,
                safe_max_repeat=safe_max_repeat,
                allow_high_repeat=args.allow_high_repeat,
                between_ms=args.between_ms,
            )
            print("All mouse actions sent successfully.")
    else:
        if args.target == "keyboard":
            sender.send_named_combination(
                combos,
                args.combo,
                hold_ms=args.hold_ms,
                repeat=args.repeat,
                safe_max_repeat=safe_max_repeat,
                allow_high_repeat=args.allow_high_repeat,
            )
            print(f"Keyboard combination '{args.combo}' sent successfully.")
        else:
            sender.send_named_action(
                combos,
                args.combo,
                hold_ms=args.hold_ms,
                repeat=args.repeat,
                safe_max_repeat=safe_max_repeat,
                allow_high_repeat=args.allow_high_repeat,
            )
            print(f"Mouse action '{args.combo}' sent successfully.")


if __name__ == "__main__":
    main()
