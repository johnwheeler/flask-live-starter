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

    _write_project_settings(app_dir, project_name)

    # show command feedback
    for root, dirs, files in os.walk(project_name):
        for f in files:
            print root + os.sep + f
    click.echo('created {}'.format(project_name))


def _write_project_settings(app_dir, project_name):
    settings_file = os.path.join(app_dir, 'settings.cfg')

    secure_random = b2a_hex(os.urandom(24))
    template = jinja_env.get_template('settings.cfg.tpl')
    file_contents = template.render(secure_random=secure_random,
                                    project_name=project_name)

    with open(settings_file, 'w') as f:
        f.write(file_contents)
