import os

PROJECT_NAME = 'app'

REMOTE_DEPLOY_DIR = '/var/www/html/{}'.format(PROJECT_NAME)
REMOTE_VENV = '{}/venv'.format(REMOTE_DEPLOY_DIR)
REMOTE_APP_DIR = '{}/{}'.format(REMOTE_DEPLOY_DIR, PROJECT_NAME)

LOCAL_ARCHIVE = 'dist/{}.tar.gz'.format(PROJECT_NAME)
REMOTE_ARCHIVE = '{}.tar.gz'.format(PROJECT_NAME)

LOCAL_GUNICORN_CONF_FILE = 'gunicorn.conf.tpl'.format(PROJECT_NAME)
REMOTE_GUNICORN_CONF_FILE = '/etc/gunicorn.d/{}.conf'.format(PROJECT_NAME)

LOCAL_NGINX_CONF_FILE = 'nginx.conf.tpl'.format(PROJECT_NAME)
REMOTE_NGINX_CONF_FILE = '/etc/nginx/conf.d/{}.conf'.format(PROJECT_NAME)

LOCAL_ETC_DIR = 'etc'
LOCAL_BACKUPS_DIR = 'backups'
