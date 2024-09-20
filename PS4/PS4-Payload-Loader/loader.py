import socket

PS4_IP = "192.168.10.137"  # Remplace par l'IP de la PS4
PS4_PORT = 9090  # Port utilisé pour envoyer le payload
PAYLOAD_PATH = "payload.bin"  # Chemin vers ton fichier payload

with open(PAYLOAD_PATH, "rb") as f:
    payload = f.read()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((PS4_IP, PS4_PORT))
    s.sendall(payload)
    print("Payload envoyé avec succès.")

