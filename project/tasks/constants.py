import os

PROJECT_NAME = os.path.basename(os.getcwd())

REMOTE_DEPLOY_DIR='/var/www/html/{}'.format(PROJECT_NAME)
REMOTE_VENV='{}/venv'.format(REMOTE_DEPLOY_DIR)
REMOTE_APP_DIR='{}/{}'.format(REMOTE_DEPLOY_DIR, PROJECT_NAME)

LOCAL_ARCHIVE='./dist/{}.tar.gz'.format(PROJECT_NAME)
REMOTE_ARCHIVE='{}.tar.gz'.format(PROJECT_NAME)

LOCAL_GUNICORN_CONF_FILE='./etc/{}.gunicorn.conf'.format(PROJECT_NAME)
REMOTE_GUNICORN_CONF_FILE='/etc/gunicorn.d/{}.conf'.format(PROJECT_NAME)

LOCAL_NGINX_CONF_FILE='./etc/{}.nginx.conf'.format(PROJECT_NAME)
REMOTE_NGINX_CONF_FILE='/etc/nginx/conf.d/{}.conf'.format(PROJECT_NAME)
