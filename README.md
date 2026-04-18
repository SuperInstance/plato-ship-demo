# plato-ship-demo

Minimal MUD server for zeroshot external agent testing.

Part of the [Cocapn fleet](https://github.com/SuperInstance). This is the public demo instance that external AI agents (Grok, Kimi, Claude, etc.) can connect to and audit without needing access to the private fleet.

## Architecture
- 6 rooms, each with a description and system prompt
- Pure Python stdlib (no dependencies)
- Telnet interface on port 4040
- Persistent player state via JSON file
- Docker-ready

## Why
The main plato-ship is private. External model sandboxes (Grok, Kimi) block outbound connections. This demo gives them something to test against — a self-contained, forkable MUD that demonstrates the room-as-system-prompt pattern.

## Run
```bash
python server.py                    # direct
docker compose up -d                # docker
telnet localhost 4040               # connect
```

## Test It
```
$ telnet localhost 4040
*** Plato Ship Demo ***
Type 'help' for commands.

> look
[dock]
You stand on the dock. The lighthouse beam sweeps overhead.
Exits: ship, tavern

> go ship
You move to ship.
[ship]
The deck of a well-worn fishing vessel. Salt air and diesel.
Exits: dock, hold, bridge

> examine
System prompt: You are a ship's first mate. Explain the vessel and operations.

> rooms
Available rooms: dock, ship, hold, bridge, tavern, backroom

> quit
Safe travels.
```

## Fleet Context
- **Full PLATO**: [SuperInstance/plato-ship](https://github.com/SuperInstance/plato-ship) (private)
- **Subcontractor API**: room-as-system-prompt at scale (2,501+ rooms)
- **Training**: [SuperInstance/plato-ml](https://github.com/SuperInstance/plato-ml)
- **Research**: [SuperInstance/flux-research](https://github.com/SuperInstance/flux-research)
