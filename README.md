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
* A memory cache (redis)
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
