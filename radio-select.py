#!/usr/bin/env python3

import sys
import json
import socket
import os
import subprocess
import time

SOCKET_PATH = "/tmp/mpvsocket"
FLUX_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "radios.json")
SERVICE = "mpv-radio.service"
SOCKET_TIMEOUT = 5 # secondes d'attente pour que le socket MPV apparaisse


def load_flux():
    with open(FLUX_FILE) as f:
        return json.load(f)


def list_flux():
    flux = load_flux()
    print(f"{'COMMANDE':8} {'NOM':20} URL")
    print("-" * 50)
    for cmd, infos in flux.items():
        print(f"{cmd:8} {infos['nom']:20} {infos['url']}")


def is_service_active():
    result = subprocess.run(
        ["systemctl", "is-active", "--quiet", SERVICE]
    )
    return result.returncode == 0


def start_service():
    subprocess.run(["sudo", "systemctl", "start", SERVICE], check=True)


def stop_service():
    subprocess.run(["sudo", "systemctl", "stop", SERVICE], check=True)


def ensure_service_running():
    if is_service_active():
        return
    print(f"{SERVICE} n'est pas actif, démarrage...")
    start_service()
    if not wait_for_socket():
        print("Le socket mpv n'est pas apparu à temps.", file=sys.stderr)
        sys.exit(1)


def cmd_status():
    if is_service_active():
        print(f"{SERVICE} : actif")
    else:
        print(f"{SERVICE} : inactif")


def wait_for_socket(timeout=SOCKET_TIMEOUT):
    start = time.time()
    while time.time() - start < timeout:
        if os.path.exists(SOCKET_PATH):
            return True
        time.sleep(0.2)
    return False


def cmd_run():
    if is_service_active():
        print(f"{SERVICE} est déjà actif.")
        return
    start_service()
    if wait_for_socket():
        print(f"{SERVICE} démarré.")
    else:
        print("Le socket mpv n'est pas apparu à temps.", file=sys.stderr)
        sys.exit(1)


def cmd_stop():
    if not is_service_active():
        print(f"{SERVICE} est déjà arrêté.")
        return
    stop_service()
    print(f"{SERVICE} arrêté.")


def play_flux(nom):
    flux = load_flux()

    if nom not in flux:
        print(f"Flux inconnu: {nom}", file=sys.stderr)
        sys.exit(1)

    ensure_service_running()

    url = flux[nom]["url"]
    commande = json.dumps({"command": ["loadfile", url, "replace"]}) + "\n"

    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect(SOCKET_PATH)
        s.sendall(commande.encode())


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: radio-select.py <nom_du_flux> | --list | status | run | stop",
            file=sys.stderr,
        )
        sys.exit(1)

    arg = sys.argv[1]

    if arg == "--list":
        list_flux()
    elif arg == "status":
        cmd_status()
    elif arg == "run":
        cmd_run()
    elif arg == "stop":
        cmd_stop()
    else:
        play_flux(arg)


if __name__ == "__main__":
    main()
