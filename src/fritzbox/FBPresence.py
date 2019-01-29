# -*- coding: utf-8 -*-
"""Module for communication with a FritzBox.

This module provides an interface for communicating with a FritzBox.
"""

__author__     = "Dennis Jung"
__copyright__  = "Copyright 2018, Dennis Jung"
__credits__    = ["Dennis Jung"]
__license__    = "GPL Version 3"
__maintainer__ = "Dennis Jung"
__email__      = "Dennis.Jung@stressfrei-arbeiten.com"


#===============================================================================
# Imports
#===============================================================================
import argparse
import logging
import urllib.request
import hashlib
import re
import json
import time
from xml.dom import minidom
import xml.etree.ElementTree as ElementTree

from fritzbox import FBCore


#===============================================================================
# Evaluate parameters
#===============================================================================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage="%(prog)s [options]", 
                                     description="In case no option is selected the script will "
                                     "return the list of all known devices including their WLAN presence status. " 
                                     "If --name or --mac is specified it will return 'True' if the device is present, 'False' otherwise. "
                                     "Debouncing of the transitions to absent is not supported if the script is used as command line tool.")
    
    parser.add_argument('--v1', 
                      help='Debug level INFO', 
                      dest='verbose_INFO',
                      default=False,
                      action='store_true')
    parser.add_argument('--v2', 
                        help='Debug level ERROR', 
                        dest='verbose_ERROR',
                        default=False,
                        action='store_true')
    parser.add_argument('--v3', 
                        help='Debug level DEBUG', 
                        dest='verbose_DEBUG',
                        default=False,
                        action='store_true')
    
    parser.add_argument('-i',
                        '--ip', 
                        help='IP adress of the FritzBox, eg. "192.168.0.1"', 
                        dest='ip',
                        default="192.168.0.1",
                        action='store',
                        required=True)
    parser.add_argument('-p',
                        '--password', 
                        help='Password for accessing the FritzBox, eg. "mysecret123"', 
                        dest='password',
                        default="password",
                        action='store',
                        required=True)
    
    parser.add_argument('-n',
                        '--name', 
                        help='Check presence of device identified by its name registered on the FritzBox', 
                        dest='name',
                        action='store')
    
    args = parser.parse_args()


#===============================================================================
# Setup logger
#===============================================================================
if __name__ == '__main__':
    log_level = logging.CRITICAL
    
    if args.verbose_INFO: log_level = logging.INFO
    if args.verbose_ERROR: log_level = logging.ERROR
    if args.verbose_DEBUG: log_level = logging.DEBUG
    
#    logging.basicConfig(level=log_level,
#                        format="[{asctime}] - [{levelname}] - [{process}:{thread}] - [{filename}:{funcName}():{lineno}]: {message}",
#                        datefmt="%Y-%m-%d %H:%M:%S",
#                        style="{")

    logging.basicConfig(level=log_level,
                        format="[{asctime}] - [{levelname}]: {message}",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        style="{")
        
logger = logging.getLogger(__name__)


#===============================================================================
# Constant declarations
#===============================================================================


#===============================================================================
# Exceptions
#===============================================================================
class InvalidParameterError(Exception): pass


#===============================================================================
# Class definitions
#===============================================================================
class FBPresence():
    """Interface for communication with a FritzBox.
    
    This class provides an interface for communication with a FritzBox using LUA pages.
    """
    
    def __init__(self, ip, password):
        self.fb = FBCore.FritzBox(ip, password)
                
        self.deviceList = {}
        self.chk_ts = 0
    
    
    def __del__(self):
        pass
        
    
    def isDevicePresent(self, deviceName=None, debounceOff=0):
        """Check if the given device is currently in WLAN access range -> device is present.
        
        The method checks if the specified device is currently in WLAN access range of the FritzBox
        to determine if it is present or not. You can optionally specify a debounce time for the transition
        to the absent state. This is helpful if you observe sporadic absent detections e.g. for iPhone
        devices.
                
        Args:
            deviceName (str): Device that shall be checked.
            debounceOff (int):  Debounce transition to absent by this no. of minutes
            
        Raises:
            UnknownDeviceError: If the given device is not registered with the FritzBox 

        Returns:
            If the device is registered with the FritzBox the method will return True if the device is present, False otherwise.
        """
        
        devices, chk_ts = self.getWLANDeviceInformation()
        
        if deviceName is not None:
            logger.debug("Check if the device " + deviceName + " is present")
            
            if deviceName in devices:
                if chk_ts - devices[deviceName]['on_ts'] == 0:
                    return True # Device is present
                elif chk_ts - devices[deviceName]['on_ts'] <= 60 * debounceOff:
                    return True # Device is absent less than the defined debounce time
                else:
                    return False # Device is absent for more than the defined debounce time
            else:
                return False # Device is not listed and therefore not present
        else:
            raise InvalidParameterError()
        
        return False

        
    def getWLANDeviceInformation(self):
        """Query WLAN information for all FritzBox known devices.
        
        The method queries all WLAN related information for all devices known to the FritzBox.
        
        Args:
            None

        Returns:
            deviceList (List): List with all devices and information as two-dimensional matrix. The parameters for each device
                               are accessible using the index FB_WLAN_DEV_INFO elements.
                        
            chk_ts (float):    Timestamp of the last presence check
        """
        
        logger.debug("Load WLAN device information from the FritzBox for all known devices")
        
        self.chk_ts = time.time()
        
        page = self.fb.loadFritzBoxPage('/data.lua', 'lang=de&no_sidrenew=&page=wSet')

        jsonStructure = json.loads(page.decode('UTF-8'))
        
        jsonStructure_devices = jsonStructure['data']['net']['devices']
        
        for i in range(len(jsonStructure_devices)):
            name = jsonStructure_devices[i]['name']
            on_ts = self.chk_ts
            
            self.deviceList[name] = {'on_ts' : on_ts}
                
        return self.deviceList, self.chk_ts
            

#===============================================================================
# Main program
#===============================================================================
def main():    
    fbP = FBPresence(ip=args.ip, password=args.password)
    
    if (args.name == None):
        devices, chk_ts = fbP.getWLANDeviceInformation()
        
        print(devices)
        
    elif (args.name != None):
        print(fbP.isDevicePresent(deviceName=args.name))
        
    
if __name__ == '__main__':
    main()