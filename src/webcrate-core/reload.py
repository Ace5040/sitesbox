#!/usr/bin/env python3

import os
import sys
import yaml
from munch import munchify

with open('/webcrate/users.yml', 'r') as f:
  users = munchify(yaml.safe_load(f))
  f.close()

SITES_PATH = '/sites'
WEBCRATE_MODE = os.environ.get('WEBCRATE_MODE', 'DEV')
WEBCRATE_UID = os.environ.get('WEBCRATE_UID', '1000')
WEBCRATE_GID = os.environ.get('WEBCRATE_GID', '1000')
UID_START_NUMBER = 100000
CGI_PORT_START_NUMBER = 9000

#stop services
os.system(f'systemctl stop dnsmasq')
os.system(f'systemctl stop proftpd')
os.system(f'systemctl stop sshd')
os.system(f'systemctl stop cronie')
os.system(f'systemctl stop telegraf')
os.system(f'kill -15 $(pgrep -f "php-fpm: master process")')
os.system(f'kill -15 $(pgrep -f "gunicorn")')
os.system(f'kill -15 $(pgrep --inverse --euid 0 '')')


#systemctl stop dnsmasq;systemctl stop proftpd;systemctl stop sshd;systemctl stop cronie;systemctl stop telegraf;kill -15 $(pgrep -f "php-fpm: master process");kill -15 $(pgrep -f "gunicorn")

print(f'services stopped')
sys.stdout.flush()

#delete users
with open("/etc/passwd") as file:
  for line in file:
    arr=line.split(":")
    user_name = arr[0]
    user_id = int(arr[2])
    if ( ( WEBCRATE_MODE == 'DEV' and user_id == int(WEBCRATE_UID) ) or ( WEBCRATE_MODE == 'PRODUCTION' and user_id >= 100000 ) ) and user_id != 0 and user_name != 'dev':
      os.system(f'userdel -f {user_name} >/dev/null 2>/dev/null')
      os.system(f'groupdel -f {user_name} >/dev/null 2>/dev/null')
print(f'users deleted')
sys.stdout.flush()

#parse users
os.system(f'/webcrate/parse-users.py')
print(f'users parsed')
sys.stdout.flush()

#start services
os.system(f'systemctl start php56-fpm')
os.system(f'systemctl start php73-fpm')
os.system(f'systemctl start php-fpm7')
os.system(f'systemctl start php-fpm')

os.system(f'systemctl start dnsmasq')
os.system(f'systemctl start proftpd')
os.system(f'systemctl start sshd')
os.system(f'systemctl start cronie')
os.system(f'systemctl start telegraf')
print(f'services started')
sys.stdout.flush()
