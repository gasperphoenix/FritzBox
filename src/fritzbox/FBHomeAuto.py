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
class FBHomeAuto():
    """Interface for communication with a FritzBox.
    
    This class provides an interface for communication with a FritzBox using LUA pages.
    """
    
    def __init__(self, ip, password):
        self.fb = FBCore.FritzBox(ip, password)
    
    
    def __del__(self):
        pass
    
    
    def getSwitchPlugs(self):
        logger.debug("Load the AINs of all available switch plugs from the FritzBox")
                
        page = self.fb.loadFritzBoxPage('/webservices/homeautoswitch.lua', '&switchcmd=getswitchlist')
        
        switchPlugs = page.decode('UTF-8').strip('\n').split(',')
        
        return switchPlugs
    
    
    def getSwitchPlugState(self, switchPlugAIN):
        logger.debug("Load the switch state of the given switch plug from the FritzBox")
        
        page = self.fb.loadFritzBoxPage('/webservices/homeautoswitch.lua', '&switchcmd=getswitchstate&ain=' + switchPlugAIN)
        
        switchPlugState = page.decode('UTF-8').strip('\n')
        
        return switchPlugState
    
    
    def setSwitchPlugState(self, switchPlugAIN, state):
        logger.debug("Set the switch state for a given switch plug using the FritzBox")
        
        if (state == 'on'):
            page = self.fb.loadFritzBoxPage('/webservices/homeautoswitch.lua', '&switchcmd=setswitchon&ain=' + switchPlugAIN)
        elif (state == 'off'):
            page = self.fb.loadFritzBoxPage('/webservices/homeautoswitch.lua', '&switchcmd=setswitchoff&ain=' + switchPlugAIN)
        else:
            pass
        
        switchPlugState = page.decode('UTF-8').strip('\n')
        
        return switchPlugState
    
    
    def toggleSwitchPlugState(self, switchPlugAIN):
        logger.debug("Toggle the switch state for a given switch plug using the FritzBox")
        
        page = self.fb.loadFritzBoxPage('/webservices/homeautoswitch.lua', '&switchcmd=setswitchtoggle&ain=' + switchPlugAIN)
        
        switchPlugState = page.decode('UTF-8').strip('\n')
        
        return switchPlugState
    
    
#===============================================================================
# Main program
#===============================================================================
def main():    
    fbHA = FBHomeAuto(ip=args.ip, password=args.password)
    
    switchPlugs = fbHA.getSwitchPlugs()
    print(switchPlugs)
        
    
if __name__ == '__main__':
    main()