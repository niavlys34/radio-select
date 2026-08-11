# radio-select

Petit script pour changer de flux radio dans une instance mpv déjà lancée (contrôle via socket Unix `/tmp/mpvsocket`), sans passer par `socat`.

## Usage

    python3 radio-select.py fip
    python3 radio-select.py --list

## Configuration

Les flux disponibles sont définis dans `radios.json` :

    {
      "fip": {"nom": "Radio FIP", "url": "https://..."}
    }

## Déploiement (systemd)

Deux services sont fournis dans `systemd/` :

- `mpv-radio.service` : lance mpv en tâche de fond avec un socket IPC actif
- `radio.service` : charge un flux par défaut au démarrage, une fois mpv-radio.service prêt (attend que le réseau soit réellement disponible avant de lancer la commande)

Installation sur le serveur :

    sudo cp systemd/*.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable --now mpv-radio.service
    sudo systemctl enable --now radio.service