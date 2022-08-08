#!/usr/bin/env python3
'''
Jednoduchy Py3 skript generuje VXLAN-EVPN config pre  Cis. Nexus Sw.
Treba intalovat python moduly s: $ pip3 install colorama
Kontrola s: $ pip3 list

by vlkv@Aug2022


DOROBIT: check na validne cislo VNI (24-bit rozsah)
'''

# importujeme potrebne moduly/kniznice:
import colorama
from colorama import Fore
import datetime

colorama.init(autoreset=True)
teraz = str(datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
vrf_volba = ''
vrf_nazov = ''
vrf_l3_vlan = ''
prefix_l2_vni = ''
pocet_vlan_vni_map = ''
zoznam_vlan = []

bgp_as_num = '64512'

print('\nJednoduchy Py3 skript generuje VXLAN-EVPN konf. pre Cisco Nexus Sw.')

vrf_volba = input('\nGenerovat konfiguraciu do Tenant VRF? (a:Ano / n:Nie): ')

while vrf_volba == 'a':
    vrf_nazov = input('\nZadajte nazov VRF pre VXLAN: ')
    try:
        vrf_l3_vlan = int(input('Zadajte cislo VLAN na L3-VNI mapovanie: '))
        break
    except Exception as err:
        print(Fore.RED + '\n --> CHYBA vstupu: ' + str(err) + '\n')

while True:
    try:
        pocet_vlan_vni_map = input('\nZadajte pocet VLAN / L2-VNI mapovani: ')
        pocet_vlan_vni_map = int(pocet_vlan_vni_map)
        break
    except Exception as err:
        print(Fore.RED + '\n --> CHYBA vstupu: ' + str(err) + '\n')

print()

for idx in range(pocet_vlan_vni_map):
    zoznam_vlan.append(idx)

    dupl = [number for number in zoznam_vlan if zoznam_vlan.count(number) > 1]

    while True:
        try:
            vstup = input('Zadajte cislo ' + str(idx + 1) + '. L2 VLANy : ')
            vstup = int(vstup)
            zoznam_vlan[idx] = vstup
            break
        except Exception as err:
            print(Fore.RED + '\n --> CHYBA vstupu: ' + str(err) + '\n')

    dupl = [number for number in zoznam_vlan if zoznam_vlan.count(number) > 1]

    if len(dupl) > 0:
        print(Fore.RED + '\n--> CHYBA vstupu: Duplicita v zozname!\n')
        stara_hodnota = zoznam_vlan[idx]
        while zoznam_vlan[idx] == stara_hodnota:
            vstup = input('Zadajte NOVE cislo ' + str(idx + 1) + '. VLANy : ')
            vstup = int(vstup)
            zoznam_vlan[idx] = vstup

dupl = [number for number in zoznam_vlan if zoznam_vlan.count(number) > 1]

if len(dupl) > 0:
    print(Fore.RED + '\n--> CHYBA vstupu: Duplicita v zozname!')
    stara_hodnota = zoznam_vlan[idx]
    while zoznam_vlan[idx] == stara_hodnota:
        vstup = input('Zadajte NOVE cislo ' + str(idx + 1) + '. VLANy : ')
        vstup = int(vstup)
        zoznam_vlan[idx] = vstup

print()
print(zoznam_vlan)

prefix_l2_vni = input('\nZadajte prefix pre VNI (napr. 4 cisla z c. zmluvy): ')
# EOF
