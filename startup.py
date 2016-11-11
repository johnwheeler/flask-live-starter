import os
import shutil

import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument('project_name')
def new(project_name):
    cwd = os.path.dirname(os.path.realpath(__file__))

    # copy the project template dir
    project_template_dir = os.path.join(cwd, 'template_files/project')
    shutil.copytree(project_template_dir, project_name)

    # rename the app to project_name
    old_app = os.path.join(project_name, 'app')
    new_app = os.path.join(project_name, project_name)
    os.rename(old_app, new_app)

    # show command feedback
    for root, dirs, files in os.walk(project_name):
        for f in files:
            print root + os.sep + f
    click.echo('created {}'.format(project_name))


if __name__ == '__main__':
    cli()
