CONFIG = {
    'working_dir': '/var/www/html/{{ project_name }}',
    # Note - the same version of gunicorn should be installed in the virtualenv below
    'python': '/var/www/html/{{ project_name }}/venv/bin/python',
    'args': (
        '--workers=3',
        '{{ project_name }}.views:app',
    ),
}
