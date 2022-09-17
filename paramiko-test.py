#!/usr/bin/env python3

'''
Jednoduchy Py3 skript "netmiko-test.py" na ucenie kniznice Paramiko.
'''

import paramiko
import time
import schedule
import datetime

# hostname = '192.168.5.201'
# username = 'admin'
# password = 'Cisco.123'

n91leaf1 = {'hostname': '192.168.5.201',
            'username': 'admin',
            'password': 'Cisco.123'}

n92leaf2 = {'hostname': '192.168.5.202',
            'username': 'admin',
            'password': 'Cisco.123'}

cat1sw = {'hostname': '192.168.5.211',
          'username': 'admin',
          'password': 'Cisco.123'}


def config_backup(hostname, username, password):
    ssh_client = paramiko.client.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh_client.connect(hostname=hostname,
                       port=22,
                       username=username,
                       password=password,
                       look_for_keys=False,
                       allow_agent=False)

    device_access = ssh_client.invoke_shell()
    print("Connected")

    device_access.send(b'terminal length 0\n')
    device_access.send(b'show running-config\n')
    time.sleep(3)

    output = device_access.recv(65535).decode()
    print(output)

    teraz = str(datetime.datetime.now().strftime('%d.%m.%Y-%H:%M:%S'))

    with open('paramiko_backup-' + teraz + '.txt', 'w') as p_data:
        p_data.write(output)

    ssh_client.close()


# config_backup(**n91leaf1)

schedule.every(15).seconds.do(config_backup, **n91leaf1)

while True:
    schedule.run_pending()
    time.sleep(1)
