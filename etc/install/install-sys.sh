#!/bin/bash
if [ $EUID -ne 0 ]; then
  echo "root install only: # $0" 1>&2
  exit 1
fi

apt update
#apt upgrade

apt -y install build-essential git supervisor
apt -y install python3-dev python3-pip python3-venv chromium-chromedriver

# local certification mkcert
apt -y install libnss3-tools

# supervisor http access
#

if [ ! -e "/etc/supervisor/supervisord.conf.old" ]; then
cp /etc/supervisor/supervisord.conf /etc/supervisor/supervisord.conf.old
cat >> /etc/supervisor/supervisord.conf << EOF
[inet_http_server]
port=*:9001
username=root
password=toor
EOF
fi

# local certification
# ex:
# mkcert example.com "*.example.com" example.test localhost 127.0.0.1 ::1
# Choose mkcert version
#
#wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.4/mkcert-v1.4.4-linux-amd64
wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.4/mkcert-v1.4.4-linux-arm
#wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.4/mkcert-v1.4.4-linux-arm64
mv mkcert-v1.4.4-linux-arm /usr/local/bin/mkcert
chmod +x /usr/local/bin/mkcert

