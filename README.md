# radio-select

Petit script pour jouer un flux radio dans une instance mpv (contrôle via socket Unix `/tmp/mpvsocket`).
Pré-requis : alsa-utils et mpv.
Un service mpv-radio.service doit exister pour fonctionner (exemple dans le dossier systemd, à adapter en fonction du hardware).
Le script permet de lancer le service et jouer un flux en une seule commande : python3 radio-select.py fip
Possibilité de lancer le service seul manuellement, de l'arrêter, ou de lancer le service et jouer un flux automatiquement au démarrage du système.


## Usage

    python3 radio-select.py fip
    python3 radio-select.py start | stop | status
    python3 radio-select.py --list

## Configuration

Les flux disponibles sont définis dans `radios.json` :

    {
      "fip": {"nom": "Radio FIP", "url": "https://..."}
    }

## Déploiement (systemd)

Installer alsa-utils et mpv

    sudo apt install alsa-utils
    sudo apt install mpv

Deux services sont fournis dans `systemd/` :

- `mpv-radio.service` : lance mpv en tâche de fond avec un socket IPC actif (attention à adapter --audio-device= !)
- `radio.service` : charge un flux par défaut au démarrage, une fois mpv-radio.service prêt (attend que le réseau soit réellement disponible avant de lancer la commande)

Installation de base :

    sudo cp systemd/*.service /etc/systemd/system/
    sudo systemctl daemon-reload

Pour un lancer le service mpv et charger un flux par défaut au lancement du système :

    sudo systemctl enable --now mpv-radio.service
    sudo systemctl enable --now radio.service