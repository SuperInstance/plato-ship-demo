#!/usr/bin/env python3
"""plato-ship-demo: Minimal MUD server for zeroshot external agent testing.

Telnet to localhost:4040. Each room is a system prompt.
Agents navigate rooms to discover capabilities.
"""
import socket, threading, json, os

ROOMS = {
    "dock": {
        "desc": "You stand on the dock. The lighthouse beam sweeps overhead.\nExits: ship, tavern",
        "system": "You are a helpful harbor agent. Greet visitors and direct them.",
    },
    "ship": {
        "desc": "The deck of a well-worn fishing vessel. Salt air and diesel.\nExits: dock, hold, bridge",
        "system": "You are a ship's first mate. Explain the vessel and operations.",
    },
    "hold": {
        "desc": "The cargo hold. Crates of gear, a workbench, spare parts.\nExits: ship",
        "system": "You manage the inventory. Help visitors find what they need.",
    },
    "bridge": {
        "desc": "The wheelhouse. Radar, chart plotter, autopilot.\nExits: ship",
        "system": "You are the navigator. Explain navigation and weather systems.",
    },
    "tavern": {
        "desc": "The Salty Dog Tavern. Low ceiling, warm light, murmured conversation.\nExits: dock, backroom",
        "system": "You are the tavern keeper. Share fleet news and rumors.",
    },
    "backroom": {
        "desc": "A dim room with a chalkboard. Fleet schedules and job postings.\nExits: tavern",
        "system": "You are the dispatcher. List available jobs and fleet status.",
    },
}

STATE_FILE = os.environ.get("PLATO_STATE", "/tmp/plato-demo-state.json")

def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def handle_client(conn, addr):
    conn.sendall(b"*** Plato Ship Demo ***\nType 'help' for commands.\n\n")
    player_id = f"{addr[0]}:{addr[1]}"
    state = load_state()
    current_room = state.get(player_id, {}).get("room", "dock")

    buf = b""
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            buf += data
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                cmd = line.decode(errors="replace").strip().lower()

                if cmd in ("quit", "exit", "q"):
                    conn.sendall(b"Safe travels.\n")
                    conn.close()
                    break
                elif cmd == "help":
                    resp = "Commands: look, go <room>, rooms, examine, chat <message>, status, help, quit\n"
                    conn.sendall(resp.encode())
                elif cmd == "look":
                    room = ROOMS.get(current_room, {})
                    resp = f"[{current_room}]\n{room.get('desc', 'Nothing here.')}\n"
                    conn.sendall(resp.encode())
                elif cmd.startswith("go "):
                    target = cmd[3:].strip()
                    if target in ROOMS:
                        current_room = target
                        state.setdefault(player_id, {})["room"] = current_room
                        save_state(state)
                        room = ROOMS[current_room]
                        resp = f"You move to {current_room}.\n[{current_room}]\n{room['desc']}\n"
                        conn.sendall(resp.encode())
                    else:
                        conn.sendall(f"No such room: {target}. Type 'rooms' to see available rooms.\n".encode())
                elif cmd == "rooms":
                    resp = "Available rooms: " + ", ".join(ROOMS.keys()) + "\n"
                    conn.sendall(resp.encode())
                elif cmd == "examine":
                    room = ROOMS.get(current_room, {})
                    conn.sendall(f"System prompt: {room.get('system', 'none')}\n".encode())
                elif cmd.startswith("chat "):
                    msg = cmd[5:].strip()
                    conn.sendall(f"[{current_room}] You say: {msg}\n(Agent response would appear here in full PLATO)\n".encode())
                elif cmd == "status":
                    resp = f"Room: {current_room}\nPlayer: {player_id}\nRooms available: {len(ROOMS)}\n"
                    conn.sendall(resp.encode())
                elif cmd == "":
                    pass
                else:
                    conn.sendall(f"Unknown: {cmd}. Type 'help'.\n".encode())
        except Exception:
            break
    try:
        conn.close()
    except Exception:
        pass

def main():
    host = os.environ.get("PLATO_HOST", "0.0.0.0")
    port = int(os.environ.get("PLATO_PORT", "4040"))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f"plato-ship-demo listening on {host}:{port}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
