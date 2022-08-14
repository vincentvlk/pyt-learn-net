#!/usr/bin/env python3
'''
Jednoduchý Py3 skript generuje VXLAN-EVPN kofiguráciu pre Cis. Nexus 9K Switch.
Treba inštalovať python modul s: '$ pip3 install colorama'
Kontrola s: '$ pip3 list'

Skript slúži ako testovací protoptyp a je na ňom čo zlepšovať / meniť. Základná
myšlienka je urýchlenie tvorby konf. syntaxe pre opakujúcu sa VXLAN-EVPN konf.
Ďalším cieľom je generovať konf. bez zásadných chýb, ktoré spomaľujú nasadenie.
Skript sa dá samozrejme použiť ako inšpirácia pre iné scenáre.

by vlkv@Aug2022

TODO:
'''
# Importujeme potrebné moduly / knižnice:
#
import colorama
from colorama import Fore
import datetime

###############################################################################
# Sekcia s nastavením premenných.
#
colorama.init(autoreset=True)
t_teraz = str(datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
# Podľa prostredia nastavíme MAC adresu pre Anycast GW, musí byť typu *Unicast*
#
any_gw_mac = '2022.2022.2022'
#
vrf_volba = ''
vrf_nazov = ''
vrf_l3_vlan = ''
pfx_volba = ''
pfx_vni = 0
pocet_vlan_vni_map = ''
zoznam_vlan = []
vni_max = ''
#
err_vlan_mimo = '\n-> CHYBA vstupu: Číslo VLANy mimo rozsah! (2-3967)\n'
err_zoznam_dupl = '\n-> CHYBA vstupu: Duplicita v zozname L2 VLAN!\n'
err_vni_mimo = '\n-> CHYBA vstupu: "Prefix+VLAN" mimo rozsah VNI! (16777216)\n'
err_pfx_mimo = '\n-> CHYBA vstupu: Prefix mimo rozsah! (1-9999)\n'
err_dup_l3vlan = '\n-> CHYBA vstupu: Toto číslo VLAN je duplicita s L3-VNI!\n'
#
s_uvod = 'Jednoduchý Py3 skript generuje VXLAN-EVPN konf. pre Cisco Nexus Sw.'
s_treba = 'Treba zadať hodnoty VLAN a VNI prefixu tak, aby vzniklo platné VNI.'
s_limit = 'Skript vkladá VNIs tak, aby boli menšie ako 16777216 (24-bit VNI).'
s_vlan_summary = 'Zoznam VLAN na L2-VNI mapovanie: '
s_vrf_volba = '\nGenerovať konfiguráciu do Tenant VRF? (a:Áno / n:Nie): '
s_pfx_volba = '\nChcete L3-VNI využiť ako prefix pre L2-VNI (a:Áno / n:Nie): '
s_vrf_ano = '\nBola zvolená konfigurácia s nasadením Tenant VRF.'
s_vrf_nie = '\nBola zvolená konfigurácia bez nasadenia Tenant VRF.'
s_pfx_ano = '\nPrefix pre L2-VNI sa bude generovať z hodnoty L3-VNI.'
s_pfx_nie = '\nPrefix pre L2-VNI sa nebude generovať z hodnoty L3-VNI.'
###############################################################################
# Sekcia, kde sa interaktívne zbierajú údaje od užívateľa.
# Je nasadená základá kontrolu vstupu, aby skript nepadal pri chybe a umožnil
# dodatočnú úpravu zadaných údajov. Na konci sekcie je výpis so sumárom
# vložených údajov:
#
print(Fore.YELLOW + '\n' + s_uvod)
print(Fore.YELLOW + s_treba)
print(Fore.YELLOW + s_limit)

vrf_volba = input(s_vrf_volba)

if vrf_volba == 'a':
    print(Fore.YELLOW + s_vrf_ano)
    vrf_nazov = input('\nZadajte názov VRF pre VXLAN: ')
else:
    print(Fore.YELLOW + s_vrf_nie)

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

if vrf_volba == 'a':
    pfx_volba = input(s_pfx_volba)

if pfx_volba == 'a':
    print(Fore.YELLOW + s_pfx_ano)
    pfx_vni = vrf_l3_vlan
else:
    print(Fore.YELLOW + s_pfx_nie)

while True:
    try:
        pocet_vlan_vni_map = input('\nZadajte počet VLAN / L2-VNI mapovaní: ')
        pocet_vlan_vni_map = int(pocet_vlan_vni_map)
        break
    except Exception as err:
        print(Fore.RED + '\n-> CHYBA vstupu: ' + str(err) + '\n')

print()

for idx in range(pocet_vlan_vni_map):
    zoznam_vlan.append(idx)

    while True:
        try:
            vstup = input('Zadajte číslo ' + str(idx + 1) + '. L2-VLAN: ')
            vstup = int(vstup)
            zoznam_vlan[idx] = vstup
            vni_max = (str(vrf_l3_vlan) + str(max(zoznam_vlan)))
            dupl = [num for num in zoznam_vlan if zoznam_vlan.count(num) > 1]
            if (vstup < 2 or vstup > 3967):
                print(Fore.RED + err_vlan_mimo)
            elif int(vni_max) > 16777216:
                print(Fore.RED + err_vni_mimo)
            elif len(dupl) > 0:
                print(Fore.RED + err_zoznam_dupl)
            elif vstup == vrf_l3_vlan:
                print(Fore.RED + err_dup_l3vlan)
            else:
                break
        except Exception as err:
            print(Fore.RED + '\n-> CHYBA vstupu: ' + str(err) + '\n')

print()

while pfx_vni == 0:
    try:
        pfx_vni = input('Zadajte prefix na generovanie VNI (max. 4 čísla): ')
        vni_max = (pfx_vni + str(max(zoznam_vlan)))
        pfx_vni = int(pfx_vni)
        print()
    except Exception as err:
        print(Fore.RED + '\n-> CHYBA vstupu: ' + str(err) + '\n')
        pfx_vni = 0
    # Táto podmienka sa dá v podstate odstrániť, ak používame nízke čísla VLAN:
    #
    if (pfx_vni < 1 or pfx_vni > 9999):
        print(Fore.RED + err_pfx_mimo)
        pfx_vni = 0
    elif int(vni_max) > 16777216:
        print(Fore.RED + err_vni_mimo)
        pfx_vni = 0
    else:
        pfx_vni = int(pfx_vni)

print(Fore.YELLOW + '=' * 80)
print(Fore.YELLOW + 'Boli zadané tieto hodnoty:\n')

if vrf_volba == 'a':
    print(Fore.YELLOW + 'Generovať konfiguráciu do Tenant VRF: \tÁno')
    vni_max = (str(pfx_vni) + str(max(zoznam_vlan)))
else:
    print(Fore.YELLOW + 'Generovať konfiguráciu do Tenant VRF: \tNie')
    vrf_l3_vlan = ''

print(Fore.YELLOW + 'Názov VRF pre Tenant VXLAN-EVPN: \t' + vrf_nazov)
print(Fore.YELLOW + 'Číslo VLAN na L3-VNI mapovanie: \t' + str(vrf_l3_vlan))
print(Fore.YELLOW + s_vlan_summary + '\t' + str(zoznam_vlan))
print(Fore.YELLOW + 'Prefix na generovanie L2-VNI: \t\t' + str(pfx_vni))
# Zakomentovaný riadok používam na ladenie generátora:
#
# print(Fore.YELLOW + 'String "VNI prefix + VLAN maximum": \t' + vni_max)
print(Fore.YELLOW + '=' * 80)

###############################################################################
# Sekcia na základe vložených údajov generuje základ VXLAN-EVPN služby.
#
print(Fore.YELLOW + '-> Generujem VXLAN-EVPN konfiguráciu:')
print(Fore.YELLOW + '=' * 80)
print('!')
print('! Nová VXLAN-EVPN konfigurácia vygenerovaná v čase: ' + t_teraz)
print('! Dôkladne SKONTROLUJTE vygenerovanú konfiguráciu!')

for idx in range(pocet_vlan_vni_map):
    print('!')
    print('vlan ' + str(zoznam_vlan[idx]))
    print('  name CustID-' + str(pfx_vni) + '-segment' + str(zoznam_vlan[idx]))
    print('  vn-segment ' + str(pfx_vni) + str(zoznam_vlan[idx]))

if vrf_volba == 'a':
    print('!')
    print('vlan ' + str(vrf_l3_vlan))
    print('  name L3-VNI-for-CustID-' + str(vrf_l3_vlan))
    print('  vn-segment ' + str(vrf_l3_vlan))

    print('!')
    print('vrf context ' + vrf_nazov)
    print('  rd auto')
    print('  vni ' + str(vrf_l3_vlan))
    print('  address-family ipv4 unicast')
    print('    route-target both auto')
    print('    route-target both auto evpn')

    print('!')
    print('interface Vlan' + str(vrf_l3_vlan))
    print('  description L3-VNI-for-CustID-' + str(vrf_l3_vlan))
    print('  no shutdown')
    print('  vrf member ' + vrf_nazov)
    print('  no ip redirects')
    print('  ip forward')

    print('!')
    print('fabric forwarding anycast-gateway-mac ' + any_gw_mac)
    for idx in range(pocet_vlan_vni_map):
        customer_ID = 'Customer-ID-' + str(vrf_l3_vlan)
        print('!')
        print('interface Vlan' + str(zoznam_vlan[idx]))
        print('  description ' + customer_ID + '-seg' + str(zoznam_vlan[idx]))
        print('  no shutdown')
        print('  vrf member ' + vrf_nazov)
        print('  no ip redirects')
        print('  ip address <VLOŽ-IP-ANYCAST-GW-VLAN' + str(zoznam_vlan[idx]))
        print('  fabric forwarding mode anycast-gateway')

print('!')
print('interface nve1')
if vrf_volba == 'a':
    print('  member vni ' + str(vrf_l3_vlan) + ' associate-vrf')
for idx in range(pocet_vlan_vni_map):
    print('  member vni ' + str(pfx_vni) + str(zoznam_vlan[idx]))
    print('    ingress-replication protocol bgp')

print('!')
print('evpn')
for idx in range(pocet_vlan_vni_map):
    print('  vni ' + str(pfx_vni) + str(zoznam_vlan[idx]) + ' l2')
    print('    rd auto')
    print('      route-target import auto')
    print('      route-target export auto')

print('!')
print('end')
print('!')
print('! Koniec vygenerovanej VXLAN-EVPN konfigurácie.')
print('!')
