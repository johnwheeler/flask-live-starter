from fabric.api import task, local
from fabric.contrib import console

from .constants import *


__all__ = ['restore_remote']


@task
def restore_remote():
    warning = "WARNING: You are about to overwrite your LOCAL database. Continue?"
    if not console.confirm(warning, default=False):
        return

    _db_kill_sessions()

    # drop/create database
    local("dropdb {}".format(APP_NAME))
    local("createdb {} -O {}".format(APP_NAME, APP_NAME))

    # restore latest remote dump
    last_backup = _sorted_ls(LOCAL_BACKUPS_DIR)[-1]
    local("pg_restore backups/{} -d {} --no-owner -x -n public --role={}"
          .format(last_backup, APP_NAME, APP_NAME))

    _db_size_report()


def _db_kill_sessions():
    kill_sessions_sql = """
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = '{}'
        AND pid <> pg_backend_pid();
        """.format(APP_NAME)
    kill_sessions_cmd = 'psql {} -c "{}"' \
        .format(APP_NAME, kill_sessions_sql)
    local(kill_sessions_cmd)


def _db_size_report():
    db_size_sql = "SELECT pg_size_pretty(pg_database_size('{}'))" \
        .format(APP_NAME)
    db_size_cmd = 'psql {} -c "{}"'.format(APP_NAME, db_size_sql)
    local(db_size_cmd)


def _sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))
