# Net-Flux
Panneaux de signalisation ultra simple sur réseau local ou public

#### Objectif:
Panneaux de signalisation principalement, mais aussi publier et/ou recevoir des contenus issus d'autres machines sur le réseau local ou public.<br>
Les contenus sont en fait des captures d'écrans complètes ou partielles.br>
Les machines sont clientes et/ou serveurs situées indifféremment sur le réseau local ou public<br>
Un simple navigateur et une ip locale suffiont pour gérer cette affaire.

#### Principe
Il y a 2 modes de fonctionnement:<br>
 
 - Publication locale simple
 
    -- Une machine serveur, publie son écran localement en http://0.0.0.0:8080
    -- Les clients visionnent en http://ip-du-server:8080
  
 - Publication par messagerie MQTT
   
    -- Les machines clientes écoutent sur l'adresse locale http://127.0.0.1:8080
    -- Les machines qui publient leur écran exécutent le service de capture 
     
Il y a 3 services:<br>
 - Publication local simple: ./webserver --handle capture
 
 - Clients de messagerie MQTT:  ./webserver --handle monitor
 
 - Publication par messagerie MQTT, capture d'écran: ./snoop.py

Les machines peuvent être à la fois en écoute ou être écoutée.<br>
Sous Linux on utilisera supervisor pour lancer ou stopper ces services


#### Machines utilisées
- Machines sous Linux de préférence, mais ce n'est pas obligatoire.
- Raspberry pi 3, 4 5 sont l'idéal. 



#### Installation




#### Fonctionnement 
