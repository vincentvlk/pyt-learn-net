#!/usr/bin/python3

import requests
import sys

# Povolenie self-signed certifikatov

requests.packages.urllib3.disable_warnings()

# Prihlasovacie udaje

USER = "developer"
PASS = "C1sco12345"
HOST = "sandbox-iosxe-recomm-1.cisco.com"

# Nastavenie premennej na ake URL sa ma skript pripojit

url = f"https://{HOST}/restconf/data/ietf-interfaces:interfaces"

print()
print("Pripajam sa na URL:")
print(url)

# Nastavenie REST API hlaviciek

headers = {
		"Content-Type": "application/yang-data+json", 
	  	"Accept": "application/yang-data+json"
          }

# Spustenie testovacej  GET metody

response = requests.get(url, auth=(USER, PASS), headers=headers, verify=False)

print()
print("Odpoved z REST API servera:")
print()
print(response.text)

