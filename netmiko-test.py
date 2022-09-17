#!/usr/bin/env python3

'''
Jednoduchy Py3 skript "paramiko-test.py" na ucenie kniznice Netmiko.
'''

from netmiko import Netmiko

n91leaf1 = Netmiko(ip='192.168.5.201',
                   username='admin',
                   password='Cisco.123',
                   device_type='cisco_nxos')

print('Connected do N9-Leaf')
print(n91leaf1.find_prompt())

show_run = n91leaf1.send_command('show running-config')
print(show_run)

cat1sw = Netmiko(ip='192.168.5.211',
                 username='admin',
                 password='Cisco.123',
                 device_type='cisco_ios')

print('-=' * 40)

print('Connected do Cat1SW')
print(cat1sw.find_prompt())

show_run = cat1sw.send_command('show running-config')
print(show_run)

with open('n91_backup.txt', 'w') as moje_data:
    moje_data.write(show_run)
with open('cat1sw_backup.txt', 'w') as moje_data:
    moje_data.write(show_run)

print('-' * 10 + 'Koniec-skriptu' + '-' * 10)
