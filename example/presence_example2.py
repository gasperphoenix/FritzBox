# Usage example:
#
# This example will supervise the presence of a device connected to
# the Fritz!Box and print a message every time the device enters or leaves
# the Fritz!Box WLAN
#
# Execute the script presence_example1.py in the terminal and note one
# device name from the output. In this example "iphone".
#
# Example:
# ========
# $ python3 presence_example1.py "192.168.178.1" "PASSWORD"
# IP: 192.168.178.1
# Password: PASSWORD
# [*] Load all devices currently connected to the Fritz!Box
# [*] Check presence of all devices
# [*] Device "iphone" is currently present
# ...
#
# Now execute this script presence_example2.py with the device name as third
# parameter. Make sure to adapt the IP address and password to your needs.
#
# Example:
# ========
# $ python3 presence_example1.py "192.168.178.1" "PASSWORD" "iphone"
# IP: 192.168.178.1
# Password: PASSWORD
# Device to supervise: iphone
# [*] Load initial presence state of device "iphone"
# [*] Deactivate WLAN for device "iphone"
# [*] Deactivate WLAN for device "iphone"
# [*] Deactivate WLAN for device "iphone"
# [*] Deactivate WLAN for device "iphone"
# [*] Deactivate WLAN for device "iphone"
# [*] Deactivate WLAN for device "iphone"
# [*] Deactivate WLAN for device "iphone"
# [*] Status of "iphone" changed from "present" to "absent"
# [*] Activate WLAN for device "iphone"
# [*] Activate WLAN for device "iphone"
# [*] Activate WLAN for device "iphone"
# [*] Activate WLAN for device "iphone"
# [*] Activate WLAN for device "iphone"
# [*] Activate WLAN for device "iphone"
# [*] Status of "iphone" changed from "absent" to "present"
# [*] Deactivate WLAN for device "iphone"
# [*] Deactivate WLAN for device "iphone"

import fritzbox.FBPresence as fp
import sys

ip = sys.argv[1]
print(f'IP: {ip}')

password = sys.argv[2]
print(f'Password: {password}')

device = sys.argv[3]
print(f'Device to supervise: {device}')

fb_p = fp.FBPresence(ip=ip, password=password)

print(f'[*] Load initial presence state of device "{device}"')
old_state = 'present' if fb_p.is_device_present(device_name=device) \
    else 'absent'

# Supervise present state changes
while True:
    new_state = 'present' if fb_p.is_device_present(device_name=device) \
        else 'absent'

    if new_state != old_state:
        print(f'[*] Status of "{device}" changed from "{old_state}" to "{new_state}"')

        old_state = new_state

    if new_state == 'present':
        print(f'[*] Deactivate WLAN for device "{device}"')
    else:
        print(f'[*] Activate WLAN for device "{device}"')

