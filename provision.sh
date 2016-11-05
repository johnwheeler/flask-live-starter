apt-get update
apt-get upgrade -y

# firewall
apt-get install ufw -y
ufw allow 80/tcp
ufw allow 22/tcp
ufw allow 443/tcp
ufw --force enable

# unattended upgrades
apt-get install needrestart -y
apt-get install unattended-upgrades -y
cp /usr/share/unattended-upgrades/20auto-upgrades /etc/apt/apt.conf.d/20auto-upgrades

# python related
apt-get install python-dev -y
apt-get install python-pip -y
apt-get install python-virtualenv -y

# python nice-to-haves
apt-get install libffi-dev -y
apt-get install libxml2-dev -y
apt-get install libxslt1-dev -y

# wsgi
apt-get install gunicorn -y

# httpd
apt-get install nginx -y

# postgres
sh -c 'echo deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
apt-get update
apt-get install postgresql-9.6 -y
apt-get install postgresql-client-9.6 -y
apt-get install postgresql-server-dev-9.6 -y
apt-get install postgresql-contrib-9.6 -y

apt-get clean
