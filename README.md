## Welcome to the FritzBox project

This project is derived from my former project [FritzBoxPresenceDetection](https://github.com/gasperphoenix/FritzBoxPresenceDetection) which provided the functionality to connect to an AVM FritzBox to check the presence of WLAN devices. While adding more features and the ability to interact with the FritzBox Home Automation actors (like switch plugs) using HTTP requests I decided to setup a complete new project with a new structure that encapsules the features for presence detection and home automation in separate modules. Furthermore I moved all the FritzBox communication related methods like authentication and lua-page loading to a new core module.

## Package structure

### FBCore
This module provides the class *FBCore* that encapsules all methods for communication with the FritzBox like authentication and loading of lua-pages.  

### FBPresence
This module provides the class *FBPresence* that encapsules all methods for determination of the WLAN device connection status on the FritzBox.  

### FBHomeAuto
This module provides the class *FBHomeAuto* that encapsules all methods for interacting with the AVM home automation actors connected to a FritzBox.

## Using the distribution files
First you need to clone a sandbox from this project.

```bash
cd ~

git clone https://github.com/gasperphoenix/FritzBox
```

Afterwards you can easily install it on your environment by invoking the following command. 

```bash
cd ~/FritzBox

pip3 install dist/fritzbox-*.wheel
```

Please refer to the example scripts as reference how to use this package. They
are stored in the "example" subfolder of the project.

Basic example for presence supervision:

```python
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
```

## Create source distribution
First you need to install all required dependencies.
```
pip3 install setuptools
```

Before creating the source distribution make sure to adapt the following attributes in the file setup.py to your needs.
```
    name = "fritzbox",
    version = "0.2",
```

To create the source distribution go to the root folder of the archive and execute the following command
```
sh create_dist.sh
```

This creates a distribution in the wheel format in the subfolder "dist" which
can be installed using pip. Please refer to the description above.


## Execute module tests
First you need to install all required dependencies.
```
pip3 install openpyxl pytest pytest-cov
```

A shell script module has been added to execute all included module tests. To execute the module tests execute the following command in the root folder of the source code:
```
sh execute_unit_test.sh
```
