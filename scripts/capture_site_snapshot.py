from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Start the local Streamlit app and save a full-page website snapshot."
    )
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--port", type=int, default=8511)
    parser.add_argument("--width", type=int, default=1440)
    parser.add_argument("--height", type=int, default=2200)
    parser.add_argument("--wait-ms", type=int, default=1800)
    return parser.parse_args()


def wait_for_server(url: str, timeout_seconds: int = 45) -> None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2):
                return
        except (urllib.error.URLError, ConnectionError):
            time.sleep(0.5)
    raise TimeoutError(f"Timed out waiting for {url}")


def terminate_process(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return

    process.send_signal(signal.SIGTERM)
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    output = args.output.resolve()
    url = f"http://127.0.0.1:{args.port}"

    env = os.environ.copy()
    env.setdefault("BROWSER", "none")

    command = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "app.py",
        "--server.headless",
        "true",
        "--server.port",
        str(args.port),
        "--server.fileWatcherType",
        "none",
    ]

    output.parent.mkdir(parents=True, exist_ok=True)
    process = subprocess.Popen(
        command,
        cwd=root,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
    )

    try:
        wait_for_server(url)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": args.width, "height": args.height})
            page.goto(url, wait_until="networkidle")
            page.wait_for_selector('[data-testid="stAppViewContainer"]')
            page.wait_for_timeout(args.wait_ms)
            page.screenshot(path=str(output), full_page=True)
            browser.close()
    finally:
        terminate_process(process)

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
