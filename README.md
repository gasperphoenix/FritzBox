## Welcome to the FritzBox project

This project is derived from my former project [FritzBoxPresenceDetection](https://github.com/gasperphoenix/FritzBoxPresenceDetection) which provided the functionality to connect to an AVM FritzBox to check the presence of WLAN devices. While adding more features and the ability to interact with the FritzBox Home Automation actors (like switch plugs) using HTTP requests I decided to setup a complete new project with a new structure that encapsules the features for presence detection and home automation in separate modules. Furthermore I moved all the FritzBox communication related methods like authentication and lua-page loading to a new core module.

### Package structure

## FBCore
This module provides the class *FBCore* that encapsules all methods for communication with the FritzBox like authentication and loading of lua-pages.  

## FBPresence
## FBHomeAuto

### Using the distribution files
- Download
- Install
- Use in own module

### Using the source files
- Download
- Install
- Use in own module
