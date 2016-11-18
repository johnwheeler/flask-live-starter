from fabric.api import env

from . import provision, remote, local

env.user = 'vagrant'
env.host_string = '192.168.33.10'
env.key_filename = '.vagrant/machines/default/virtualbox/private_key'
