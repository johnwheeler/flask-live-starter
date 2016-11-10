import os
import shutil

import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument('project_name')
def start(project_name):
    cwd = os.path.dirname(os.path.realpath(__file__))
    src_dir = os.path.join(cwd, 'src')
    shutil.copytree(src_dir, project_name)
    old_py = os.path.join(project_name, 'app')
    new_py = os.path.join(project_name, project_name)
    os.rename(old_py, new_py)


if __name__ == '__main__':
    cli()
