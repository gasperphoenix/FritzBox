# Usage example:
#
# This example will return all switch plugs connected to the Fritz!Box
#
# Execute the script in the terminal but make sure to adapt the IP address
# and password to your needs.
#
# Example:
# ========
# $ python3 homeauto_example1.py "192.168.178.1" "PASSWORD"
# IP: 192.168.178.1
# Password: PASSWORD
# [*] Load all switch plugs currently connected to the Fritz!Box
# [*] Switch plug "087610520001" is on
# [*] Switch plug "087610510002" is on

import fritzbox.FBHomeAuto as fha
import sys

ip = sys.argv[1]
print(f'IP: {ip}')

password = sys.argv[2]
print(f'Password: {password}')

fb_ha = fha.FBHomeAuto(ip=ip, password=password)

print('[*] Load all switch plugs currently connected to the Fritz!Box')
switch_plugs = fb_ha.get_switch_plugs()

for switch in switch_plugs:
    state = 'on' if fb_ha.get_switch_plug_state(switch) else 'off'
    print(f'[*] Switch plug "{switch}" is {state}')
