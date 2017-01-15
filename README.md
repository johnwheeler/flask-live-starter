![Do it live!](http://i.imgur.com/MgdS9jJ.jpg)

[![bird] Follow @_johnwheeler for updates](https://twitter.com/_johnwheeler)
[bird]: http://i.imgur.com/UUARvmc.png

# Welcome to Flask-Live-Starter

***Note:*** *This is an alpha release that supports Unix-based development environments only.*

Go from 0 to 100 MPH with the infrastructure behind [OldGeekJobs.com](https://oldgeekjobs.com).

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

<!--

#### `install`

Placeholder

#### `provision`

Placeholder

#### `remote`

Placeholder

#### `local`

Placeholder

## Technology selection

Placeholder

#### Debian

Placeholder

#### Flask

Placeholder

#### Gunicorn

Placeholder

#### Nginx

Placeholder

#### Postgresql

Placeholder

#### Redis

Placeholder
-->
