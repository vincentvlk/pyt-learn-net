#!/usr/bin/env python3

'''
Jednoduchy Py3 skript "netmiko-test.py" na ucenie kniznice Paramiko.
'''

import paramiko
import time
import datetime
import threading

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

flotila_list = [n91leaf1, n92leaf2, cat1sw]


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
    print(f'Connected to \"{hostname}\"')

    device_access.send(b'terminal length 0\n')
    device_access.send(b'show running-config\n')
    time.sleep(3)

    output = device_access.recv(65535).decode()
    print(output)

    teraz = str(datetime.datetime.now().strftime('%d.%m.%Y-%H:%M:%S'))

    print(f'Config zariadenia \"{hostname}\" ukladam do suboru.')
    with open('backup-' + hostname + '-' + teraz + '.txt', 'w') as p_data:
        p_data.write(output)

    ssh_client.close()


# config_backup(**n91leaf1)

bkp_threads_list = []

for device in flotila_list:
    bkp_thread = threading.Thread(target=config_backup, kwargs=device)
    bkp_threads_list.append(bkp_thread)
    bkp_thread.start()

for thread in bkp_threads_list:
    thread.join()
