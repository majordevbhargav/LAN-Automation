# LAN Automation

A Python-based network device command runner for collecting operational output from Cisco and Aruba/HP switches.

## Overview

The tool reads a device inventory, connects through Netmiko, executes one or more CLI commands, and can save timestamped output per device.

## Features

- Cisco IOS / IOS-XE support
- HP ProCurve / ArubaOS-Switch support
- Inventory-driven execution
- Multiple CLI commands per run
- Timestamped output files
- Single-device targeting
- Credential input through environment variables or a secure prompt

## Setup

```bash
pip install -r requirements.txt
```

Define devices in `inventory.yaml` without storing passwords in the inventory.

## Usage

Run one command:

```bash
python netdevice_runner.py -c "show run"
```

Run multiple commands and save results:

```bash
python netdevice_runner.py -c "show run" "show version" --save
```

Use a command file:

```bash
python netdevice_runner.py -f commands.txt --save
```

Target one device:

```bash
python netdevice_runner.py -c "show run" --only core-switch-01
```

## Security

Do not hardcode credentials. Use environment variables, prompts, or a proper secrets-management solution. Run the tool only against infrastructure you own or are authorized to manage.

## Future Direction

- Parallel execution
- Configuration push workflows
- Configuration diffing
- Structured output parsing
- Automated validation
- Ansible-based equivalent
- Centralized reporting

## Author

**Dev Bhargav**

- GitHub: https://github.com/majordevbhargav
- LinkedIn: https://www.linkedin.com/in/devbhargav100
