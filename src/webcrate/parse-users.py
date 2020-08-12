#!/usr/bin/env python3

import os
import yaml
from munch import munchify
from pprint import pprint

with open('/webcrate/users/users.yml') as f:
  users = munchify(yaml.safe_load(f))

SITES_PATH = '/sites'
MODE = os.environ.get('MODE', 'DEV')
DEV_MODE_USER_UID = os.environ.get('DEV_MODE_USER_UID', '1000')
DEV_MODE_USER_GID = os.environ.get('DEV_MODE_USER_GID', '1000')
DEV_MODE_USER_PASS = os.environ.get('DEV_MODE_USER_PASS', 'DEV')
CGI_PORT_START_NUMBER = 9000
UID_START_NUMBER = 100000

if MODE == 'PRODUCTION':
  os.system(f'userdel dev > /dev/null 2>&1')
  for username,user in users.items():
    user.name = username
    os.system(f'groupadd --gid {user.uid} {user.name}')
    os.system(f'useradd --no-create-home --uid {user.uid} --gid {user.uid} --home-dir {SITES_PATH}/{user.name} {user.name}')
    os.system(f'usermod -s /bin/fish {user.name} > /dev/null 2>&1')
    os.system(f'chown {user.name}:{user.name} {SITES_PATH}/{user.name}')
    os.system(f'usermod -p "{user.password}" {user.name} > /dev/null 2>&1')
    if user.backend == 'gunicorn':
      port = CGI_PORT_START_NUMBER + user.uid - UID_START_NUMBER
      os.system(f'source /sites/{user.name}/app/env/bin/activate; sudo -u {user.name} gunicorn --daemon --bind :{port} --name {user.name} --user {user.name} --group {user.name} --pid ../tmp/gunicorn.pid --error-logfile ../logs/gunicorn-error.log -c /sites/{user.name}/app/gunicorn.conf.py --chdir /sites/{user.name}/app core.wsgi:application; deactivate')
    print(f'{user.name} - created')

if MODE == 'DEV':
  stream = os.popen('openssl passwd -6 {DEV_MODE_USER_PASS}')
  dev_password = stream.read()
  os.system(f'usermod -p "{dev_password}" dev > /dev/null 2>&1')
  os.system(f'usermod -u {DEV_MODE_USER_UID} dev > /dev/null 2>&1')
  os.system(f'groupmod -g {DEV_MODE_USER_GID} dev > /dev/null 2>&1')
  os.system(f'usermod -s /bin/fish dev > /dev/null 2>&1')

  for username,user in users.items():
    user.name = username
    if user.backend == 'gunicorn':
      port = CGI_PORT_START_NUMBER + user.uid - UID_START_NUMBER
      os.system(f'source /sites/{user.name}/app/env/bin/activate; sudo -u dev gunicorn --daemon --bind :{port} --name {user.name} --user dev --group dev --pid ../tmp/gunicorn.pid --error-logfile ../logs/gunicorn-error.log -c /sites/{user.name}/app/gunicorn.conf.py --chdir /sites/{user.name}/app core.wsgi:application; deactivate')
    print(f'{user.name} - parsed')
