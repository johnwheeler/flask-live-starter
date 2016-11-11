import os
import shutil
from binascii import b2a_hex
from textwrap import dedent

import click
from jinja2 import Environment, FileSystemLoader


CWD = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(CWD, 'templates')
jinja_env = Environment(loader=FileSystemLoader(template_dir))


@click.group()
def cli():
    pass


@cli.command()
@click.argument('project_name')
def new(project_name):
    # copy the project template dir
    project_template_dir = os.path.join(CWD, 'project')
    shutil.copytree(project_template_dir, project_name)

    # rename the app to project_name
    old_app_dir = os.path.join(project_name, 'app')
    app_dir = os.path.join(project_name, project_name)
    os.rename(old_app_dir, app_dir)

    # write project settings
    _write_project_settings(app_dir, project_name)

    # make etc directory
    etc_dir = os.path.join(project_name, 'etc')
    os.mkdir(etc_dir)

    # write ngnix config
    _write_nginx_conf(project_name)

    # write gunicorn config
    _write_gunicorn_conf(project_name)

    # show command feedback
    for root, dirs, files in os.walk(project_name):
        for f in files:
            print root + os.sep + f
    click.echo('created {}'.format(project_name))


def _write_project_settings(app_dir, project_name):
    # generate the template
    secure_random = b2a_hex(os.urandom(24))
    template = jinja_env.get_template('settings.cfg.tpl')
    file_contents = template.render(secure_random=secure_random,
                                    project_name=project_name)

    # write the file
    settings_file = os.path.join(app_dir, 'settings.cfg')
    with open(settings_file, 'w') as f:
        f.write(file_contents)


def _write_nginx_conf(project_name):
    # generate the template
    template = jinja_env.get_template('etc/nginx.conf.tpl')
    file_contents = template.render(project_name=project_name)

    # write the file
    filename = '{}.nginx.conf'.format(project_name)
    nginx_conf = os.path.join(project_name, 'etc', filename)
    with open(nginx_conf, 'w') as f:
        f.write(file_contents)


def _write_gunicorn_conf(project_name):
    # generate the template
    template = jinja_env.get_template('etc/gunicorn.conf.tpl')
    file_contents = template.render(project_name=project_name)

    # write the file
    filename = '{}.gunicorn.conf'.format(project_name)
    gunicorn_conf = os.path.join(project_name, 'etc', filename)
    with open(gunicorn_conf, 'w') as f:
        f.write(file_contents)
