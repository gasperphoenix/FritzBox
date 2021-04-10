# Usage example:
#
# This script will check the presence of all devices currently connected to
# the Fritz!Box
#
# Execute the script in the terminal and follow the instructions given on
# the terminal output. Make sure to adapt the IP address and password to your
# needs.
#
# Example:
# ========
# $ python3 presence_example1.py "192.168.178.1" "PASSWORD"
# IP: 192.168.178.1
# Password: PASSWORD
# [*] Load all devices currently connected to the Fritz!Box
# [*] Check presence of all devices
# [*] Device "iphone" is currently present
# [*] Device "laptop" is currently present
# [*] Device "playstation" is currently present

import fritzbox.FBPresence as fp
import sys

ip = sys.argv[1]
print(f'IP: {ip}')

password = sys.argv[2]
print(f'Password: {password}')

fb_p = fp.FBPresence(ip=ip, password=password)

print('[*] Load all devices currently connected to the Fritz!Box')
devices, chk_ts = fb_p.get_wlan_device_information()

print('[*] Check presence of all devices')
for device in devices.keys():
    state = 'present' if fb_p.is_device_present(device_name=device) \
        else 'absent'

    print(f'[*] Device "{device}" is currently {state}')
