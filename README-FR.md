# Net-Flux
Panneaux de signalisation ultra simple sur réseau local ou public

#### Objectif:
Panneaux de signalisation principalement, mais aussi publier et/ou recevoir des contenus issus d'autres machines sur le réseau local ou public.<br>
Les contenus sont en fait des captures d'écrans complètes ou partielles.br>
Les machines sont clientes et/ou serveurs situées indifféremment sur le réseau local ou public<br>
Un simple navigateur et une ip locale suffiont pour gérer cette affaire.

#### Principe
Il y a 2 modes de fonctionnement:<br>
 
- Publication locale simpl
    - Une machine serveur, publie son écran localement en http://0.0.0.0:8080
    - Les clients visionnent en http://ip-du-server:8080

- Publication par messagerie MQTT
    - Les machines clientes écoutent sur l'adresse locale http://127.0.0.1:8080
    - Les machines qui publient leur écran exécutent le service de capture 
     
Il y a 3 services:<br>

- Publication local simple: ./webserver --handle capture
 
- Clients de messagerie MQTT:  ./webserver --handle monitor
 
- Publication par messagerie MQTT, capture d'écran: ./snoop.py

Les machines peuvent être à la fois en écoute ou être écoutée.<br>
Sous Linux on utilisera supervisor pour lancer ou stopper ces services<br>


#### Machines utilisées

- Machines sous Linux de préférence, mais ce n'est pas obligatoire.
- Raspberry pi 3, 4 5 sont l'idéal. 
- Firefox, Chromium, Chrome et dérivés sont conseillés

#### Installation
Cloner ou télécharger le code depuis https://github.com/deunix-educ/Net-Flux

        $> git clone git@github.com:deunix-educ/Net-Flux.git
        ou
        $> tar xzfv Net-Flux-main.zip
        $> mv Net-Flux-main Net-Flux
        
        $> cd Net-Flux
- Dans répertoire etc
    - bin quelques utilitaires
    - conf exemple de configuration pour un raspberry pi4
    - install  exemple d'installation système pour un raspberry pi4
- Installer les packages suivants:
        $> sudo apt update
        $> sudo apt -y install build-essential git supervisor
        $> sudo apt -y python3-dev python3-pip python3-venv chromium-chromedriver
        $> sudo cp /etc/supervisor/supervisord.conf /etc/supervisor/supervisord.conf.old
        $> sudo cat >> /etc/supervisor/supervisord.conf << EOF
        [inet_http_server]
        port=*:9001
        username=root
        password=toor
        EOF
- Changer les droits des fichiers suivants
        $> chmod +x netflux/*.py
        $> chmod +x etc/bin/*.sh
- Installer L'environnement virtuel python (dans .venv)
        $> etc/bin/venv-install etc/install/requirements.txt
- Enfin installer le fichier de configuration service supervisor
        $> sudo cp etc/conf/netflux_service.conf /etc/supervisor/conf.d/
        $> sudo supervisorctl reread && sudo supervisorctl update

#### Fonctionnement 
Tester à la main.
        $> cd netflux
- La configuration des services ce trouve dans config_example.yaml





