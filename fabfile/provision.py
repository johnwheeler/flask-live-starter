from fabric.api import task, sudo

from .constants import *


__all__ = ['certificate', 'firewall', 'database']


@task
def certificate():
    sudo('certbot --nginx --non-interactive --agree-tos --redirect --domain {} --domain {}.{} --email {}'
         .format(DOMAIN, SUBDOMAIN, DOMAIN, EMAIL))


@task
def firewall():
    # allow http
    sudo('ufw allow 80/tcp')
    # allow https
    sudo('ufw allow 443/tcp')
    # allow ssh
    sudo('ufw allow 22/tcp')
    # enable firewall
    sudo('ufw --force enable')


@task
def database():
    sudo('createuser {} -P'.format(APP_NAME), user='postgres')
    sudo('createdb {} -O {}'.format(APP_NAME, APP_NAME), user='postgres')
