![Do it live!](http://i.imgur.com/MgdS9jJ.jpg)

[![bird] Follow @_johnwheeler for updates](https://twitter.com/_johnwheeler)
[bird]: http://i.imgur.com/UUARvmc.png

# Welcome to Flask-Live-Starter

***Note:*** *This is an alpha release that supports Unix-based development environments only.*

Go from 0 to 100 MPH with the infrastructure behind [OldGeekJobs.com](https://oldgeekjobs.com).

Flask-Live-Starter is a boilerplate Flask application with Fabric tasks that automate the provisioning of:

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

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Quickstart](#quickstart)
    - [Download flask-live-starter](#download-flask-live-starter)
    - [Prepare your local development environment](#prepare-your-local-development-environment)
    - [Configure your application for development](#configure-your-application-for-development)
    - [Prepare the remote server](#prepare-the-remote-server)
- [Fabric Tasks](#fabric-tasks)
    - [`install`](#install)
    - [`provision`](#provision)
    - [`remote`](#remote)
    - [`local`](#local)
- [Technology selection](#technology-selection)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

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

fab local.initdb

export FLASK_APP=app/views.py
export FLASK_DEBUG=1
flask run
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
