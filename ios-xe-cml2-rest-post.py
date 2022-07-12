#!/usr/bin/python3

import requests

# Povolenie self-signed certifikatov

requests.packages.urllib3.disable_warnings()

# Prihlasovacie udaje

USER = "cisco"
PASS = "cisco"
HOST = "10.10.20.175"

# Nastavenie premennej na ake URL sa ma skript pripojit

url = f"https://{HOST}/restconf/data/ietf-interfaces:interfaces"

print()
print("Pripajam sa na URL:")
print(url)
print()

# Nastavenie REST API hlaviciek

headers = {
        "Content-Type": "application/yang-data+json",
        "Accept": "application/yang-data+json"
          }

int_num = 5

for i in range(1,2):
        ipaddr = "192.0.2." + str(i)
        n = str(i)
        print(f"-->Vytvaram Loopback{n} rozhranie s IPv4 adresou: "+ipaddr+"/32")

        payload = '\
        {\
            "ietf-interfaces:interface": {\
                "name": "Loopback' + str(i) + '",\
                "description": "RESTCONF pokus by vlkv",\
                "type": "iana-if-type:softwareLoopback",\
                "enabled": true,\
                "ietf-ip:ipv4": {\
                    "address": [\
                        {\
                            "ip": "192.0.2.' + str(i) + '",\
                            "netmask": "255.255.255.255"\
                        }\
                    ]\
                }\
            }\
         }'

        #print(payload)

        response = requests.request('POST',url, auth=(USER, PASS), 
                                   headers=headers, data=payload, verify=False)

        print()
        print("Odpovede z REST API servera:")
        print()
        print("Status Code: " + str(response.status_code))
        print(response.text)

print("Cyklus a skript sa ukoncili.")

