CONFIG = {
    'working_dir': '/var/www/html/{{ app_name }}',
    # Note - the same version of gunicorn should be installed in the virtualenv below
    'python': '/var/www/html/{{ app_name }}/venv/bin/python',
    'args': (
        '--workers=3',
        '{{ app_name }}.views:app',
    ),
}
