import os
from datetime import datetime

from fabric.api import task, local, sudo, put
from fabric.contrib import files
from jinja2 import Environment, FileSystemLoader

from .constants import *


__all__ = ['deploy', 'undeploy', 'backup', 'tail', 'reset_log']


@task
def tail(grep=""):
    sudo("tail -F -n +1 {} | grep --line-buffered -i '{}'"
         .format(REMOTE_LOG_FILE, grep))


@task
def reset_log():
    sudo("rm -f {}".format(REMOTE_LOG_FILE))
    sudo("service gunicorn reload")


@task
def deploy():
    _upload_archive()
    _extract_archive()
    _update_py_deps()
    _ensure_log_dir()
    _configure_gunicorn()
    _configure_nginx()


@task
def undeploy():
    sudo('rm -rf {}'.format(REMOTE_DEPLOY_DIR))

    if files.exists(REMOTE_GUNICORN_CONF_FILE):
        sudo('rm {}'.format(REMOTE_GUNICORN_CONF_FILE))
        sudo("service gunicorn restart")

    if files.exists(REMOTE_NGINX_CONF_FILE):
        sudo('rm {}'.format(REMOTE_NGINX_CONF_FILE))
        sudo('service nginx restart')


@task
def backup():
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
    dump_file = '%s-remote-%s.dmp' % (APP_NAME, timestamp)
    pg_dump_cmd = 'pg_dump {} -U {} -h localhost -x -Fc -f {}' \
        .format(APP_NAME, APP_NAME, dump_file)
    sudo(pg_dump_cmd)
    if not os.path.exists(LOCAL_BACKUPS_DIR):
        local('mkdir {}'.format(LOCAL_BACKUPS_DIR))
    files.get(dump_file, LOCAL_BACKUPS_DIR)
    sudo("rm %s" % dump_file)


def _upload_archive():
    outdir = 'dist/{}'.format(APP_NAME)
    local('mkdir -p {}'.format(outdir))
    local('cp requirements.txt {}'.format(outdir))
    local('cp -R {} {}'.format(APP_NAME, outdir))
    local('find {} -name "*.pyc" -type f -delete'.format(outdir))
    local('tar czf {} {}'.format(LOCAL_ARCHIVE, outdir))
    put(LOCAL_ARCHIVE, REMOTE_ARCHIVE, use_sudo=True)
    local('rm -rf dist')


def _extract_archive():
    if not files.exists(REMOTE_DEPLOY_DIR, use_sudo=True):
        sudo('mkdir {}'.format(REMOTE_DEPLOY_DIR))
        sudo('chown -R www-data:www-data {}'.format(REMOTE_DEPLOY_DIR))
        sudo('chmod -R og-rwx,g+rxs {}'.format(REMOTE_DEPLOY_DIR))

    sudo('rm -rf {}'.format(REMOTE_APP_DIR))
    sudo('tar xmzf {} -C {} --strip-components=2'.format(REMOTE_ARCHIVE, REMOTE_DEPLOY_DIR))
    sudo('rm {}'.format(REMOTE_ARCHIVE))


def _update_py_deps():
    if not files.exists(REMOTE_VENV, use_sudo=True):
        sudo('virtualenv {}'.format(REMOTE_VENV))

    sudo('{}/bin/pip install -r {}/requirements.txt'.format(REMOTE_VENV, REMOTE_DEPLOY_DIR))


def _ensure_log_dir():
    if not files.exists(REMOTE_LOG_DIR):
        sudo('mkdir {}'.format(REMOTE_LOG_DIR))
        sudo('chown -R www-data:www-data {}'.format(REMOTE_LOG_DIR))
        sudo('chmod -R og-rwx,g+rxs {}'.format(REMOTE_LOG_DIR))


def _configure_gunicorn():
    if not files.exists(REMOTE_GUNICORN_CONF_FILE):
        files.upload_template(LOCAL_GUNICORN_CONF_FILE,
                              REMOTE_GUNICORN_CONF_FILE,
                              context={'app_name': APP_NAME},
                              template_dir=LOCAL_ETC_DIR,
                              use_jinja=True,
                              use_sudo=True)
    sudo("service gunicorn restart")


def _configure_nginx():
    if not files.exists(REMOTE_NGINX_CONF_FILE):
        files.upload_template(LOCAL_NGINX_CONF_FILE,
                              REMOTE_NGINX_CONF_FILE,
                              context={
                                  'app_name': APP_NAME,
                                  'domain': DOMAIN,
                                  'subdomain': SUBDOMAIN
                              },
                              template_dir=LOCAL_ETC_DIR,
                              use_jinja=True,
                              use_sudo=True)
    sudo('service nginx reload')
