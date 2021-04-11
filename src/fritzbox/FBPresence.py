# -*- coding: utf-8 -*-
"""Module for communication with a FritzBox.

This module provides an interface for communicating with a FritzBox.
"""

import fritzbox._info

__author__     = fritzbox._info.__author__
__copyright__  = fritzbox._info.__copyright__
__credits__    = fritzbox._info.__credits__
__license__    = fritzbox._info.__license__
__maintainer__ = fritzbox._info.__maintainer__
__email__      = fritzbox._info.__email__


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
import collections
import threading

import fritzbox.FBCore


#===============================================================================
# Evaluate parameters
#===============================================================================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage="%(prog)s [options]",
                                     description="In case no option is selected the script will "
                                     "return the list of all known devices including their WLAN presence status. "
                                     "If --name or --mac is specified it will return 'True' if the device is present, "
                                     "'False' otherwise. Debouncing of the transitions to absent is not supported if "
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
# Global variables
#===============================================================================
device_states = collections.defaultdict(dict)


#===============================================================================
# Exceptions
#===============================================================================
class InvalidParameterError(Exception):
    """Parameter error class"""
    pass


#===============================================================================
# Method definitions
#===============================================================================
def _supervise_device_presence_changes(fbpresence, device, callback):
    """Thread method for the presence supervision

    The callback function needs to implement the following signature:
        callback(device, old_state, new_state):
            device (str): Device name
            old_state (bool): True=present, False=absent
            new_state (bool): True=present, False=absent

    Args:
        fbpresence (fritzbox.FBPresence.FBPresence): FBPresence object
        device (str): Name of a device registered to the Fritz!Box WLAN
        callback (function): Reference to a function that shall be called
            everytime the device state changes.
    """

    global device_states

    if device not in device_states.keys():
        old_state = fbpresence.is_device_present(device_name=device)
    else:
        old_state = device_states[device]

    while True:
        new_state = fbpresence.is_device_present(device_name=device)

        if new_state != old_state:
            callback(device,
                     old_state,
                     new_state)

        old_state = new_state
        device_states[device] = new_state


def start_device_presence_supervision(fbpresence, device, callback):
    """Start a presence supervision for a device

    Registers a callback that will be called everytime the presence state
    of a device changes.

    The callback function needs to implement the following signature:
        callback(device, old_state, new_state):
            device (str): Device name
            old_state (bool): True=present, False=absent
            new_state (bool): True=present, False=absent

    Args:
        fbpresence (fritzbox.FBPresence.FBPresence): FBPresence object
        device (str): Name of a device registered to the Fritz!Box WLAN
        callback (function): Reference to a function that shall be called
            everytime the device state changes.

    Returns:
        thread (threading.Thread): Thread created for the supervision

    Examples:
        ...
    """

    t = threading.Thread(target=_supervise_device_presence_changes,
                         args=(fbpresence, device, callback),
                         daemon=True)

    t.start()


#===============================================================================
# Class definitions
#===============================================================================
class FBPresence(object):
    """Interface for communication with a FritzBox.

    This class provides an interface for communication with a FritzBox using LUA pages.
    """

    def __init__(self, ip, password):
        self.fb = fritzbox.FBCore.FritzBox(ip, password)

        self.device_list = {}
        self.chk_ts = 0


    def __del__(self):
        pass


    def is_device_present(self, device_name=None, debounce_off=0):
        """Check if the given device is currently in WLAN access range -> device is present.

        The method checks if the specified device is currently in WLAN access range of the FritzBox
        to determine if it is present or not. You can optionally specify a debounce time for the transition
        to the absent state. This is helpful if you observe sporadic absent detections e.g. for iPhone
        devices.

        Args:
            device_name (str): Device that shall be checked.
            debounce_off (int):  Debounce transition to absent by this no. of minutes

        Returns:
            If the device is registered with the FritzBox the method will return True if the device is present,
            False otherwise.
        """

        devices, chk_ts = self.get_wlan_device_information()

        if device_name is not None:
            logger.debug("Check if the device " + device_name + " is present")

            if device_name in devices:
                if chk_ts - devices[device_name]['on_ts'] == 0:
                    # Device is present
                    return True
                elif chk_ts - devices[device_name]['on_ts'] <= 60 * debounce_off:
                    # Device is absent less than the defined debounce time
                    return True
                else:
                    # Device is absent for more than the defined debounce time
                    return False
            else:
                # Device is not listed and therefore not present
                return False
        else:
            raise InvalidParameterError()

        return False


    def get_wlan_device_information(self):
        """Query WLAN information for all FritzBox known devices.

        The method queries all WLAN related information for all devices known to the FritzBox.

        Args:
            None

        Returns:
            device_list (List): List with all devices and information as two-dimensional matrix. The
                                parameters for each device are accessible using the index
                                FB_WLAN_DEV_INFO elements.

            chk_ts (float):    Timestamp of the last presence check
        """

        logger.debug("Load WLAN device information from the FritzBox for all known devices")

        self.chk_ts = time.time()

        page = self.fb.load_fritzbox_page('/data.lua', 'lang=de&no_sidrenew=&page=wSet')

        json_structure = json.loads(page.decode('UTF-8'))

        json_structure_devices = json_structure['data']['net']['devices']

        for i in range(len(json_structure_devices)):
            name = json_structure_devices[i]['name']
            on_ts = self.chk_ts

            self.device_list[name] = {'on_ts' : on_ts}

        return self.device_list, self.chk_ts


#===============================================================================
# Main program
#===============================================================================
def main():
    """Main function for testing purpose"""
    fb_p = FBPresence(ip=args.ip, password=args.password)

    if args.name == None:
        devices, chk_ts = fb_p.get_wlan_device_information()

        print(devices)

    elif args.name != None:
        print(fb_p.is_device_present(device_name=args.name))


if __name__ == '__main__':
    main()
