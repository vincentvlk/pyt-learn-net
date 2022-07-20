#!/usr/bin/env python3
'''
toto je pokec a poznamky ku skriptu co hlada volne/obsadene VLANy
poznamka: show vlan id 100 | include active|not
'''

from netmiko import Netmiko
import datetime

f_zoznam = 'flotila.zoznam'
dev_num = 1
vlan_id = 100

try:
    f = open(f_zoznam, 'r')
    b_zoznam = f.readlines()
except:
        print('\nNastala chyba pri otvarani suboru s adresami', f_zoznam, '\n')

for i in b_zoznam :
    print('\nPripajam sa na adresu:', i)
    try:
        pripojenie = Netmiko(host = i,
                             device_type = 'cisco_ios', 
                             username ='ssh', 
                             password = 'ssh.2022')

        vystup = (pripojenie.send_command('show vlan id 100 | include active|not'))
    except:
        print('Nastala chyba pri SSH pripojeni na:', i)
    
    pripojenie.disconnect
    print(vystup)
