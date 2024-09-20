
import socket
import struct
import os
import json

def get_current_directory():
    """Returns the current execution directory."""
    return os.getcwd()

# Path to the configuration file in the current directory
CONFIG_FILE = os.path.join(get_current_directory(), "config_loader_ps4.json")

def create_config_file():
    """Creates a configuration file with the necessary information."""
    print("Creating a new configuration file.")
    ip = input("Please enter the PS4 IP address: ").strip()
    port = input("Please enter the TCP listener port (default 9020): ").strip() or "9020"
    
    # Default path is the current execution directory
    default_payload_path = os.path.join(get_current_directory(), "payload.bin")
    payload_path = input(f"Please enter the path to the payload file (default: {default_payload_path}): ").strip() or default_payload_path

    config = {
        "ip": ip,
        "port": int(port),
        "payload_path": payload_path
    }

    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
    
    print(f"Configuration successfully saved in {CONFIG_FILE}.")

def read_config_file():
    """Reads the configuration from the JSON file in the current directory."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return None

def save_config_file(config):
    """Saves modifications to the configuration file."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def prompt_configuration(config):
    """Asks if the user wants to modify the configuration details."""
    print("Current configuration:")
    print(f"IP Address: {config['ip']}")
    print(f"TCP Port: {config['port']}")
    print(f"Payload File: {config['payload_path']}")
    
    choice = input("Do you want to modify this information? (Press Enter for no / y for yes): ").strip()
    if choice.lower() == 'y':
        config['ip'] = input(f"New IP Address (current: {config['ip']}): ").strip() or config['ip']
        config['port'] = input(f"New TCP Port (current: {config['port']}): ").strip() or config['port']
        
        # Default path in the current execution directory if the user wants to change the path
        default_payload_path = os.path.join(get_current_directory(), "payload.bin")
        config['payload_path'] = input(f"New payload path (current: {config['payload_path']} - default: {default_payload_path}): ").strip() or config['payload_path']
        
        save_config_file(config)
    
    return config

def send_payload(ip, port, payload_path):
    """Sends the payload to the PS4."""
    # Read the payload
    with open(payload_path, 'rb') as f:
        payload = f.read()

    # Connect to the PS4 server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    
    # Send the payload size
    payload_size = struct.pack('<Q', len(payload))
    sock.sendall(payload_size)

    # Send the payload in chunks
    bytes_sent = 0
    while bytes_sent < len(payload):
        chunk_size = min(4096, len(payload) - bytes_sent)
        sock.sendall(payload[bytes_sent:bytes_sent + chunk_size])
        bytes_sent += chunk_size

    print(f"Payload successfully sent ({bytes_sent} bytes)")

    # Close the connection
    sock.close()

if __name__ == "__main__":
    # Read the configuration or create it if it doesn't exist
    config = read_config_file()
    if config is None:
        create_config_file()
        config = read_config_file()

    # Ask the user if they want to modify the information
    config = prompt_configuration(config)

    # Send the payload using the configuration information
    send_payload(config['ip'], int(config['port']), config['payload_path'])
