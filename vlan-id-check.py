#!/usr/bin/env python3
'''
toto je pokec a poznamky ku skriptu co hlada volne/obsadene VLANy
poznamka: show vlan id 100 | include active|not

na cisco box-e bol pridany user s prikazom: 'username ssh privilege 15 secret ssh.2022'
'''

from netmiko import Netmiko
import datetime

f_zoznam = 'flotila.zoznam'
uzivatel = 'ssh'
vlan_id = input('\nZadaj cislo hladanej VLAN: ')
prikaz = 'show vlan id ' + vlan_id + ' | include active|not'

try:
    f = open(f_zoznam, 'r')
    b_zoznam = f.readlines()
except:
        print('\nNastala chyba pri otvarani suboru s adresami', f_zoznam, '\n')

for riadok in b_zoznam :
    teraz = str(datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
    print('\n' + teraz + ' --> Pripajam sa na adresu:', riadok)
    try:
        pripojenie = Netmiko(host = riadok,
                             device_type = 'cisco_ios', 
                             username = uzivatel, 
                             password = 'ssh.2022')

        vystup = (pripojenie.send_command(prikaz))

    except:
        print('Nastala chyba pri SSH pripojeni na:', riadok)
    
    pripojenie.disconnect

    print('Odpoved z', riadok[:-1], ':', vystup)
