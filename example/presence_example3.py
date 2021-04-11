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
# Now execute this script presence_example3.py with the device name as third
# parameter. Make sure to adapt the IP address and password to your needs and
# follow the instructions on the terminal. It will request you to switch the
# WLAN on your device on or off.
#
# Example:
# ========
# $ python3 presence_example1.py "192.168.178.1" "PASSWORD" "iphone"
# IP: 192.168.178.1
# Password: PASSWORD
# Device to supervise: iphone
# [*] Starting device supervision
# [*] Toggle WLAN on device "iphone"
# [*] Toggle WLAN on device "iphone"
# [*] Toggle WLAN on device "iphone"
# [*] Toggle WLAN on device "iphone"
# Device "iphone" changed from present to absent
# [*] Toggle WLAN on device "iphone"
# [*] Toggle WLAN on device "iphone"
# [*] Toggle WLAN on device "iphone"
# [*] Toggle WLAN on device "iphone"
# Device "iphone" changed from absent to present
# [*] Toggle WLAN on device "iphone"
# [*] Toggle WLAN on device "iphone"
# ...

import fritzbox.FBPresence as fp
import sys
import time


def alert_change(device, old_state, new_state):
    # Do your stuff in case a device changes its presence state

    old_state = 'present' if old_state else 'absent'
    new_state = 'present' if new_state else 'absent'

    print(f'Device "{device}" changed from {old_state} to {new_state}')


ip = sys.argv[1]
print(f'IP: {ip}')

password = sys.argv[2]
print(f'Password: {password}')

device = sys.argv[3]
print(f'Device to supervise: {device}')

fb_p = fp.FBPresence(ip=ip, password=password)

print('[*] Starting device supervision')

fp.start_device_presence_supervision(fb_p,
                                     device,
                                     alert_change)

while True:
    print(f'[*] Toggle WLAN on device "{device}"')

    time.sleep(5)
