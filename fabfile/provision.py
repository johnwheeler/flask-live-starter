from fabric.api import task, sudo

from .constants import *


__all__ = ['system', 'certificate', 'database']


@task
def system():
    _system_update_upgrade()
    # firewall
    _install('ufw')
    _configure_firewall()
    # unattended upgrades
    _install('needrestart')
    _install('unattended-upgrades')
    sudo('cp /usr/share/unattended-upgrades/20auto-upgrades /etc/apt/apt.conf.d/20auto-upgrades')
    # python related
    _install('python-dev')
    _install('python-pip')
    _install('python-virtualenv')
    # wsgi
    _install('gunicorn')
    # httpd
    _install('nginx')
    # postgres
    pg_version = '9.6'
    _install('postgresql-{}'.format(pg_version))
    _install('postgresql-client-{}'.format(pg_version))
    _install('postgresql-server-dev-{}'.format(pg_version))
    _install('postgresql-contrib-{}'.format(pg_version))
    # certbot (letsencrypt)
    _install('python-certbot-nginx -t jessie-backports')


@task
def certificate():
    sudo('certbot --nginx --non-interactive --agree-tos --redirect --domain {} --domain {}.{} --email {}'.format(DOMAIN, SUBDOMAIN, DOMAIN, EMAIL))


@task
def database():
    sudo('createuser {} -P'.format(APP_NAME), user='postgres')
    sudo('createdb {} -O {}'.format(APP_NAME, APP_NAME), user='postgres')


def _system_update_upgrade():
    # backports
    sudo("sh -c 'echo deb http://ftp.us.debian.org/debian/ jessie-backports main >> /etc/apt/sources.list'")

    # postgresql
    sudo("sh -c 'echo deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main > /etc/apt/sources.list.d/pgdg.list'")
    sudo('wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -')

    sudo('apt-get update')
    sudo('apt-get upgrade -y')


def _install(pkg):
    sudo('DEBIAN_FRONTEND=noninteractive apt-get install {} -y'.format(pkg))


def _configure_firewall():
    sudo('ufw allow 80/tcp')
    sudo('ufw allow 22/tcp')
    sudo('ufw allow 443/tcp')
    sudo('ufw --force enable')
