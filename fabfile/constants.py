import os

from fabric.api import env

APP_NAME = env._app_name
DOMAIN = env._domain
SUBDOMAIN = env._subdomain
EMAIL = env._email

LOCAL_ARCHIVE = 'dist/{}.tar.gz'.format(APP_NAME)
REMOTE_ARCHIVE = '{}.tar.gz'.format(APP_NAME)

LOCAL_GUNICORN_CONF_FILE = 'gunicorn.tpl'.format(APP_NAME)
REMOTE_GUNICORN_CONF_FILE = '/etc/gunicorn.d/{}'.format(APP_NAME)

LOCAL_NGINX_CONF_FILE = 'nginx.conf.tpl'.format(APP_NAME)
REMOTE_NGINX_CONF_FILE = '/etc/nginx/conf.d/{}.conf'.format(APP_NAME)

REMOTE_DEPLOY_DIR = '/var/www/html/{}'.format(APP_NAME)
REMOTE_VENV = '{}/venv'.format(REMOTE_DEPLOY_DIR, APP_NAME)
REMOTE_APP_DIR = '{}/{}'.format(REMOTE_DEPLOY_DIR, APP_NAME)
REMOTE_LOG_DIR = '/var/log/flask'
REMOTE_LOG_FILE = '{}/{}.log'.format(REMOTE_LOG_DIR, APP_NAME)

LOCAL_ETC_DIR = 'etc'
LOCAL_BACKUPS_DIR = 'backups'
