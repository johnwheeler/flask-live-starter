![Do it live!](http://i.imgur.com/MgdS9jJ.jpg)

# Welcome to Flask-Live-Starter

Developing a Flask application locally is easy. However, getting it up and running on production infrastructure is harder. 

Flask-Live-Starter prescribes a set of best-of-breed infrastructure components that make deploying to VPS instances a snap. It includes Fabric tasks that automate provisioning, deployment, and common post-deployment operations (database backup and log tailing). Deploy early and easily with Flask-Live-Starter!

## Introduction

Flask-Live-Starter is a boilerplate Flask application with Fabric tasks that automate the installation and provisioning of:

* A Linux box (Debian)
* A WSGI server (Gunicorn)
* An HTTPD server (Nginx)
* An SSL certificate (LetsEncrypt)
* A database server (Postgresql)
* An in-memory cache (Redis)
* A firewall (UFW)

In addition to provisioning your application's environment, Flask-Live-Starter makes it a snap to:

* Deploy your Flask application
* Backup your production database
* Tail your production logs

Flask-Live-Starter is all about backend provisioning and deployment. It makes no assumptions about and gives no guidance on front-end frameworks. It only focuses on server-side code, so you're free to use JQuery, Angular, Bootstrap, or whatever you wish.

## Quickstart

Let's setup a new application named myapp.

#### Download flask-live-starter

```
git clone https://github.com/johnwheeler/flask-live-starter myapp
rm -rf myapp/.git
```

#### Prepare your local development environment

```
cd myapp
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Configure your application for development

```
cp fabfile/settings.py.example fabfile/settings.py
nano fabfile/settings.py

cp app/settings.cfg.example app/settings.cfg
nano app/settings.cfg

createuser <app_name> -P
createdb <app_name> -O <app_name>

# where <app_name> is the value of env._app_name in fabfile/settings.py

python app/views.py
```

#### Prepare the remote server

```
fab install.system install.postgres install.redis

fab provision.firewall provision.database

fab remote.deploy

fab provision.certificate
```

## Fabric Tasks

The fabric tasks are broken into four namespaces that each focus on a separate
deployment concern.

* `install` is for installing system components including the stack for serving Flask apps, Postgresql, and Redis
* `provision` is for provisioning a certificate, a firewall, and a database
* `remote` includes tasks to deploy your application, backup your database, and tail and grep logs
* `local` has one task that restores the latest backup to your local development database so you can work off your production dataset.

[See the tasks in each namespace for details](https://github.com/johnwheeler/flask-live-starter/tree/master/fabfile)
