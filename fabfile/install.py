from fabric.api import task, sudo
from fabric.contrib.files import sed
from fabric.context_managers import cd

from .constants import *


__all__ = ['system', 'certificate', 'postgres', 'redis']


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


@task
def postgres():
    # add postgres repository to apt
    sudo("sh -c 'echo deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main > /etc/apt/sources.list.d/pgdg.list'")
    sudo('wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -')
    sudo('apt-get update')

    # install postgresql components
    pg_version = '9.6'
    _install('postgresql-{}'.format(pg_version))
    _install('postgresql-client-{}'.format(pg_version))
    _install('postgresql-server-dev-{}'.format(pg_version))
    _install('postgresql-contrib-{}'.format(pg_version))


@task
def redis():
    # make required directories
    sudo('mkdir /etc/redis')
    sudo('mkdir /var/redis')
    sudo('mkdir /var/redis/6379')

    # download
    sudo('wget http://download.redis.io/redis-stable.tar.gz')
    # untar
    sudo('tar xzf redis-stable.tar.gz')

    with cd('redis-stable'):
        # make & make install
        sudo('make')
        sudo('make install')
        # copy system init script
        sudo('cp utils/redis_init_script /etc/init.d/redis_6379')
        # copy redis configuration file
        sudo('cp redis.conf /etc/redis/6379.conf')

    # edit the configuration file
    sed('/etc/redis/6379.conf', '^daemonize no$', 'daemonize yes', use_sudo=True)
    sed('/etc/redis/6379.conf', '^logfile ""$',
        'logfile /var/log/redis_6379.log', use_sudo=True)
    sed('/etc/redis/6379.conf', '^dir ./$',
        'dir /var/redis/6379', use_sudo=True)

    # # update script init links
    sudo('update-rc.d redis_6379 defaults')
    # start redis system service
    sudo('service redis_6379 start')

    # clean up
    sudo('rm -rf redis-stable')
    sudo('rm redis-stable.tar.gz')


@task
def certificate():
    _install('python-certbot-nginx -t jessie-backports')
    sudo('certbot --nginx --non-interactive --agree-tos --redirect --domain {} --domain {}.{} --email {}'
         .format(DOMAIN, SUBDOMAIN, DOMAIN, EMAIL))


def _system_update_upgrade():
    # backports
    sudo("sh -c 'echo deb http://ftp.us.debian.org/debian/ jessie-backports main >> /etc/apt/sources.list'")
    sudo('apt-get update')
    sudo('apt-get upgrade -y')


def _install(pkg):
    sudo('DEBIAN_FRONTEND=noninteractive apt-get install {} -y'.format(pkg))


def _configure_firewall():
    sudo('ufw allow 80/tcp')
    sudo('ufw allow 22/tcp')
    sudo('ufw allow 443/tcp')
    sudo('ufw --force enable')
