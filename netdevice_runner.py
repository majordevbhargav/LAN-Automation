#!/usr/bin/env python3
"""
netdevice_runner.py

Run one or more CLI commands against a list of network devices
(Cisco IOS, HP/Aruba switches, etc.) and save or print the output.

WHY THIS DESIGN
----------------
- Devices live in inventory.yaml (host + vendor only - no secrets).
- Username/password are supplied at run time, either via environment
  variables or a masked prompt. They are never written to disk or
  hardcoded in this script or the inventory file.
- Uses Netmiko, which wraps Paramiko/SSH and knows the quirks of
  Cisco IOS, HP ProCurve, and ArubaOS-Switch CLIs.

BASIC USAGE
-----------
  # one command, printed to screen
  python netdevice_runner.py -c "show run"

  # several commands, saved to files instead of the screen
  python netdevice_runner.py -c "show run" "show version" --save

  # commands from a text file (one per line), saved to files
  python netdevice_runner.py -f commands.txt --save

  # only run against one device from the inventory
  python netdevice_runner.py -c "show run" --only core-switch-01

CREDENTIALS
-----------
Preferred: set environment variables before running, so nothing is
typed or stored in this session:

  export NET_USER=ram
  export NET_PASS='the real password'
  python netdevice_runner.py -c "show run"

If NET_USER / NET_PASS aren't set, the script will prompt for them
(password input is hidden, not echoed to the screen).

OUTPUT
------
--save writes one timestamped .txt file per device per run into
./output/, e.g. output/core-switch-01_20260901_143012.txt
Without --save, output just prints to the terminal.
"""

import argparse
import getpass
import os
import sys
from datetime import datetime
from pathlib import Path

import yaml
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException


INVENTORY_FILE = "inventory.yaml"
OUTPUT_DIR = Path("output")


def load_inventory(path: str = INVENTORY_FILE, only: str | None = None) -> list[dict]:
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    devices = data.get("devices", [])
    if only:
        devices = [d for d in devices if d["name"] == only]
        if not devices:
            sys.exit(f"No device named '{only}' found in {path}")
    return devices


def get_credentials() -> tuple[str, str]:
    user = os.environ.get("NET_USER") or input("Username: ")
    password = os.environ.get("NET_PASS") or getpass.getpass("Password: ")
    return user, password


def load_commands(args: argparse.Namespace) -> list[str]:
    if args.commands:
        return args.commands
    if args.file:
        with open(args.file, "r") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    sys.exit("No commands given. Use -c/--commands or -f/--file.")


def run_on_device(device: dict, username: str, password: str, commands: list[str]) -> str:
    conn_params = {
        "device_type": device["device_type"],
        "host": device["host"],
        "username": username,
        "password": password,
        # secret= is only needed if the device requires 'enable' for these commands;
        # uncomment and set NET_SECRET if so:
        # "secret": os.environ.get("NET_SECRET", password),
    }

    output_chunks = [f"=== {device['name']} ({device['host']}) ==="]
    try:
        with ConnectHandler(**conn_params) as conn:
            # conn.enable()  # uncomment if commands need privileged/enable mode
            for cmd in commands:
                output_chunks.append(f"\n--- {cmd} ---")
                result = conn.send_command(cmd)
                output_chunks.append(result)
    except NetmikoAuthenticationException:
        output_chunks.append("\n[ERROR] Authentication failed - check username/password.")
    except NetmikoTimeoutException:
        output_chunks.append("\n[ERROR] Connection timed out - check host/IP and reachability.")
    except Exception as e:
        output_chunks.append(f"\n[ERROR] {type(e).__name__}: {e}")

    return "\n".join(output_chunks)


def main():
    parser = argparse.ArgumentParser(description="Run commands across network devices.")
    parser.add_argument("-c", "--commands", nargs="+", help="One or more commands, e.g. -c \"show run\" \"show version\"")
    parser.add_argument("-f", "--file", help="Path to a text file of commands, one per line")
    parser.add_argument("--inventory", default=INVENTORY_FILE, help="Path to inventory YAML file")
    parser.add_argument("--only", help="Run against a single device (match by 'name' in inventory)")
    parser.add_argument("--save", action="store_true", help="Save output to ./output/ instead of just printing")
    args = parser.parse_args()

    devices = load_inventory(args.inventory, only=args.only)
    commands = load_commands(args)
    username, password = get_credentials()

    if args.save:
        OUTPUT_DIR.mkdir(exist_ok=True)

    for device in devices:
        print(f"\nConnecting to {device['name']} ({device['host']})...")
        result = run_on_device(device, username, password, commands)

        if args.save:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_path = OUTPUT_DIR / f"{device['name']}_{timestamp}.txt"
            out_path.write_text(result)
            print(f"  Saved -> {out_path}")
        else:
            print(result)


if __name__ == "__main__":
    main()
