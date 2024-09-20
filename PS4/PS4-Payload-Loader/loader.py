import socket
import struct
import os
import json

def chemin_execution_script():
    """Retourne le chemin du répertoire d'exécution actuel (le dossier courant)."""
    return os.getcwd()

# Chemin du fichier de configuration dans le dossier courant
CONFIG_FILE = os.path.join(chemin_execution_script(), "config_loader_ps4.json")

def creer_fichier_config():
    """Crée un fichier de configuration avec les informations nécessaires."""
    print("Création d'un nouveau fichier de configuration.")
    ip = input("Veuillez entrer l'adresse IP de la PS4 : ").strip()
    port = input("Veuillez entrer le port TCP du listener (par défaut 9020) : ").strip() or "9020"
    
    # Chemin par défaut proposé est le répertoire du script
    default_payload_path = os.path.join(chemin_execution_script(), "payload.bin")
    payload_path = input(f"Veuillez entrer le chemin vers le fichier de payload (par défaut: {default_payload_path}) : ").strip() or default_payload_path

    config = {
        "ip": ip,
        "port": int(port),
        "payload_path": payload_path
    }

    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
    
    print(f"Configuration enregistrée avec succès dans {CONFIG_FILE}.")

def lire_fichier_config():
    """Lit la configuration à partir du fichier JSON dans le dossier courant."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return None

def sauvegarder_fichier_config(config):
    """Sauvegarde les modifications dans le fichier de configuration."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def demander_configuration(config):
    """Demande si l'utilisateur veut modifier les informations de la configuration."""
    print("Configuration actuelle :")
    print(f"Adresse IP : {config['ip']}")
    print(f"Port TCP : {config['port']}")
    print(f"Fichier Payload : {config['payload_path']}")
    
    choix = input("Voulez-vous modifier ces informations ? (Entrer pour non / o pour oui) : ").
