from fabric.api import *
from fabric.utils import abort, puts
from fabric.contrib.files import exists
from fabric.contrib.console import confirm
from fabric.context_managers import quiet

env.user = 'vagrant'
env.host_string = '192.168.33.10'
env.key_filename = '.vagrant/machines/default/virtualbox/private_key'


APP_NAME = 'app'
DEPLOY_DIR = '/var/www/html/{}'.format(APP_NAME)
VIRTUALENV = '{}/venv'.format(DEPLOY_DIR)
LOCAL_ARCHIVE = './dist/{}.tar.gz'.format(APP_NAME)
REMOTE_ARCHIVE = '/root/{}.tar.gz'.format(APP_NAME)


def configure():
    msg = 'This will overwrite your nginx and gunicorn configuration. Proceed?'
    if confirm(msg, default=False):
        put('etc/app.gunicorn.conf', '/etc/gunicorn.d/', use_sudo=True)
        sudo("service gunicorn restart")

        put('etc/app.nginx.conf', '/etc/nginx/conf.d/', use_sudo=True)
        sudo('service nginx restart')


def dist():
    outdir = 'dist/{}'.format(APP_NAME)
    local('mkdir -p {}'.format(outdir))
    local('cp requirements.txt {}'.format(outdir))
    local('cp -R {} {}'.format(APP_NAME, outdir))
    local('find {} -name "*.pyc" -type f -delete'.format(outdir))
    local('tar czf dist/{}.tar.gz {}'.format(APP_NAME, outdir))


def deploy():
    dist()
    _upload_and_extract_archive()
    _update_py_deps()
    sudo('chown -R root:www-data {}'.format(DEPLOY_DIR))
    sudo('chmod -R og-rwx,g+rxs {}'.format(DEPLOY_DIR))
    sudo("service gunicorn restart")
    clean()


def clean():
    local('rm -rf ./dist')


def clean_remote():
    sudo('rm -rf {}'.format(DEPLOY_DIR))


def provision():
    puts('updating and upgrading system. this may take a while...')
    with quiet():
        sudo("sh -c 'echo deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main > /etc/apt/sources.list.d/pgdg.list'")
        sudo('wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -')
        sudo('apt-get update')
        sudo('apt-get upgrade -y')
    puts('system updated and upgraded')
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

    if not exists(DEPLOY_DIR, use_sudo=True):
        sudo('mkdir {}'.format(DEPLOY_DIR))

    appdir = '{}/{}'.format(DEPLOY_DIR, APP_NAME)
    sudo('rm -rf {}'.format(appdir))
    sudo('tar xmzf {} -C {} --strip-components=2'.format(REMOTE_ARCHIVE, DEPLOY_DIR))
    sudo('rm {}'.format(REMOTE_ARCHIVE))


def _update_py_deps():
    if not exists(VIRTUALENV, use_sudo=True):
        sudo('virtualenv {}'.format(VIRTUALENV))
    sudo('{}/bin/pip install -r {}/requirements.txt'.format(VIRTUALENV, DEPLOY_DIR))


def _install(pkg):
    puts('installing {}...'.format(pkg))
    with quiet():
        sudo('DEBIAN_FRONTEND=noninteractive apt-get install {} -y'.format(pkg))
    puts('{} installed'.format(pkg))


def _configure_firewall():
    with quiet():
        sudo('ufw allow 80/tcp')
        sudo('ufw allow 22/tcp')
        sudo('ufw allow 443/tcp')
        sudo('ufw --force enable')
    puts('firewall configured')
