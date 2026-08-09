from __future__ import annotations

import time
from pathlib import Path
from typing import Dict, Iterable


BUTTON_MAP: Dict[str, int] = {
    "LEFT": 0x01,
    "RIGHT": 0x02,
    "MIDDLE": 0x04,
    "BACK": 0x08,
    "FORWARD": 0x10,
}


class MouseHidSender:
    """Sends USB HID mouse reports to a HID gadget endpoint."""

    def __init__(self, device_path: str = "/dev/hidg1", dry_run: bool = False) -> None:
        self.device_path = Path(device_path)
        self.dry_run = dry_run

    @staticmethod
    def _check_int8(value: int, field_name: str) -> None:
        if value < -127 or value > 127:
            raise ValueError(f"{field_name} must be in range [-127, 127]")

    def _buttons_byte(self, buttons: Iterable[str]) -> int:
        value = 0
        for button in buttons:
            if button not in BUTTON_MAP:
                raise KeyError(f"Unknown mouse button: {button}")
            value |= BUTTON_MAP[button]
        return value

    def build_report(self, buttons: Iterable[str], move_x: int = 0, move_y: int = 0, wheel: int = 0) -> bytes:
        self._check_int8(move_x, "move_x")
        self._check_int8(move_y, "move_y")
        self._check_int8(wheel, "wheel")
        return bytes([
            self._buttons_byte(buttons),
            move_x & 0xFF,
            move_y & 0xFF,
            wheel & 0xFF,
        ])

    def _write_report(self, report: bytes) -> None:
        if self.dry_run:
            print(f"[DRY-RUN] Mouse report ({len(report)} bytes): {report.hex(' ')}")
            return

        if not self.device_path.exists():
            raise FileNotFoundError(
                f"HID device not found at {self.device_path}. "
                "Configure USB HID gadget first (e.g. /dev/hidg1)."
            )

        with self.device_path.open("wb", buffering=0) as hid_dev:
            hid_dev.write(report)

    def send_action(
        self,
        buttons: Iterable[str],
        move_x: int = 0,
        move_y: int = 0,
        wheel: int = 0,
        hold_ms: int = 30,
        repeat: int = 1,
    ) -> None:
        if repeat < 1:
            raise ValueError("repeat must be >= 1")

        action_report = self.build_report(buttons, move_x=move_x, move_y=move_y, wheel=wheel)
        release_report = bytes([0x00, 0x00, 0x00, 0x00])

        for _ in range(repeat):
            self._write_report(action_report)
            time.sleep(max(hold_ms, 0) / 1000)
            self._write_report(release_report)

    def send_named_action(
        self,
        actions: Dict[str, dict],
        action_name: str,
        hold_ms: int = 30,
        repeat: int | None = None,
        safe_max_repeat: int | None = 20,
        allow_high_repeat: bool = False,
        print_timing: bool = True,
    ) -> None:
        action_key = action_name.upper()
        if action_key not in actions:
            available = ", ".join(sorted(actions.keys()))
            raise KeyError(f"Action '{action_name}' not found. Available: {available}")

        action = actions[action_key]
        action_repeat = int(action.get("repeat", 1))
        final_repeat = repeat if repeat is not None else action_repeat

        if (
            safe_max_repeat is not None
            and final_repeat > safe_max_repeat
            and not allow_high_repeat
        ):
            raise ValueError(
                f"Repeat {final_repeat} exceeds safe limit {safe_max_repeat}. "
                "Use allow_high_repeat to override."
            )

        start = time.perf_counter()
        self.send_action(
            action.get("buttons", []),
            move_x=int(action.get("move_x", 0)),
            move_y=int(action.get("move_y", 0)),
            wheel=int(action.get("wheel", 0)),
            hold_ms=hold_ms,
            repeat=final_repeat,
        )
        if print_timing:
            elapsed_ms = (time.perf_counter() - start) * 1000
            print(f"[TIMER] {action_key}: {elapsed_ms:.2f} ms")

    def send_all_actions(
        self,
        actions: Dict[str, dict],
        hold_ms: int = 30,
        repeat: int | None = None,
        safe_max_repeat: int | None = 20,
        allow_high_repeat: bool = False,
        between_ms: int = 0,
    ) -> None:
        batch_start = time.perf_counter()
        names = list(actions.keys())
        total = len(names)
        skipped = 0
        sent = 0
        for index, name in enumerate(names, start=1):
            action = actions[name]
            effective_repeat = repeat if repeat is not None else int(action.get("repeat", 1))
            if (
                safe_max_repeat is not None
                and effective_repeat > safe_max_repeat
                and not allow_high_repeat
            ):
                skipped += 1
                print(
                    f"[{index}/{total}] Skipped {name} "
                    f"(repeat={effective_repeat} > safe_max_repeat={safe_max_repeat})"
                )
                if between_ms > 0 and index < total:
                    time.sleep(between_ms / 1000)
                continue

            print(f"[{index}/{total}] Sending {name}")
            item_start = time.perf_counter()
            self.send_named_action(
                actions,
                name,
                hold_ms=hold_ms,
                repeat=repeat,
                safe_max_repeat=safe_max_repeat,
                allow_high_repeat=allow_high_repeat,
                print_timing=False,
            )
            item_elapsed_ms = (time.perf_counter() - item_start) * 1000
            print(f"[{index}/{total}] Done {name} in {item_elapsed_ms:.2f} ms")
            sent += 1
            if between_ms > 0 and index < total:
                time.sleep(between_ms / 1000)
        batch_elapsed_ms = (time.perf_counter() - batch_start) * 1000
        print(
            f"Batch done: sent={sent}, skipped={skipped}, total_time={batch_elapsed_ms:.2f} ms"
        )
