#!/usr/bin/python3
from netmiko import ConnectHandler
import json

"""
Nastavime parametre premennej nx_os
"""

nx_os = {
    "device_type": "cisco_ios",
    "ip": "10.10.20.177",
    "username": "cisco",
    "password": "cisco",
    "port": 22
}

net_connect = ConnectHandler(**nx_os)
output = net_connect.send_command("show ip interface brief | json-pretty")

json_data = json.loads(output)
int_number = len(json_data["TABLE_intf"]["ROW_intf"])

for x in range(int_number):
    print("Nazov: " + json_data["TABLE_intf"]["ROW_intf"][x]["intf-name"])
    print("Adresa: " + json_data["TABLE_intf"]["ROW_intf"][x]["prefix"])
    print("Stav: " + json_data["TABLE_intf"]["ROW_intf"][x]["proto-state"])
    print()
