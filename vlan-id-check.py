#!/usr/bin/env python3
'''
Jednoduchy Pyt3 skript hlada volne/obsadene VLANy na Cis. Catalyst/Nexus sw.
Je potrebne intalovat python modul: $ pip3 install netmiko
by vlkv@jul2022
'''
# importujeme potrebne moduly/kniznice:

from netmiko import Netmiko
from getpass import getpass
import datetime

'''
- nastavime potrebne premenne:
- nastavujeme premennu "teraz" s aktualnym systemovym casom, kvoli logovaniu
'''
f_zoznam = 'flotila.zoznam'
uzivatel = 'sshview'

vlan_id = input('\nZadaj cislo hladanej VLAN: ')
heslo = getpass('Zadajte SSH heslo pre uzivatela \"' + uzivatel + '\": ')

prikaz = 'show vlan id ' + vlan_id + ' | include active|not'
teraz = str(datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))

# nacitame subor so zoznamom adries/zariadeni do bufferu:
try:
    f = open(f_zoznam, 'r')
    b_zoznam = f.readlines()
except FileNotFoundError:
    print('\n' + teraz + ' --> CHYBA pri otvarani suboru: ' + f_zoznam + '\n')

print()

'''
- spustime for slucku, ktora sa na IP/name v zozname pripoji a vykona "prikaz"
- do premennej "vystup" ulozime odpoved zo zadaneho prikazu z prem. "prikaz"
'''
for riadok in b_zoznam:
    teraz = str(datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))

    print(teraz + ' --> Pripajam sa na adresu:', riadok)
    try:
        pripojenie = Netmiko(host=riadok,
                             device_type='cisco_nxos',
                             username=uzivatel,
                             password=heslo)

        vystup = (pripojenie.send_command(prikaz))

    except (Netmiko.ssh_exception):
        print(teraz + ' --> CHYBA pri SSH pripojeni na:', riadok)
        vystup = '-NEDOSTUPNY-'

    pripojenie.disconnect

    print('Odpoved z', riadok[:-1], ':', vystup)

teraz = str(datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
print(teraz + ' --> KONIEC skriptu.')
