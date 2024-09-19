# Net-Flux
Ultra simple signage boards in the local or public network

#### Objective:
Mainly signage boards, but also publish and/or receive content from other machines on the local or public network.<br>
The contents are in fact complete or partial screenshots.<br>
The machines are clients and/or servers located indifferently on the local or public network<br>
A simple browser and a local IP will be enough to manage this matter.

#### Principle
There are 2 operating modes:<br>

- Simple local publication
    - A server machine publishes its screen locally in http://0.0.0.0:8080
    - Clients view in http://ip-du-server:8080

- Publication by MQTT messaging
    - Client machines listen on the local address http://127.0.0.1:8080
    - Machines that publish their screen execute the capture service

There are 3 services:<br>
- Simple local publication: ./webserver --handle capture

- MQTT messaging clients: ./webserver --handle monitor

- Publication by MQTT messaging, screenshot: ./snoop.py

Machines can be both listening or being listened to.<br>
Under Linux, supervisor will be used to start or stop these services<br>
All scripts are in python3<br>
The display is done only from a single html file flux/web/index.html which is easily modifiable.

#### Machines used

 - Linux machines preferred, but not mandatory.
 - Raspberry pi 3, 4 5 are ideal.
 - Firefox, Chromium, Chrome and derivatives are recommended
 
###### About raspberry pi
Provide ssh access to install VNC. A connected screen is not necessary.<br>
All manipulations can then be done directly by VNC.

##### Preview with a raspberry pi4
The machine is in 192.168.1.10:8080<br>
In a console:<br>
 - Run ./webserver.py -- handle capture
 - or supervisor in a browser http://127.0.0.1:9001
 - Launch a presentation with LibreOffice Impress<br>
    - Clients follow this presentation in http://192.168.1.10:8080

 - Capture the webcam with VLC
    - viewing in http://192.168.1.10:8080<br>
    
etc...

#### Installation

Clone or download the code from https://github.com/deunix-educ/Net-Flux

        $> git clone git@github.com:deunix-educ/Net-Flux.git
        or
        $> tar xzfv Net-Flux-main.zip
        $> mv Net-Flux-main Net-Flux
        
        $> cd Net-Flux

- In etc directory
    - bin some utilities
    - conf example of configuration for a raspberry pi4
    - install example of system installation for a raspberry pi4

- Install the following packages:

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

- Install mosquitto if necessary on a machine on the local network

        $> sudo apt -y install mosquitto

- Otherwise use a public mqtt server

    - https://github.com/emqx/blog/blob/main/en/202111/popular-online-public-mqtt-brokers.md

- Change the rights of the following files

        $> chmod +x netflux/*.py
        $> chmod +x etc/bin/*.sh

- Install the python virtual environment (in .venv)

        $> etc/bin/venv-install etc/install/requirements.txt

- Finally install the service supervisor configuration file

        $> sudo cp etc/conf/netflux_service.conf /etc/supervisor/conf.d/
        $> sudo supervisorctl reread && sudo supervisorctl update

#### Operation
Test by hand.<br>

        $> cd netflux

- copy config_example.yaml

        $> cp config_example.yaml config.yaml

- Edit the services configuration from config.yaml

    - Complete the mqtt fields
    
    - Complete screen
        - fps x image/s
        - title screen title
        - display: blank or (x11 display: 0.0 for linux)
    
    - complete server
        - host: ip or 0.0.0.0 for any ip
        - port: 8080

#### Simple local publication
Local mode if the machine server/capture is in 192.168.1.10:8080<br>

        $> ./webserver --handle capture

Clients visit the page with chromium<br>

        http://192.168.1.10:8080

Clients can also launch chromium directly<br>
    
        $> ./browser.py --host 192.168.1.10 --port 8080

On the server machine we can launch the demonstration

        $> ./demo_webpage.py

#### Publication and capture by MQTT messaging

Publishing by MQTT messaging by screenshot<br>
On the machines that must publish,

 - Service to launch<br>

        ./snoop.py

MQTT messaging clients in 192.168.1.20:8080<br>

 - Service to start<br>

        ./webserver --handle monitor

 - Result with chromium<br>

    - on the server: http://127.0.0.1:8080
    
 - from a machine on the network: http://192.168.1.20:8080


