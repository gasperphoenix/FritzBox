#!/bin/bash

#Short description...

#This module is used to execute the unit tests for this project

#__author__     = "Dennis Jung"
#__copyright__  = "Copyright 2019, Dennis Jung"
#__credits__    = ["Dennis Jung"]
#__license__    = "GPL Version 3"
#__maintainer__ = "Dennis Jung"
#__email__      = "Dennis.Jung@it-jung.com"


#===============================================================================
# Constant declaration
#===============================================================================
# SHELL_COLORS
FORMAT_RED_NORMAL="\033[31;1m"
FORMAT_BLUE_NORMAL="\033[34;1m"
FORMAT_YELLOW_NORMAL="\033[33;1m"
FORMAT_GREEN_NORMAL="\033[32;1m"

FORMAT_DEFAULT="\033[0m"


#===============================================================================
# Determine system type
#===============================================================================
unameOut="$(uname -s)"

case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac


#===============================================================================
# Adapt system commands to machine type
#===============================================================================
case "${unameOut}" in
    Linux*)     ESCAPED_ECHO=$(echo -e);;
    Mac*)       ESCAPED_ECHO=$(echo);;
esac


#===============================================================================
# Function definitions
#===============================================================================
# This functions writes a log message on the shell using
# the following parameters
#
# log_message (color, tag, message)
#     color:   Color from the list SHELL_COLORS
#     tag:     Will be written in braces in front of the log message; 
#              provided in quotes
#     message: Message to be written on the shell; provided in quotes
log_message () {
	color=$1
	tag=$2
	message=$3
	
	echo $ESCAPED_ECHO "[$color$tag$FORMAT_DEFAULT] $message"
}
	

#===============================================================================
# Start of script
#===============================================================================
# Clear the shell screen
clear

# Write initial log message
log_message $FORMAT_YELLOW_NORMAL "info" "Start execution of: $0"

log_message $FORMAT_GREEN_NORMAL "info" "Start unit tests"

py.test -v --cov-report term-missing --cov FBPresence 

log_message $FORMAT_GREEN_NORMAL "info" "Finalize unit tests"
