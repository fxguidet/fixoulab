import socket
import struct
import os
import json

# Chemin du fichier de configuration
CONFIG_FILE = "config_loader_ps4.json"

def chemin_execution_script():
    """Retourne le chemin du répertoire dans lequel s'exécute le script."""
    return os.path.dirname(os.path.abspath(__file__))

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
    
    print("Configuration enregistrée avec succès.")

def lire_fichier_config():
    """Lit la configuration à partir du fichier JSON."""
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
    
    choix = input("Voulez-vous modifier ces informations ? (Entrer pour non / o pour oui) : ").strip()
    if choix.lower() == 'o':
        config['ip'] = input(f"Nouvelle adresse IP (actuelle: {config['ip']}) : ").strip() or config['ip']
        config['port'] = input(f"Nouveau port TCP (actuel: {config['port']}) : ").strip() or config['port']
        
        # Proposer le chemin par défaut du répertoire d'exécution si l'utilisateur modifie le chemin
        default_payload_path = os.path.join(chemin_execution_script(), "payload.bin")
        config['payload_path'] = input(f"Nouveau chemin vers le payload (actuel: {config['payload_path']} - par défaut: {default_payload_path}) : ").strip() or config['payload_path']
        
        sauvegarder_fichier_config(config)
    
    return config

def send_payload(ip, port, payload_path):
    """Envoi du payload vers la PS4."""
    # Lecture du payload
    with open(payload_path, 'rb') as f:
        payload = f.read()

    # Connexion au serveur PS4
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    
    # Envoi de la taille du payload
    payload_size = struct.pack('<Q', len(payload))
    sock.sendall(payload_size)

    # Envoi du payload en morceaux
    bytes_sent = 0
    while bytes_sent < len(payload):
        chunk_size = min(4096, len(payload) - bytes_sent)
        sock.sendall(payload[bytes_sent:bytes_sent + chunk_size])
        bytes_sent += chunk_size

    print(f"Payload envoyé avec succès ({bytes_sent} octets)")

    # Fermeture de la connexion
    sock.close()

if __name__ == "__main__":
    # Lire la configuration ou la créer si elle n'existe pas
    config = lire_fichier_config()
    if config is None:
        creer_fichier_config()
        config = lire_fichier_config()

    # Demander à l'utilisateur s'il veut modifier les informations
    config = demander_configuration(config)

    # Envoyer le payload en utilisant les infos de la configuration
    send_payload(config['ip'], int(config['port']), config['payload_path'])

