#!/usr/bin/env python3
'''
toto je pokec a poznamky ku skriptu co hlada volne/obsadene VLANy
poznamka: show vlan id 100 | include active|not

na cisco box-e bol pridany user: 'username ssh privilege 15 secret ssh.2022'
'''
# importujeme potrebne moduly/kniznice:

from netmiko import Netmiko
from getpass import getpass
import datetime

# nastavime potrebne premenne:
# nastavujeme premennu 'teraz' s aktualnym systemovym casom, kvoli logovaniu

f_zoznam = 'flotila.zoznam'
uzivatel = 'ssh'

vlan_id = input('\nZadaj cislo hladanej VLAN: ')
prikaz = 'show vlan id ' + vlan_id + ' | include active|not'
teraz = str(datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))

# nacitame subor so zoznamom adries/zariadeni:
try:
    f = open(f_zoznam, 'r')
    b_zoznam = f.readlines()
except:
    print('\n' + teraz + ' --> CHYBA pri otvarani suboru: ' + f_zoznam + '\n')

# spustime for slucku, ktora sa na IP/name v zozname pripoji a vykona 'prikaz'
# do premennej 'vystup' ulozime odpoved zo zadaneho prikazu z prem. 'prikaz'
for riadok in b_zoznam :
    teraz = str(datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))

    print('\n' + teraz + ' --> Pripajam sa na adresu:', riadok)
    try:
        pripojenie = Netmiko(host = riadok,
                             device_type = 'cisco_nxos', 
                             username = uzivatel, 
                             password = 'ssh.2022')

        vystup = (pripojenie.send_command(prikaz))

    except:
        print(teraz + ' --> CHYBA pri SSH pripojeni na:', riadok)
        vystup = '-NEDOSTUPNY-'

    pripojenie.disconnect

    print('Odpoved z', riadok[:-1], ':', vystup)

#EOF
