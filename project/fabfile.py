import os
from datetime import datetime

from fabric.api import env, local, sudo, put
from fabric.utils import puts
from fabric.contrib.files import exists, get
from fabric.context_managers import quiet

env.user = 'vagrant'
env.host_string = '192.168.33.10'
env.key_filename = '.vagrant/machines/default/virtualbox/private_key'


PROJECT_NAME = os.path.basename(os.path.dirname(os.path.realpath(__file__)))

REMOTE_DEPLOY_DIR = '/var/www/html/{}'.format(PROJECT_NAME)
REMOTE_VENV = '{}/venv'.format(REMOTE_DEPLOY_DIR)
REMOTE_APP_DIR = '{}/{}'.format(REMOTE_DEPLOY_DIR, PROJECT_NAME)

LOCAL_ARCHIVE = './dist/{}.tar.gz'.format(PROJECT_NAME)
REMOTE_ARCHIVE = '{}.tar.gz'.format(PROJECT_NAME)

LOCAL_GUNICORN_CONF_FILE = './etc/{}.gunicorn.conf'.format(PROJECT_NAME)
REMOTE_GUNICORN_CONF_FILE = '/etc/gunicorn.d/{}.conf'.format(PROJECT_NAME)

LOCAL_NGINX_CONF_FILE = './etc/{}.nginx.conf'.format(PROJECT_NAME)
REMOTE_NGINX_CONF_FILE = '/etc/nginx/conf.d/{}.conf'.format(PROJECT_NAME)


def deploy():
    if not exists(REMOTE_DEPLOY_DIR, use_sudo=True):
        sudo('mkdir {}'.format(REMOTE_DEPLOY_DIR))

    _dist()
    _upload_and_extract_archive()
    _update_py_deps()
    sudo('chown -R root:www-data {}'.format(REMOTE_DEPLOY_DIR))
    sudo('chmod -R og-rwx,g+rxs {}'.format(REMOTE_DEPLOY_DIR))

    if not exists(REMOTE_GUNICORN_CONF_FILE):
        put(LOCAL_GUNICORN_CONF_FILE, REMOTE_GUNICORN_CONF_FILE, use_sudo=True)

    if not exists(REMOTE_NGINX_CONF_FILE):
        put(LOCAL_NGINX_CONF_FILE, REMOTE_NGINX_CONF_FILE, use_sudo=True)
        sudo('service nginx restart')

    sudo("service gunicorn restart")
    local('rm -rf ./dist')


def backup_remote_db():
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
    dump_file = '%s-remote-%s.dmp' % (PROJECT_NAME, timestamp)
    pg_dump_cmd = 'pg_dump {} -U {} -h localhost -x -Fc -f {}' \
        .format(PROJECT_NAME, PROJECT_NAME, dump_file)
    sudo(pg_dump_cmd)
    if not os.path.exists('backups'):
        local('mkdir backups')
    get(dump_file, 'backups')
    sudo("rm %s" % dump_file)


def uninstall_remote():
    sudo('rm -rf {}'.format(REMOTE_DEPLOY_DIR))
    sudo('rm {}'.format(REMOTE_NGINX_CONF_FILE))
    sudo('rm {}'.format(REMOTE_GUNICORN_CONF_FILE))
    sudo("service gunicorn restart")
    sudo('service nginx restart')


def provision_system():
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


def provision_database():
    sudo('createuser {} -P'.format(PROJECT_NAME), user='postgres')
    sudo('createdb {} -O {}'.format(PROJECT_NAME, PROJECT_NAME), user='postgres')


def _dist():
    outdir = 'dist/{}'.format(PROJECT_NAME)
    local('mkdir -p {}'.format(outdir))
    local('cp requirements.txt {}'.format(outdir))
    local('cp -R {} {}'.format(PROJECT_NAME, outdir))
    local('find {} -name "*.pyc" -type f -delete'.format(outdir))
    local('tar czf dist/{}.tar.gz {}'.format(PROJECT_NAME, outdir))


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
