# -*- coding: utf-8 -*-
"""Short description.

This test module will test the functionality of the module FBPresence
"""
from openpyxl.worksheet import page

__author__     = "Dennis Jung"
__copyright__  = "Copyright 2019, Dennis Jung"
__credits__    = ["Dennis Jung"]
__license__    = "GPL Version 3"
__maintainer__ = "Dennis Jung"
__email__      = "Dennis.Jung@it-jung.com"


#===============================================================================
# Additional information
#===============================================================================


#===============================================================================
# System imports
#===============================================================================
import sys
import os
import json
import pytest

from unittest import mock, TestCase
from unittest.mock import patch, Mock


#===============================================================================
# Include parent folders
#===============================================================================
dir_up = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(dir_up,'..'))


#===============================================================================
# User imports
#===============================================================================
from FBPresence import FBPresence, InvalidParameterError


#===============================================================================
# Constant declarations
#===============================================================================
IP                = '192.168.0.1'
PASSWORD          = 'abc'
TIMESTAMP_NOW     = 123


#===============================================================================
# Test class definitions
#===============================================================================
class test_CLASS(TestCase):
    """Test class that contains all test cases"""
    @patch('FBPresence.FBCore.FritzBox', autospec=True)
    def setUp(self, fritzbox_mock):
        self.fbP = FBPresence(ip=IP, password=PASSWORD)
        fritzbox_mock.assert_called_once_with(IP, PASSWORD)


    def tearDown(self):
        pass


    def test_init(self):
        assert self.fbP.device_list == {}


    @patch('FBPresence.json.loads', autospec=True)
    @patch('FBPresence.time.time', autospec=True)
    def test_get_wlan_device_information(self, time_mock, json_mock):
        time_mock.return_value = TIMESTAMP_NOW
        self.fbP.get_wlan_device_information()
        assert json_mock.call_count == 1
        assert self.fbP.device_list == {}


    @patch('FBPresence.FBPresence.get_wlan_device_information', autospec=True)
    def test_is_device_present(self, fbpresence_mock):
        debounce_time = 1

        fbpresence_mock.return_value = {'PresentDevice' : {'on_ts' : 60*debounce_time*10},
                                        'DebounceAbsentDevice' : {'on_ts' : 60*debounce_time*10-30},
                                        'AbsentDevice' : {'on_ts' : 0}}, 60*debounce_time*10

        assert self.fbP.is_device_present(device_name='UnknownDevice', debounce_off=debounce_time) == False

        assert self.fbP.is_device_present(device_name='PresentDevice', debounce_off=debounce_time) == True
        assert self.fbP.is_device_present(device_name='DebounceAbsentDevice', debounce_off=debounce_time) == True

        assert self.fbP.is_device_present(device_name='AbsentDevice', debounce_off=debounce_time) == False

        with pytest.raises(InvalidParameterError):
            self.fbP.is_device_present(debounce_off=1) == False


#===============================================================================
# Start of program
#===============================================================================
if __name__ == '__main__':
    unittest.main()
