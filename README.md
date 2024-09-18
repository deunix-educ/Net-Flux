# Net-Flux
Panneaux de signalisation ultra simple sur réseau local ou public

#### Objectif:
Panneaux de signalisation principalement, mais aussi publier et/ou recevoir des contenus issus d'autres machines sur le réseau local ou public.<br>
Les contenus sont en fait des captures d'écrans complètes ou partielles.<br>
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
    - install exemple d'installation système pour un raspberry pi4
    
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

- Installer mosquitto si besoin sur une machine du réseau local 

        $> sudo apt -y install mosquitto

- Sinon utiliser un serveur mqtt public
    
    - https://github.com/emqx/blog/blob/main/en/202111/popular-online-public-mqtt-brokers.md

- Changer les droits des fichiers suivants

        $> chmod +x netflux/*.py
        $> chmod +x etc/bin/*.sh

- Installer l'environnement virtuel python (dans .venv)

        $> etc/bin/venv-install etc/install/requirements.txt

- Enfin installer le fichier de configuration service supervisor

        $> sudo cp etc/conf/netflux_service.conf /etc/supervisor/conf.d/
        $> sudo supervisorctl reread && sudo supervisorctl update

#### Fonctionnement 
Tester à la main.<br>

        $> cd netflux

- copier config_example.yaml

        $> cp config_example.yaml config.yaml

- Editer la configuration des services depuis config.yaml

    - Compléter les champs de mqtt
    
    - Compléter screen
        - fps x image/s
        - title titre écran
        - display: blanc ou (x11 display :0.0 pour linux)
        
    - compléter server
        - host: ip ou 0.0.0.0 pour toute ip
        - port: 8080
  
#### Publication local simple
Mode local si la machine serveur/capture est en 192.168.1.10:8080<br>
        
        $> ./webserver --handle capture

Les clients visitent la page avec chromium<br>

        http://192.168.1.10:8080
    
Les clients peuvent lancer aussi directement chromium<br>
        
        $> ./browser.py --host 192.168.1.10 --port 8080

Sur la machine serveur on peut lancer la démonstration

        $> ./demo_webpage.py

#### Publication et capture par messagerie MQTT

Publication par messagerie MQTT par capture d'écran<br>
Sur les machines qui doivent publier, 

 - Service à lancer<br>
        
         ./snoop.py

Clients de messagerie MQTT en 192.168.1.20:8080<br>
 
 - Service à lancer<br>
   
        ./webserver --handle monitor

 - Résultat avec chromium<br>
    - sur le serveur: http://127.0.0.1:8080
    - à partir d'une machine sur le réseau: http://192.168.1.20:8080
