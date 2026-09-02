# Network Device Command Runner

Run CLI commands (e.g. `show run`) across a list of Cisco and HP/Aruba
switches, and either print the output or save it to files.

## 1. Setup (on any machine with Python 3.9+)

```bash
pip install -r requirements.txt
```

## 2. Edit the inventory

Open `inventory.yaml` and list your devices. No passwords go in this
file - just name, IP, and device type:

```yaml
devices:
  - name: core-switch-01
    host: 10.5.1.20
    device_type: cisco_ios

  - name: aruba-switch-01
    host: 172.29.129.63
    device_type: aruba_os
```

Common `device_type` values:
| Vendor / platform            | device_type      |
|-------------------------------|------------------|
| Cisco IOS / IOS-XE            | `cisco_ios`      |
| HP ProCurve (older switches)  | `hp_procurve`    |
| HP Aruba (ArubaOS-Switch)     | `aruba_os`       |

## 3. Set credentials (don't hardcode them anywhere)

Either export them before running:

```bash
export NET_USER=ram
export NET_PASS='your-real-password'
```

...or just leave them unset and the script will prompt you, hiding
the password as you type it.

## 4. Run it

```bash
# One command, printed to the screen
python netdevice_runner.py -c "show run"

# Multiple commands, saved to files in ./output/
python netdevice_runner.py -c "show run" "show version" --save

# Commands from a file, one per line
python netdevice_runner.py -f commands.txt --save

# Only target one device
python netdevice_runner.py -c "show run" --only core-switch-01
```

Saved files land in `./output/`, named like
`core-switch-01_20260901_143012.txt` - one file per device per run,
easy to open in Notepad or any text editor.

## Ideas for next steps (once the basics feel solid)

- **Enable mode**: if your switches need `enable` before some
  commands work, uncomment the `secret=` line and `conn.enable()`
  call in the script and set a `NET_SECRET` env var.
- **Config push, not just show commands**: Netmiko's
  `send_config_set()` can push configuration changes the same way
  this script pulls output - useful for standardizing VLANs, ACLs,
  etc. across many switches at once.
- **Parallel execution**: right now devices run one after another;
  for a large fleet, Netmiko plays well with Python's
  `concurrent.futures.ThreadPoolExecutor` to run them in parallel.
- **Diffing configs over time**: since each run is saved with a
  timestamp, you could diff two runs against the same device to see
  what changed - handy for change control / audit trails.
- **Structured output**: some commands can be parsed into
  structured data (via `use_textfsm=True` in `send_command`, backed
  by ntc-templates) instead of raw text - useful if you want to feed
  results into a report or dashboard instead of just eyeballing text.
- **Secrets management**: for anything beyond personal/manual use,
  swap the env-var/prompt approach for a proper vault (Ansible
  Vault, HashiCorp Vault, or even a local `.env` file that's
  git-ignored) so credentials aren't retyped every run.
- **Ansible version**: if you'd rather standardize on Ansible long
  term (e.g. because your team already uses it, or you want to layer
  in config management, not just show commands), this same idea maps
  cleanly onto `cisco.ios` and `arubanetworks.aos_switch` Ansible
  collections with an inventory file and Ansible Vault for
  credentials. Happy to build that version if useful.

## Security note

The IPs, username, and password you shared earlier are real-looking
credentials for production switches - I did not put the password
anywhere in these files. Please treat that password as something to
rotate if it was ever pasted somewhere outside this chat, and always
supply it via the environment variable or the prompt, never by
editing it into a script.
