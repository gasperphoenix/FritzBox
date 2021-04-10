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


#===============================================================================
# Evaluate parameters
#===============================================================================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage="%(prog)s [options]",
                                     description="In case no option is selected the script will "
                                     "connect to the FritzBox and return it's name")

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
USER_AGENT = "Mozilla/5.0 (U; Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0"


#===============================================================================
# Exceptions
#===============================================================================
class InvalidParameterError(Exception):
    """Parameter error class"""
    pass


#===============================================================================
# Class definitions
#===============================================================================
class FritzBox(object):
    """Interface for communication with a FritzBox.

    This class provides an interface for communication with a FritzBox using LUA pages.
    """

    def __init__(self, ip, password):
        self.ip = ip
        self.password = password
        self.sid = ''


    def __del__(self):
        pass


    def load_fritzbox_page(self, url, param):
        """Method to read out a page from the FritzBox.

        The method reads out the given page from the FritzBox. It automatically includes a session id
        between url and param.

        Args:
            url (str):   URL of the page that shall be read out from the FritzBox.
            param (str): Additional parameters that shall be added to the URL.

        Returns:
            Requested page as string, None otherwise.
        """

        if self.login():
            page_url = 'http://' + self.ip + ':80' + url + '?sid=' + self.sid.decode('utf-8') + param

            logger.debug("Load the FritzBox page: " + page_url)

            headers = { "Accept" : "application/xml",
                        "Content-Type" : "text/plain",
                        "User-Agent" : USER_AGENT}

            request = urllib.request.Request(page_url, headers = headers)

            try:
                response = urllib.request.urlopen(request)
            except:
                logger.error("Loading of the FritzBox page failed: %s" %(page_url))

                return None

            page = response.read()

            if response.status != 200:
                logger.error("Unexpected feedback from FritzBox received: %s %s" % (response.status, response.reason))

                return None
            else:
                return page
        else:
            return None


    def login(self):
        """Authenticate with the FritzBox to access private pages.

        The method authenticates with a FritzBox using the authentication credentials
        read out from the configuration file during the class object instantiation.

        Args:
            Does not require any arguments.

        Returns:
            Does not return any value.
        """

        logger.debug("Login to the FritzBox")

        headers = { "Accept" : "application/xml",
                    "Content-Type" : "text/plain",
                    "User-Agent" : USER_AGENT}

        page_url = 'http://' + self.ip + ':80/login_sid.lua'

        request = urllib.request.Request (page_url, headers = headers)

        try:
            response = urllib.request.urlopen(request)
        except:
            logger.error("Loading of the FritzBox page failed: %s" %(page_url))

            return False

        page = response.read()

        if response.status != 200:
            logger.error("Unexpected feedback from FritzBox received: %s %s" % (response.status, response.reason))

            return False
        else:
            page_xml = minidom.parseString(page)

            sid_info = page_xml.getElementsByTagName('SID')

            sid = sid_info[0].firstChild.data

            if sid == "0000000000000000":
                challenge_info = page_xml.getElementsByTagName('Challenge')

                challenge = challenge_info[0].firstChild.data

                challenge_bf = (challenge + '-' + self.password).encode( 'utf-16le' )

                m = hashlib.md5()

                m.update(challenge_bf)

                response_bf = challenge + '-' + m.hexdigest().lower()

            else:
                logger.debug("Authentication succeeded")

                self.sid = sid

                return True

        headers = { "Accept" : "text/html,application/xhtml+xml,application/xml",
                    "Content-Type" : "application/x-www-form-urlencoded",
                    "User-Agent" : USER_AGENT}

        page_url = 'http://' + self.ip + ':80/login_sid.lua?&response=' + response_bf

        request = urllib.request.Request(page_url, headers = headers)

        response = urllib.request.urlopen(request)

        page = response.read()

        if response.status != 200:
            logger.error("Unexpected feedback from FritzBox received: %s %s" % (response.status, response.reason))

            return False
        else:
            sid = re.search(b'<SID>(.*?)</SID>', page).group(1)

            if sid == "0000000000000000":
                logger.error("Authentication failed due to invalid password")

                return False
            else:
                logger.debug("Authentication succeeded")

                self.sid = sid

                return True


#===============================================================================
# Main program
#===============================================================================
def main():
    """Main function for testing purpose"""
    fb = FritzBox(ip=args.ip, password=args.password)


if __name__ == '__main__':
    main()
