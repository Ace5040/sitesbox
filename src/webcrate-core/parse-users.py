#!/usr/bin/env python3

import os
import yaml
from munch import munchify
from pprint import pprint

with open('/webcrate/users.yml', 'r') as f:
  users = munchify(yaml.safe_load(f))
  f.close()

SITES_PATH = '/sites'
WEBCRATE_MODE = os.environ.get('WEBCRATE_MODE', 'DEV')
WEBCRATE_UID = os.environ.get('WEBCRATE_UID', '1000')
WEBCRATE_GID = os.environ.get('WEBCRATE_GID', '1000')
DEV_MODE_USER_PASS = os.environ.get('DEV_MODE_USER_PASS', 'DEV')
UID_START_NUMBER = int(os.environ.get('UID_START_NUMBER', '100000'))
CGI_PORT_START_NUMBER = int(os.environ.get('CGI_PORT_START_NUMBER', '9000'))

if WEBCRATE_MODE == 'PRODUCTION':
  os.system(f'userdel dev > /dev/null 2>&1')
  for username,user in users.items():
    user.name = username
    os.system(f'groupadd --gid {user.uid} {user.name}')
    os.system(f'useradd --no-create-home --uid {user.uid} --gid {user.uid} --home-dir {SITES_PATH}/{user.name} {user.name}')
    os.system(f'usermod -s /bin/fish {user.name} > /dev/null 2>&1')
    os.system(f'chown {user.name}:{user.name} {SITES_PATH}/{user.name}')
    password = str(user.password).replace("$", "\$")
    os.system(f'usermod -p {password} {user.name} > /dev/null 2>&1')
    if user.backend == 'gunicorn':
      data_folder=user.root_folder.split("/")[0]
      port = CGI_PORT_START_NUMBER + user.uid - UID_START_NUMBER
      gunicorn_conf=''
      if os.path.isfile(f'/sites/{user.name}/{data_folder}/gunicorn.conf.py'):
        gunicorn_conf=f'-c /sites/{user.name}/{data_folder}/gunicorn.conf.py'
      os.system(f'source /sites/{user.name}/{data_folder}/env/bin/activate; sudo -u {user.name} gunicorn --daemon --bind :{port} --name {user.name} --user {user.name} --group {user.name} --pid ../tmp/gunicorn.pid --error-logfile ../log/gunicorn-error.log {gunicorn_conf} --chdir /sites/{user.name}/{data_folder} {user.gunicorn_app_module}; deactivate')
    print(f'{user.name} - created')

if WEBCRATE_MODE == 'DEV':
  stream = os.popen('openssl passwd -6 {DEV_MODE_USER_PASS}')
  dev_password = stream.read().strip()
  os.system(f'usermod -p "{dev_password}" dev > /dev/null 2>&1')
  os.system(f'usermod -u {WEBCRATE_UID} dev > /dev/null 2>&1')
  os.system(f'groupmod -g {WEBCRATE_GID} dev > /dev/null 2>&1')
  os.system(f'usermod -s /bin/fish dev > /dev/null 2>&1')

  for username,user in users.items():
    user.name = username
    if user.backend == 'gunicorn':
      data_folder=user.root_folder.split("/")[0]
      port = CGI_PORT_START_NUMBER + user.uid - UID_START_NUMBER
      gunicorn_conf=''
      if os.path.isfile(f'/sites/{user.name}/{data_folder}/gunicorn.conf.py'):
        gunicorn_conf=f'-c /sites/{user.name}/{data_folder}/gunicorn.conf.py'
      dev_user = 'dev'
      if WEBCRATE_UID == 0 or WEBCRATE_GID == 0:
        dev_user = 'root'
      os.system(f'source /sites/{user.name}/{data_folder}/env/bin/activate; sudo -u {dev_user} gunicorn --daemon --bind :{port} --name {user.name} --user {dev_user} --group {dev_user} --pid ../tmp/gunicorn.pid --error-logfile ../log/gunicorn-error.log {gunicorn_conf} --chdir /sites/{user.name}/{data_folder} {user.gunicorn_app_module}; deactivate')
    print(f'{user.name} - parsed')