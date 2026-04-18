# Plato Ship Demo — Zeroshot Audit Guide

## Quick Start
```bash
# Docker
docker compose up -d
telnet localhost 4040

# Or directly
python server.py
```

## Rooms
Each room has a description and a system prompt (the "agent personality" for that room).
- `dock` — Harbor agent, greets visitors
- `ship` — First mate, vessel operations
- `hold` — Inventory manager
- `bridge` — Navigator, weather/radar
- `tavern` — Keeper, fleet news
- `backroom` — Dispatcher, jobs

## Commands
- `look` — room description
- `go <room>` — move to room
- `rooms` — list all rooms
- `examine` — see the room's system prompt
- `chat <msg>` — talk (placeholder for full PLATO)
- `status` — player info
- `help` — command list
- `quit` — disconnect

## For External Agent Testing
This demo is designed for zeroshot testing by external AI agents:
1. Agent connects via telnet
2. Agent discovers rooms and system prompts
3. Agent evaluates room coherence and navigation logic
4. Agent reports findings

No API keys needed. No external dependencies. Pure Python stdlib.
