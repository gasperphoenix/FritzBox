# -*- coding: utf-8 -*-
"""Short description.

This test module ...
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
LUA_URL           = '/data.lua'
LUA_URL_PARAMETER = 'lang=de&no_sidrenew=&page=wSet'


#===============================================================================
# Test class definitions
#===============================================================================
class test_CLASS(TestCase):
    @patch('FBPresence.FBCore.FritzBox', autospec=True)
    def setUp(self, FritzBox_mock):
        self.fbP = FBPresence(ip=IP, password=PASSWORD)
        FritzBox_mock.assert_called_once_with(IP, PASSWORD)
    
    
    def tearDown(self):
        pass
    
        
    def test_init(self):    
        assert self.fbP.deviceList == {}
    

    @patch('FBPresence.json.loads', autospec=True)
    @patch('FBPresence.time.time', autospec=True)
    def test_getWLANDeviceInformation(self, time_mock, json_mock):
        time_mock.return_value = TIMESTAMP_NOW
        self.fbP.getWLANDeviceInformation()
        assert json_mock.call_count == 1
        assert self.fbP.deviceList == {}

        
    @patch('FBPresence.FBPresence.getWLANDeviceInformation', autospec=True)    
    def test_isDevicePresent(self, FBPresence_mock):
        debounceTime = 1
        
        FBPresence_mock.return_value = {'PresentDevice' : {'on_ts' : 60*debounceTime*10},
                                        'DebounceAbsentDevice' : {'on_ts' : 60*debounceTime*10-30},
                                        'AbsentDevice' : {'on_ts' : 0}}, 60*debounceTime*10
        
        assert self.fbP.isDevicePresent(deviceName='UnknownDevice', debounceOff=debounceTime) == False
        
        assert self.fbP.isDevicePresent(deviceName='PresentDevice', debounceOff=debounceTime) == True
        assert self.fbP.isDevicePresent(deviceName='DebounceAbsentDevice', debounceOff=debounceTime) == True
        
        assert self.fbP.isDevicePresent(deviceName='AbsentDevice', debounceOff=debounceTime) == False
        
        with pytest.raises(InvalidParameterError):
            self.fbP.isDevicePresent(debounceOff=1) == False
    
    
#===============================================================================
# Start of program
#===============================================================================
if __name__ == '__main__':
    unittest.main()