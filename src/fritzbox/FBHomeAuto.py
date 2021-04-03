# -*- coding: utf-8 -*-
"""Module for communication with a FritzBox.

This module provides an interface for communicating with a FritzBox.
"""

import _info

__author__     = _info.__author__
__copyright__  = _info.__copyright__
__credits__    = _info.__credits__
__license__    = _info.__license__
__maintainer__ = _info.__maintainer__
__email__      = _info.__email__


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

import FBCore


#===============================================================================
# Evaluate parameters
#===============================================================================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage="%(prog)s [options]",
                                     description="In case no option is selected the script will "
                                     "return the list of all known devices including their WLAN presence status. "
                                     "If --name or --mac is specified it will return 'True' if the device is present, "
                                     " 'False' otherwise. Debouncing of the transitions to absent is not supported if "
                                     "the script is used as command line tool.")

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

    if args.verbose_INFO:
        log_level = logging.INFO

    if args.verbose_ERROR:
        log_level = logging.ERROR

    if args.verbose_DEBUG:
        log_level = logging.DEBUG

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
class InvalidParameterError(Exception):
    """Parameter error class"""
    pass


#===============================================================================
# Class definitions
#===============================================================================
class FBHomeAuto(object):
    """Interface for communication with a FritzBox.

    This class provides an interface for communication with a FritzBox using LUA pages.
    """

    def __init__(self, ip, password):
        self.fb = FBCore.FritzBox(ip, password)


    def __del__(self):
        pass


    def get_switch_plugs(self):
        """Load the AINs of all available switch plugs from the FritzBox.

        This method reads out the AINs of all switch plugs registered with the FritzBox and
        returns them as a list.

        Args:
            Does not require any arguments.

        Returns:
            Returns a list with all AINs of registered switch plugs
        """

        logger.debug("Load the AINs of all available switch plugs from the FritzBox")

        page = self.fb.load_fritzbox_page('/webservices/homeautoswitch.lua', '&switchcmd=getswitchlist')

        switch_plugs = page.decode('UTF-8').strip('\n').split(',')

        return switch_plugs


    def get_switch_plug_state(self, switch_plug_ain):
        """Load the switch state of the given switch plug from the FritzBox.

        This method returns the switch state of the requested switch plug.

        Args:
            switch_plug_ain (str):    The AIN of the switch plug that should be checked

        Returns:
            Returns the state of the switch plug
        """

        logger.debug("Load the switch state of the given switch plug from the FritzBox")

        page = self.fb.loadFritzBoxPage('/webservices/homeautoswitch.lua', '&switchcmd=getswitchstate&ain=' +
                                        switch_plug_ain)

        switch_plug_state = page.decode('UTF-8').strip('\n')

        return switch_plug_state


    def set_switch_plug_state(self, switch_plug_ain, state):
        """Set the switch state of the given switch plug.

        This method sets the switch state of the requested switch plug.

        Args:
            switch_plug_ain (str): The AIN of the switch plug that should be set
            state (str):           Target state 'on' or 'off'

        Returns:
            Does not return any value.
        """

        logger.debug("Set the switch state for a given switch plug using the FritzBox")

        if state == 'on':
            page = self.fb.loadFritzBoxPage('/webservices/homeautoswitch.lua', '&switchcmd=setswitchon&ain=' +
                                            switch_plug_ain)
        elif state == 'off':
            page = self.fb.loadFritzBoxPage('/webservices/homeautoswitch.lua', '&switchcmd=setswitchoff&ain=' +
                                            switch_plug_ain)
        else:
            pass

        switch_plug_state = page.decode('UTF-8').strip('\n')

        return switch_plug_state


    def toggle_switch_plug_state(self, switch_plug_ain):
        """Toggle the state of the given switch plug.

        This method toggles the state of the requested switch plug.

        Args:
            switch_plug_ain (str): The AIN of the switch plug that should be set

        Returns:
            Does not return any value.
        """

        logger.debug("Toggle the switch state for a given switch plug using the FritzBox")

        page = self.fb.loadFritzBoxPage('/webservices/homeautoswitch.lua', '&switchcmd=setswitchtoggle&ain=' +
                                        switch_plug_ain)

        switch_plug_state = page.decode('UTF-8').strip('\n')

        return switch_plug_state


#===============================================================================
# Main program
#===============================================================================
def main():
    """Main function for testing purpose"""
    fb_ha = FBHomeAuto(ip=args.ip, password=args.password)

    switch_plugs = fb_ha.get_switch_plugs()
    print(switch_plugs)


if __name__ == '__main__':
    main()
