# Net-Flux
Ultra simple signage boards in the local or public network

#### Objective:
Mainly signage boards, but also publish and/or receive content from other machines on the local or public network.<br>
The contents are in fact complete or partial screenshots.br>
The machines are clients and/or servers located indifferently on the local or public network<br>
A simple browser and a local IP will be enough to manage this matter.

#### Principle
There are 2 operating modes:<br>

 - Simple local publication

    -- A server machine publishes its screen locally in http://0.0.0.0:8080
    -- Clients view in http://ip-du-server:8080

 - Publication by MQTT messaging

    -- Client machines listen on the local address http://127.0.0.1:8080
    -- Machines that publish their screen execute the capture service

There are 3 services:<br>
 - Simple local publication: ./webserver --handle capture

 - MQTT messaging clients: ./webserver --handle monitor

 - Publication by MQTT messaging, screenshot: ./snoop.py

Machines can be both listening or being listened to.<br>
Under Linux, supervisor will be used to start or stop these services

#### Machines used
- Linux machines preferred, but not mandatory.
- Raspberry pi 3, 4 5 are ideal.

#### Installation

#### Operation