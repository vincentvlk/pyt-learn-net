#!/usr/bin/env python3
'''
Jednoduchy Py3 skript generuje VXLAN-EVPN kofiguraciu pre Cis. Nexus 9K Switch.
Treba intalovat python modul s: '$ pip3 install colorama'
Kontrola s: '$ pip3 list'

by vlkv@Aug2022

DOROBIT: - check na validne cislo VNI (24-bit rozsah)
         - dat chybove hlasky do premennych
         - spravit funkciu na zadavanie VLAN, uz sa opakuje
         - osetrit zadavanie prefixu, aby to bolo cislo
'''

# importujeme potrebne moduly/kniznice:
import colorama
from colorama import Fore
import datetime
#
colorama.init(autoreset=True)
teraz = str(datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
#
bgp_as_num = '64512'
#
vrf_volba = ''
vrf_nazov = ''
vrf_l3_vlan = ''
pfx_vni = ''
pocet_vlan_vni_map = ''
zoznam_vlan = []
vni_max = ''
#
err_vlan_mimo = '\n-> CHYBA vstupu: Číslo VLANy mimo rozsah! (2-3967)\n'
err_zoznam_dupl = '\n-> CHYBA vstupu: Duplicita v zozname L2 VLAN!\n'
s_uvod = 'Jednoduchý Py3 skript generuje VXLAN-EVPN konf. pre Cisco Nexus Sw.'
s_treba = 'Treba zadať hodnoty VLAN a VNI prefixu tak, aby vzniklo platné VNI.'
s_limit = 'Skript generuje VNI tak, aby boli menšie ako 16777216 (24-bit VNI).'
s_vlan_summary = 'Zoznam VLAN na L2-VNI mapovanie: '
#
print(Fore.YELLOW + '\n' + s_uvod)
print(Fore.YELLOW + s_treba)
print(Fore.YELLOW + s_limit)

vrf_volba = input('\nGenerovať konfiguráciu do Tenant VRF? (a:Áno / n:Nie): ')

if vrf_volba == 'a':
    vrf_nazov = input('\nZadajte názov VRF pre VXLAN: ')

while vrf_volba == 'a':
    try:
        vrf_l3_vlan = input('Zadajte číslo VLAN na L3-VNI mapovanie: ')
        vrf_l3_vlan = int(vrf_l3_vlan)
        if (vrf_l3_vlan < 2 or vrf_l3_vlan > 3967):
            print(Fore.RED + err_vlan_mimo)
        else:
            break
    except Exception as err:
        print(Fore.RED + '\n-> CHYBA vstupu: ' + str(err) + '\n')

while True:
    try:
        pocet_vlan_vni_map = input('\nZadajte počet VLAN/L2-VNI mapovaní: ')
        pocet_vlan_vni_map = int(pocet_vlan_vni_map)
        break
    except Exception as err:
        print(Fore.RED + '\n--> CHYBA vstupu: ' + str(err) + '\n')

print()

for idx in range(pocet_vlan_vni_map):
    zoznam_vlan.append(idx)

    dupl = [number for number in zoznam_vlan if zoznam_vlan.count(number) > 1]

    while True:
        try:
            vstup = input('Zadajte číslo ' + str(idx + 1) + '. L2-VLANy: ')
            vstup = int(vstup)
            zoznam_vlan[idx] = vstup
            if (vstup < 2 or vstup > 3967):
                print(Fore.RED + err_vlan_mimo)
            else:
                break
        except Exception as err:
            print(Fore.RED + '\n-> CHYBA vstupu: ' + str(err) + '\n')

    dupl = [number for number in zoznam_vlan if zoznam_vlan.count(number) > 1]

    if len(dupl) > 0:
        print(Fore.RED + err_zoznam_dupl)
        stara_hodnota = zoznam_vlan[idx]
        while zoznam_vlan[idx] == stara_hodnota:
            vstup = input('Zadajte NOVÉ číslo ' + str(idx + 1) + '. VLANy: ')
            vstup = int(vstup)
            zoznam_vlan[idx] = vstup

dupl = [number for number in zoznam_vlan if zoznam_vlan.count(number) > 1]

if len(dupl) > 0:
    print(Fore.RED + err_zoznam_dupl)
    stara_hodnota = zoznam_vlan[idx]
    while zoznam_vlan[idx] == stara_hodnota:
        vstup = input('Zadajte NOVÉ číslo ' + str(idx + 1) + '. VLANy: ')
        vstup = int(vstup)
        zoznam_vlan[idx] = vstup

print()

while vrf_l3_vlan == '':
    try:
        pfx_vni = input('Zadajte prefix na generovanie VNI (max. 4 čísla): ')
        vni_max = (pfx_vni + str(max(zoznam_vlan)))
        pfx_vni = int(pfx_vni)
        print()
    except Exception as err:
        print(Fore.RED + '\n-> CHYBA vstupu: ' + str(err) + '\n')
        pfx_vni = 0
    if (pfx_vni < 1 or pfx_vni > 9999):
        print(Fore.RED + '\n-> CHYBA vstupu: Prefix mimo rozsah! (1-1677)\n')
        vrf_l3_vlan = ''
    elif int(vni_max) > 16777216:
        print(Fore.RED + '\n-> CHYBA vstupu: "Prefix+VLAN" mimo rozsah VNI!\n')
        vrf_l3_vlan = ''
    else:
        vrf_l3_vlan = pfx_vni

if vrf_l3_vlan != '':
    pfx_vni = vrf_l3_vlan

print('=' * 80)
print('Boli zadané tieto hodnoty:\n')

if vrf_volba == 'a':
    print('Generovať konfiguráciu do Tenant VRF: \tÁno')
    vni_max = (str(pfx_vni) + str(max(zoznam_vlan)))
else:
    print('Generovať konfiguráciu do Tenant VRF: \tNie')
    vrf_l3_vlan = ''

print('Názov VRF pre Tenant VXLAN-EVPN: \t' + vrf_nazov)
print('Číslo VLAN na L3-VNI mapovanie: \t' + str(vrf_l3_vlan))
print(s_vlan_summary + '\t' + str(zoznam_vlan))
print('Prefix na generovanie L2-VNI: \t\t' + str(pfx_vni))
print('VNI prefix + VLAN maximum: \t\t' + vni_max)
print('=' * 80)

# EOF
