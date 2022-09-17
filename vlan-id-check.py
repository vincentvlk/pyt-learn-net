#!/usr/bin/env python3
'''
Jednoduchy Py3 skript hlada volne/obsadene VLANy na Cis. Catalyst/Nexus Sw.
Treba intalovat python moduly s: $ pip3 install netmiko colorama
Kontrola s: $ pip3 list

pouzit pattern: "(\d+\s+\S+\s+active|not found in current VLAN database)"
kniznica "import re"

by vlkv@jul2022
'''

# importujeme potrebne moduly/kniznice:
from netmiko import Netmiko
from getpass import getpass
import colorama
from colorama import Fore
import datetime

'''
- nastavime potrebne premenne:
- nastavujeme premennu "teraz" s aktualnym systemovym casom, kvoli logovaniu
'''
colorama.init(autoreset=True)

f_zoznam = 'flotila.zoznam'
uzivatel = 'sshview'
teraz = str(datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))

# nacitame subor so zoznamom adries/zariadeni do bufferu:
try:
    f = open(f_zoznam, 'r')
    b_zoznam = f.readlines()
except Exception as err:
    print(Fore.RED + '\n' + teraz + ' --> CHYBA suboru: ' + f_zoznam + '\n')
    print(err)
    raise

vlan_id = input('\nZadajte cislo hladanej VLAN: ')
heslo = getpass('Zadajte SSH heslo pre uzivatela \"' + uzivatel + '\": ')
prikaz = 'show vlan id ' + vlan_id + ' | include active|not'

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

        vystup = (Fore.CYAN + pripojenie.send_command(prikaz))

    except Exception as err:
        print(Fore.RED + teraz + ' --> CHYBA pri SSH pripojeni na:', riadok)
        print(err)
        vystup = '-NEDOSTUPNA-\n'

    pripojenie.disconnect
    print(Fore.CYAN + 'Odpoved z', riadok[:-1], ':', vystup)

teraz = str(datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
print(teraz + ' --> KONIEC skriptu.')
