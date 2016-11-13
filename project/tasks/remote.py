import os
from datetime import datetime

from fabric.api import task, local, sudo, put
from fabric.contrib import files

from .constants import *


__all__ = ['deploy', 'undeploy', 'backup', 'initdb']


@task
def deploy():
    if not files.exists(REMOTE_DEPLOY_DIR, use_sudo=True):
        sudo('mkdir {}'.format(REMOTE_DEPLOY_DIR))

    _dist()
    _upload_and_extract_archive()
    _update_py_deps()

    sudo('chown -R root:www-data {}'.format(REMOTE_DEPLOY_DIR))
    sudo('chmod -R og-rwx,g+rxs {}'.format(REMOTE_DEPLOY_DIR))

    if not files.exists(REMOTE_GUNICORN_CONF_FILE):
        put(LOCAL_GUNICORN_CONF_FILE, REMOTE_GUNICORN_CONF_FILE, use_sudo=True)

    if not files.exists(REMOTE_NGINX_CONF_FILE):
        put(LOCAL_NGINX_CONF_FILE, REMOTE_NGINX_CONF_FILE, use_sudo=True)
        sudo('service nginx restart')

    sudo("service gunicorn restart")
    local('rm -rf ./dist')


@task
def undeploy():
    sudo('rm -rf {}'.format(REMOTE_DEPLOY_DIR))
    sudo('rm {}'.format(REMOTE_NGINX_CONF_FILE))
    sudo('rm {}'.format(REMOTE_GUNICORN_CONF_FILE))
    sudo("service gunicorn restart")
    sudo('service nginx restart')


@task
def initdb():
    sudo('createuser {} -P'.format(PROJECT_NAME), user='postgres')
    sudo('createdb {} -O {}'.format(PROJECT_NAME, PROJECT_NAME), user='postgres')


@task
def backup():
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
    dump_file = '%s-remote-%s.dmp' % (PROJECT_NAME, timestamp)
    pg_dump_cmd = 'pg_dump {} -U {} -h localhost -x -Fc -f {}' \
        .format(PROJECT_NAME, PROJECT_NAME, dump_file)
    sudo(pg_dump_cmd)
    if not os.path.exists(LOCAL_BACKUPS_DIR):
        local('mkdir {}'.format(LOCAL_BACKUPS_DIR))
    files.get(dump_file, LOCAL_BACKUPS_DIR)
    sudo("rm %s" % dump_file)


def _dist():
    outdir = 'dist/{}'.format(PROJECT_NAME)
    local('mkdir -p {}'.format(outdir))
    local('cp requirements.txt {}'.format(outdir))
    local('cp -R {} {}'.format(PROJECT_NAME, outdir))
    local('find {} -name "*.pyc" -type f -delete'.format(outdir))
    local('tar czf dist/{}.tar.gz {}'.format(PROJECT_NAME, outdir))


def _upload_and_extract_archive():
    put(LOCAL_ARCHIVE, REMOTE_ARCHIVE, use_sudo=True)

    if not files.exists(REMOTE_DEPLOY_DIR, use_sudo=True):
        sudo('mkdir {}'.format(REMOTE_DEPLOY_DIR))

    sudo('rm -rf {}'.format(REMOTE_APP_DIR))
    sudo('tar xmzf {} -C {} --strip-components=2'.format(REMOTE_ARCHIVE, REMOTE_DEPLOY_DIR))
    sudo('rm {}'.format(REMOTE_ARCHIVE))


def _update_py_deps():
    if not files.exists(REMOTE_VENV, use_sudo=True):
        sudo('virtualenv {}'.format(REMOTE_VENV))

    sudo('{}/bin/pip install -r {}/requirements.txt'.format(REMOTE_VENV, REMOTE_DEPLOY_DIR))
