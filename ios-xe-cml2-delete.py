#!/usr/bin/python3

import requests

# Povolenie self-signed certifikatov

requests.packages.urllib3.disable_warnings()

# Prihlasovacie udaje

USER = "cisco"
PASS = "cisco"
HOST = "10.10.20.175"

# Nastavenie REST API hlaviciek

headers = {
            "Content-Type": "application/yang-data+json",
            "Accept": "application/yang-data+json"
          }

# Premenna 'payload' sa nastavuje na prazdnu

payload = {}

# Cyklus, ktory sa postupne pripaja na REST API routera a moze rozhrania podla rozsahu

for i in range(1,51):

        intname = 'Loopback' + str(i)
        print('Mazem rozhranie: ' + intname)
        
        url = f"https://{HOST}/restconf/data/ietf-interfaces:interfaces/interface="+intname
        print('Pripajam sa cez URL: ' + url) 
        response = requests.request('DELETE',url, auth=(USER, PASS), 
                                   headers=headers, data=payload, verify=False)

        print()
        print("Odpovede z REST API servera:")
        print()
        print("Status Code: " + str(response.status_code))
        print(response.text)

print("Cyklus a skript sa ukoncili.")

