import os
import shutil

import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument('project_name')
def start(project_name):
    # create the source directory paths
    src_dir = os.path.dirname(os.path.realpath(__file__))
    src_app_dir = os.path.join(src_dir, 'app')
    src_etc_dir = os.path.join(src_dir, 'etc')

    # create the destination directory paths
    dest_dir = project_name
    dest_app_dir = os.path.join(dest_dir, project_name)
    dest_etc_dir = os.path.join(dest_dir, 'etc')

    # make the destination directory
    os.mkdir(dest_dir)

    # copy the app directory into project_name
    shutil.copytree(src_app_dir, dest_app_dir)
    shutil.copytree(src_etc_dir, dest_etc_dir)


if __name__ == '__main__':
    cli()
