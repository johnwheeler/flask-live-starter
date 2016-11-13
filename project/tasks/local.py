from fabric.api import task, local
from fabric.contrib import console

from .constants import *


__all__ = ['initdb', 'restore_remote']


@task
def initdb():
    local('createuser {} -P'.format(PROJECT_NAME))
    local('createdb {} -O {}'.format(PROJECT_NAME, PROJECT_NAME))


@task
def restore_remote():
    warning = "WARNING: You are about to overwrite your LOCAL database. Continue?"
    if not console.confirm(warning, default=False):
        return

    _db_kill_sessions()

    # drop/create database
    local("dropdb {}".format(PROJECT_NAME))
    local("createdb {} -O {}".format(PROJECT_NAME, PROJECT_NAME))

    # restore latest remote dump
    last_backup = _sorted_ls(LOCAL_BACKUPS_DIR)[-1]
    local("pg_restore backups/{} -d {} --no-owner -x -n public --role={}"
          .format(last_backup, PROJECT_NAME, PROJECT_NAME))

    _db_size_report()


def _db_kill_sessions():
    kill_sessions_sql = """
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = '{}'
        AND pid <> pg_backend_pid();
        """.format(PROJECT_NAME)

    kill_sessions_cmd = 'psql {} -c "{}"' \
        .format(PROJECT_NAME, kill_sessions_sql)
    local(kill_sessions_cmd)


def _db_size_report():
    db_size_sql = "SELECT pg_size_pretty(pg_database_size('{}'))" \
        .format(PROJECT_NAME)
    db_size_cmd = 'psql {} -c "{}"'.format(PROJECT_NAME, db_size_sql)
    local(db_size_cmd)


def _sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))
