#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3
#
# Jednoduchy python skript, ktory generuje LoopBack rozhrania na labovanie
#
import os
#
rnum = input('Zadaj cislo routera: ')
rnum = str(rnum)
#
print('')
print('!')
print('end')
print('configure terminal')
#
i = 1
#
for i in range(1, 10):
    print('interface loopback' + str(rnum) + str(i))
    print('  ip address 192.168.'+ str(rnum) + '0.' + str(i) + ' 255.255.255.255')
    print('  ipv6 address fd00:' + str(rnum) + '0::' + str(i) + '/128')
#
print('end')
print('write memory')
print('!')
print('')
#
