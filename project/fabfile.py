from os.path import basename, dirname, realpath

from fabric.api import env, local, sudo, put
from fabric.utils import puts
from fabric.contrib.files import exists
from fabric.context_managers import quiet

env.user = 'vagrant'
env.host_string = '192.168.33.10'
env.key_filename = '.vagrant/machines/default/virtualbox/private_key'


APP_NAME = basename(dirname(realpath(__file__)))

REMOTE_DEPLOY_DIR = '/var/www/html/{}'.format(APP_NAME)
REMOTE_VENV = '{}/venv'.format(REMOTE_DEPLOY_DIR)
REMOTE_APP_DIR = '{}/{}'.format(REMOTE_DEPLOY_DIR, APP_NAME)

LOCAL_ARCHIVE = './dist/{}.tar.gz'.format(APP_NAME)
REMOTE_ARCHIVE = '/root/{}.tar.gz'.format(APP_NAME)

LOCAL_GUNICORN_CONF_FILE = './etc/{}.gunicorn.conf'.format(APP_NAME)
REMOTE_GUNICORN_CONF_FILE = '/etc/gunicorn.d/{}.conf'.format(APP_NAME)

LOCAL_NGINX_CONF_FILE = './etc/{}.nginx.conf'.format(APP_NAME)
REMOTE_NGINX_CONF_FILE = '/etc/nginx/conf.d/{}.conf'.format(APP_NAME)


def dist():
    outdir = 'dist/{}'.format(APP_NAME)
    local('mkdir -p {}'.format(outdir))
    local('cp requirements.txt {}'.format(outdir))
    local('cp -R {} {}'.format(APP_NAME, outdir))
    local('find {} -name "*.pyc" -type f -delete'.format(outdir))
    local('tar czf dist/{}.tar.gz {}'.format(APP_NAME, outdir))


def deploy():
    if not exists(REMOTE_DEPLOY_DIR, use_sudo=True):
        sudo('mkdir {}'.format(REMOTE_DEPLOY_DIR))

    dist()
    _upload_and_extract_archive()
    _update_py_deps()
    sudo('chown -R root:www-data {}'.format(REMOTE_DEPLOY_DIR))
    sudo('chmod -R og-rwx,g+rxs {}'.format(REMOTE_DEPLOY_DIR))

    if not exists(REMOTE_NGINX_CONF_FILE):
        put(LOCAL_NGINX_CONF_FILE, REMOTE_NGINX_CONF_FILE, use_sudo=True)
        sudo('service nginx restart')

    if not exists(REMOTE_GUNICORN_CONF_FILE):
        put(LOCAL_GUNICORN_CONF_FILE, REMOTE_GUNICORN_CONF_FILE, use_sudo=True)

    sudo("service gunicorn restart")

    clean()


def clean():
    local('rm -rf ./dist')


def clean_remote():
    sudo('rm -rf {}'.format(REMOTE_DEPLOY_DIR))


def provision():
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
    # python nice-to-haves
    _install('libffi-dev')
    # wsgi
    _install('gunicorn')
    # httpd
    _install('nginx')
    # postgres
    _install('postgresql-9.6')
    _install('postgresql-client-9.6')
    _install('postgresql-server-dev-9.6')
    _install('postgresql-contrib-9.6')


def _upload_and_extract_archive():
    put(LOCAL_ARCHIVE, REMOTE_ARCHIVE, use_sudo=True)

    if not exists(REMOTE_DEPLOY_DIR, use_sudo=True):
        sudo('mkdir {}'.format(REMOTE_DEPLOY_DIR))

    sudo('rm -rf {}'.format(REMOTE_APP_DIR))
    sudo('tar xmzf {} -C {} --strip-components=2'.format(REMOTE_ARCHIVE, REMOTE_DEPLOY_DIR))
    sudo('rm {}'.format(REMOTE_ARCHIVE))


def _update_py_deps():
    if not exists(REMOTE_VENV, use_sudo=True):
        sudo('virtualenv {}'.format(REMOTE_VENV))
    sudo('{}/bin/pip install -r {}/requirements.txt'.format(REMOTE_VENV, REMOTE_DEPLOY_DIR))


def _install(pkg):
    puts('installing {}...'.format(pkg))
    with quiet():
        sudo('DEBIAN_FRONTEND=noninteractive apt-get install {} -y'.format(pkg))
    puts('{} installed'.format(pkg))


def _system_update_upgrade():
    puts('updating and upgrading system. this may take a while...')
    with quiet():
        sudo("sh -c 'echo deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main > /etc/apt/sources.list.d/pgdg.list'")
        sudo('wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -')
        sudo('apt-get update')
        sudo('apt-get upgrade -y')
    puts('system updated and upgraded')


def _configure_firewall():
    with quiet():
        sudo('ufw allow 80/tcp')
        sudo('ufw allow 22/tcp')
        sudo('ufw allow 443/tcp')
        sudo('ufw --force enable')
    puts('firewall configured')
