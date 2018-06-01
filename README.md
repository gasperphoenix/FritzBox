## Welcome to the FritzBox project

This project is derived from my former project [FritzBoxPresenceDetection](https://github.com/gasperphoenix/FritzBoxPresenceDetection) which provided the functionality to connect to an AVM FritzBox to check the presence of WLAN devices. While adding more features and the ability to interact with the FritzBox Home Automation actors (like switch plugs) using HTTP requests I decided to setup a complete new project with a new structure that encapsules the features for presence detection and home automation in separate modules. Furthermore I moved all the FritzBox communication related methods like authentication and lua-page loading to a new core module.

### Package structure

## FBCore
This module provides the class *FBCore* that encapsules all methods for communication with the FritzBox like authentication and loading of lua-pages.  

## FBPresence
This module provides the class *FBPresence* that encapsules all methods for determination of the WLAN device connection status on the FritzBox.  

## FBHomeAuto
This module provides the class *FBHomeAuto* that encapsules all methods for interacting with the AVM home automation actors connected to a FritzBox.

### Using the distribution files
First you need to download a source distribution file from ...

Afterwards you can easily install it on your environment by invoking the following command. As the packet name may differ, please adapt it before executing the command.
```bash
sudo pip3 install fritzbox-0.1.tar.gz
```

Once successfully installed you can use the packet inside your scripts. Please find an example below.
```python
from fritzbox.FBHomeAuto import FBHomeAuto

fbHA = FBHomeAuto(ip="192.168.0.1", password="pass1234")

print(fbHA.getSwitchPlugs())
```