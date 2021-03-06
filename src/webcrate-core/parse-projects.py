#!/usr/bin/env python3

import os
import yaml
from munch import munchify

with open('/webcrate/projects.yml', 'r') as f:
  projects = munchify(yaml.safe_load(f))
  f.close()

WEBCRATE_MODE = os.environ.get('WEBCRATE_MODE', 'DEV')
WEBCRATE_UID = os.environ.get('WEBCRATE_UID', '1000')
WEBCRATE_GID = os.environ.get('WEBCRATE_GID', '1000')
UID_START_NUMBER = 100000
CGI_PORT_START_NUMBER = 9000

if WEBCRATE_MODE == 'PRODUCTION':
  os.system(f'userdel dev > /dev/null 2>&1')

if WEBCRATE_MODE == 'DEV':
  os.system(f'usermod -u {WEBCRATE_UID} dev > /dev/null 2>&1')
  os.system(f'groupmod -g {WEBCRATE_GID} dev > /dev/null 2>&1')
  os.system(f'usermod -s /bin/fish dev > /dev/null 2>&1')

for projectname,project in projects.items():
  project.name = projectname

  if hasattr(project, 'volume'):
    project.folder = f'/projects{(project.volume + 1) if project.volume else ""}/{project.name}'
  else:
    project.folder = f'/projects/{project.name}'

  UID = project.uid
  GID = project.uid

  if WEBCRATE_MODE == 'DEV':
    UID = WEBCRATE_UID
    GID = WEBCRATE_GID

  os.system(f'groupadd --non-unique --gid {GID} {project.name}')
  os.system(f'useradd --non-unique --no-create-home --uid {UID} --gid {GID} --home-dir {project.folder} {project.name}')
  os.system(f'usermod -s /bin/fish {project.name} > /dev/null 2>&1')
  os.system(f'chown {project.name}:{project.name} {project.folder}')
  password = str(project.password).replace("$", "\$")
  os.system(f'usermod -p {password} {project.name} > /dev/null 2>&1')

  os.system(f'touch /etc/ftp.passwd')
  if hasattr(project, 'ftps') and project.ftps:
    with open(f'/etc/ftp.passwd', 'a') as f:
      for ftp in project.ftps:
        ftp_folder = f'{project.folder}{("/" + ftp.home) if ftp.home else ""}'
        f.write(f'{ftp.name}:{ftp.password}:{UID}:{GID}::{ftp_folder}:/bin/false\n')
        os.system(f'mkdir -p {ftp_folder}')
        os.system(f'chown -R {project.name}:{project.name} {ftp_folder}')
      f.close()

    print(f'additional ftp accounts for {project.name} - generated')
  os.system(f'chmod a-rwx,u+rw /etc/ftp.passwd')

  if project.backend == 'gunicorn':
    data_folder=project.root_folder.split("/")[0]
    port = CGI_PORT_START_NUMBER + project.uid - UID_START_NUMBER
    gunicorn_conf=''
    if os.path.isfile(f'{project.folder}/{data_folder}/gunicorn.conf.py'):
      gunicorn_conf=f'-c {project.folder}/{data_folder}/gunicorn.conf.py'
    os.system(f'source {project.folder}/{data_folder}/env/bin/activate; sudo -u {project.name} gunicorn --daemon --bind :{port} --name {project.name} --user {project.name} --group {project.name} --pid ../tmp/gunicorn.pid --error-logfile ../log/gunicorn-error.log {gunicorn_conf} --chdir {project.folder}/{data_folder} {project.gunicorn_app_module}; deactivate')

  print(f'{project.name} - created')
