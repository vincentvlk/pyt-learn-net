#!/usr/bin/env python3

'''
Jednoduchy Py3 skript "netmiko-test.py" na ucenie kniznice Paramiko.
'''

import paramiko
import time
# import datetime
import threading
import re

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

# regx = '(\S+)\s+(([\d\.]+)|unassigned)\s+\S+\s+\S+\s+(up|administratively down)\s+(\S+)'

int_pattern = re.compile(r"(\S+)\s+(([\d\.]+)|unassigned)\s+\S+\s+\S+\s+(up|administratively down)\s+(\S+)")


def cisco_int_parser(hostname, username, password):
    ssh_client = paramiko.client.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh_client.connect(hostname=hostname,
                       port=22,
                       username=username,
                       password=password,
                       look_for_keys=False,
                       allow_agent=False)

    device_access = ssh_client.invoke_shell()
    print(f'\nPripojeny na SSHv2 zariadenie \"{hostname}\"')

    device_access.send(b'terminal length 0\n')
    device_access.send(b'show ip interface brief\n')
    time.sleep(5)

    output = device_access.recv(65535).decode()
    print(output)
    print('Parsujem vystup')
    int_iter = int_pattern.finditer(output)
    for interface in int_iter:
        print(interface)


bkp_threads_list = []

for device in [cat1sw]:
    bkp_thread = threading.Thread(target=cisco_int_parser, kwargs=device)
    bkp_threads_list.append(bkp_thread)
    bkp_thread.start()

for thread in bkp_threads_list:
    thread.join()
