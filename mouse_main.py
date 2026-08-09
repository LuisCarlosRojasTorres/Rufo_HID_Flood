import argparse
from pathlib import Path

from MouseHidSender import MouseHidSender
from MouseLoader import load_mouse_combinations


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Send mouse HID actions through USB HID gadget endpoint"
    )
    parser.add_argument(
        "action",
        nargs="?",
        default=None,
        help="Action name from JSON (example: LEFT_CLICK)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Send all actions from JSON sequentially",
    )
    parser.add_argument(
        "--json",
        default="data/mouse_combinations.json",
        help="Path to the mouse actions JSON file",
    )
    parser.add_argument(
        "--device",
        default="/dev/hidg1",
        help="HID gadget mouse device path",
    )
    parser.add_argument(
        "--hold-ms",
        default=30,
        type=int,
        help="How long to hold each action report before release",
    )
    parser.add_argument(
        "--repeat",
        default=None,
        type=int,
        help="Override how many times to repeat the action",
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
        help="Delay between actions when using --all",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print HID reports without writing to USB device",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.all and not args.action:
        raise SystemExit("Provide ACTION name or use --all")

    actions = load_mouse_combinations(Path(args.json))
    sender = MouseHidSender(device_path=args.device, dry_run=args.dry_run)
    safe_max_repeat = None if args.safe_max_repeat < 0 else args.safe_max_repeat

    if args.all:
        sender.send_all_actions(
            actions,
            hold_ms=args.hold_ms,
            repeat=args.repeat,
            safe_max_repeat=safe_max_repeat,
            allow_high_repeat=args.allow_high_repeat,
            between_ms=args.between_ms,
        )
        print("All mouse actions sent successfully.")
    else:
        sender.send_named_action(
            actions,
            args.action,
            hold_ms=args.hold_ms,
            repeat=args.repeat,
            safe_max_repeat=safe_max_repeat,
            allow_high_repeat=args.allow_high_repeat,
        )
        print(f"Mouse action '{args.action}' sent successfully.")


if __name__ == "__main__":
    main()
