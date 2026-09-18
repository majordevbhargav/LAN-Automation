# LAN Automation

A Python-based network automation utility for collecting operational information from Cisco and Aruba/HP switches.

## Workflow

```text
Inventory
   |
   v
Device Connection
   |
   v
CLI Commands
   |
   v
Output Collection
   |
   v
Timestamped Reports
```

## Features

- Cisco IOS / IOS-XE support
- HP ProCurve / ArubaOS-Switch support
- Inventory-driven execution
- Multiple CLI commands
- Timestamped output
- Single-device targeting
- Credential input through secure prompts or environment variables

## Setup

```bash
pip install -r requirements.txt
```

Define devices in `inventory.yaml` without storing passwords in source control.

## Examples

```bash
python netdevice_runner.py -c "show run"
python netdevice_runner.py -c "show run" "show version" --save
python netdevice_runner.py -f commands.txt --save
python netdevice_runner.py -c "show run" --only core-switch-01
```

## Learning Direction

This repository represents the programmable step between manual CLI work and declarative Ansible automation.

It helped me practice:

- Device connectivity
- Network CLI automation
- Inventory design
- Output handling
- Multi-vendor workflows
- Automation safety

## Security

Never hardcode passwords. Use secure prompts, environment variables, or an approved secrets-management system.

Only automate infrastructure you are authorized to manage.

## Future Direction

- Parallel execution
- Configuration push
- Configuration diffing
- Structured parsing
- Automated validation
- Centralized reporting

## Author

**Dev Bhargav**

[GitHub](https://github.com/majordevbhargav) · [LinkedIn](https://www.linkedin.com/in/devbhargav100)
