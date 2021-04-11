# Minimal usage example:
#
# This example will supervise the presence of a device connected to
# the Fritz!Box and print a message every time the device enters or leaves
# the Fritz!Box WLAN. It assumes the following setting:
#
# ip: 192.168.178.1
# password: PASSWORD
# device: iphone
#
# Example:
# ========
# $ python3 presence_example4.py
# [*] Starting device supervision
# Device "iphone" changed from present to absent
# Device "iphone" changed from absent to present
# ...

import fritzbox.FBPresence as fp

ip = '192.168.178.1'
password = 'PASSWORD'
device = 'iphone'

def alert_change(device, old_state, new_state):
    old_state = 'present' if old_state else 'absent'
    new_state = 'present' if new_state else 'absent'

    print(f'Device "{device}" changed from {old_state} to {new_state}')


fb_p = fp.FBPresence(ip=ip, password=password)

print('[*] Starting device supervision')
fp.start_device_presence_supervision(fb_p,
                                     device,
                                     alert_change)

while True:
    pass
