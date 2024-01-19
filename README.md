## EvasiveShellPython


## Avertissement
Les scripts fournis dans ce dépôt sont destinés uniquement à des fins éducatives et de recherche. L'utilisation de ces scripts à des fins malveillantes est illégale et contraire à l'éthique. L'auteur et les contributeurs de ce dépôt ne sont pas responsables de l'utilisation abusive de ces scripts.

## Script 1 : Reverse Evasive Shell Backdoor  ______ ATTACKER

### Description
Le premier script est un exemple de backdoor de shell inversé en Python. Il permet à un attaquant de prendre le contrôle d'une machine distante sur un réseau en ouvrant un shell à distance. Le script écoute sur un port et exécute des commandes sur la machine distante.

### Utilisation
1. Assurez-vous d'avoir Python installé sur votre machine.
2. Exécutez le script sur la machine cible.
3. Connectez-vous au script à l'aide d'un outil de connexion netcat ou un autre client approprié.
4. Utilisez le shell distant de manière responsable et légale.

## Script 2 : C2C Execution and ARP Spoofing ____VICTIM

### Description
Le deuxième script est une implémentation de base d'un outil de spoofing réseau et d'exécution de commandes. Il utilise l'ARP spoofing pour rediriger le trafic réseau de la victime vers l'attaquant, permettant ainsi à l'attaquant d'envoyer des commandes à la victime et de recevoir les réponses.

### Utilisation
1. Assurez-vous d'avoir Python installé, ainsi que la bibliothèque Scapy.
2. Exécutez le script en fournissant les informations requises, telles que l'adresse IP de la victime et l'adresse IP à usurper.
3. Le script commencera à envoyer des paquets de spoofing ARP.
4. Vous pourrez interagir avec la victime en envoyant des commandes et en recevant les réponses.

