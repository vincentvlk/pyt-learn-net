#!/usr/bin/env python3
#
# Jednoduchy Python skript generuje zakladnu a IP konfiguraciu pre full-mesh
# zapojenie virtualnych routerov s OS Cisco IOS(-XE).
#
import os
#
rnum = input('Zadaj cislo routera: ')
rcount = input('Zadaj pocet routerov vo full-mesh topologii: ')
iftype = input('Zadaj typ routera (1: vIOS | 2: vIOS-XE:): ')
#
rnum = int(rnum)
rcount = int(rcount)
iftype = int(iftype)
mngint = ''
#
octB = 0
octC = 0
#
if iftype == 1:
    iftype = str(iftype)
    iftype = '0/'
    mngint = 'GigabitEthernet0/0'
else:
    iftype = str(iftype)
    iftype = ''
    mngint = 'GigabitEthernet' + str(rcount + 1)
#
print('')
print('! ---Generujem config pre Router R' + str(rnum) + '---')
print('!')
print('end')
print('enable')
print('configure terminal')
print('!')
#
print('clock timezone CET 1 0')
print('clock summer-time CEST recurring last Sun Mar 2:00 last Sun Oct 3:00')
print('!')
#
print('service timestamps debug datetime msec localtime show-timezone year')
print('service timestamps log datetime msec localtime show-timezone year')
print('!')
#
print('alias exec dsave copy running-config flash:r' + str(rnum) + '-clean-config.txt')
print('alias exec dconf configure replace flash:r' + str(rnum) + '-clean-config.txt force')
print('!')
#
print('hostname R' + str(rnum))
print('ipv6 unicast-routing')
print('no service config')
print('!')
#
print('vrf definition vrfmng')
print(' description manazment-vrf-pre-' + mngint)
print(' !')
print(' address-family ipv4')
print(' exit-address-family')
print(' !')
print(' address-family ipv6')
print(' exit-address-family')
print('!')
#
print('interface '+ mngint)
print(' description Manazment interface "vrfmng"')
print(' vrf forwarding vrfmng')
print(' ip address 192.168.1.'+ str(rnum + 200) + ' 255.255.255.0')
print(' no keepalive')
print(' no cdp enable')
print(' no mop enabled')
print(' no mop sysid')
print(' no shutdown')
print('exit')
print('!')
#
print('ip route vrf vrfmng 0.0.0.0 0.0.0.0 ' + mngint + ' 192.168.1.1')
print('!')
#
print('ip name-server vrf vrfmng 193.17.47.1')
print('ip name-server vrf vrfmng 185.43.135.1')
print('ip domain lookup source-interface ' + mngint)
print('ip domain-name gns3lab.local')
print('!')
#
print('ntp server vrf vrfmng ntp.nic.cz prefer')
print('!')
#
print('line console 0')
print(' exec-timeout 0 0')
print(' logging synchronous')
print(' escape-character 3')
print(' transport preferred none')
print(' privilege level 15')
print('exit')
print('!')
#
print('interface Loopback1')
print(' description Zakladny interface pre Router-ID')
print(' ip address 192.0.2.' + str(rnum) + ' 255.255.255.255')
print(' ipv6 address 2001:db8::' + str(rnum) + '/128')
print('!')
#
index = 1
#
for index in range(1, rcount + 1):
    if rnum != index:
        if rnum > index:
            octB = index
            octC = rnum
        else:
            octB = rnum
            octC = index
        print('interface GigabitEthernet' + iftype +str(index))
        print(' description Prepojenie z R' + str(rnum) + ' na router R' + str(index))
        print(' no ip redirects')
        print(' ip address 10.' + str(octB) + '.' + str(octC) + '.' + str(rnum) + ' 255.255.255.0')
        print(' ipv6 address fc00:' + str(octB) + ':' + str(octC) + '::' + str(rnum) + '/64')
        print(' no shutdown')
    #
#
print('end')
print('!')
print('copy running-config startup-config')
print('!')
print('')
#
# koniec skriptu
