#!/usr/bin/env python3

import sys
import json
import socket
import os

SOCKET_PATH = "/tmp/mpvsocket"
FLUX_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "radios.json")

def load_flux():
    with open(FLUX_FILE) as f:
        return json.load(f)

def list_flux():
    flux = load_flux()
    print(f"{'COMMANDE':8} {'NOM':20} URL")
    print("-" * 50)
    for cmd, infos in flux.items():
        print(f"{cmd:8} {infos['nom']:20} {infos['url']}")

def play_flux(nom):
    flux = load_flux()

    if nom not in flux:
        print(f"Flux inconnu: {nom}", file=sys.stderr)
        sys.exit(1)

    url = flux[nom]["url"]
    commande = json.dumps({"command": ["loadfile", url, "replace"]}) + "\n"

    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect(SOCKET_PATH)
        s.sendall(commande.encode())

def main():
    if len(sys.argv) != 2:
        print("Usage: radio-select.py <nom_du_flux> | radio-select.py --list", file=sys.stderr)
        sys.exit(1)

    arg = sys.argv[1]

    if arg == "--list":
        list_flux()
        return

    play_flux(arg)

if __name__ == "__main__":
    main()