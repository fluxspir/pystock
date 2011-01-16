#!/usr/bin/python3.1
#
# pystock.py
#
# (c) Franck LABADILLE  ; franck {att} kernlog [dot] net
# IRC : Franck @ irc.oftc.net
#       
# Version 0.1  ; 2011-01-16 
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS 0AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
# use to get data about stock market, analyse, make your own portfolio
#
#
###############################################################################
###############################################################################
###########                            CHANGELOG                     ##########
###############################################################################
###############################################################################
#
##############
## Changelog 0.1
##############
#
#
#
###############################################################################
###############################################################################
############                             TODO                        ##########
###############################################################################
###############################################################################
#
#
#
#
#
#
#                                    ~~~~~~~~~
#                                    ~ FIXED ~
#                                    ~~~~~~~~~
#
###############################################################################
###############################################################################
###########                   BEGINNING  OF  pystock.sh             ##########
###############################################################################
###############################################################################

###############################################################################
###############################################################################
###############################################################################
#####                                                                      ####
#####     DO NOT EDIT AFTER THIS LINE UNLESS YOU KNOW WHAT YOU'RE DOING    ####
#####                                                                      ####
###############################################################################
###############################################################################
###############################################################################
__author__ = "Franck LABADILLE (franck@kernlog.net)"
__version__ = "$Revision 0.1 $"
__date__ = "$Date: 2011/01/17 $"
__copyright__ = "Copyright (c) 2011 Franck LABADILLE"
__licence__ = "BSD"

###############
### IMPORT
###############

import os
import shutil
import sys
import fConfig
from optparse import OptionParser

###############
## VARIABLE (- CONSTANT)
###############

progname = "pystock"
version = "0.1"
previous_version = "None"
dateVersion = "2011-01-16"

default_conf = {
"stocks": {"GOOG": "biarritz",}
}

################
## functions
################

def debug(source, debug_message):
    """This function displays on stdout messages.
    "source" is the variable that tells which parts
    of programm want to tell us something.
    Messages displayed tells where in the prog 
    we are right now, some variables state...
    """
    debug_message = debug_message.strip()
    if options.verbose is not None:
        verbose = options.verbose.split(",")
        source = source.split(",")
        
        def test_source():
            """ test message source if need"""
            for src in source:
                if src == key:
                    print(debug_message)
#                if src == "battery":
#                    battery.set_debug(True)
        for key in verbose:
            if key == "all":
                print(debug_message)
#                fConfig.set_debug(True)
#                battery.set_debug(True)
#                sound.set_debug(True)

            else:
                test_source()


def quit_prog(message):
    """Function to exit properly the program

    We have to remove all temporary files/dir
    Exit the program
    """

    bugsource = "main"
    debug(bugsource,"Entering quitting function")
    print(message)
    ## Remove temporary
    debug(bugsource, "Removing temporary directory %s" % conf.tmpdir)
    shutil.rmtree(conf.tmpdir)
    ## Exit the program
    debug(bugsource, "Exiting")
    sys.exit(0)

###########
## OptParse
###########

parser = OptionParser(usage="%prog [-c] [-t]", version="%prog version " + \
                    version + " ; released the " + dateVersion + ".\n")
parser.add_option("-c", "--config",
                    action="store", type="string", dest="userconf",
                    help="PATH to alternative pystock config file")

parser.add_option("-s", "--stocks",
                    action="store", type="string", dest="stocks",
                    help="stocks codes, separated by comma ; \
                    e.g. : google will be : GOOG")

parser.add_option("--debug", type="string",
                    action="store", dest="verbose",
                    help="Verbose mode . Possible values, comma separated, at \
                    least one : \n\
                    [main][,conf][,fetch] | [all]")

(options,args) = parser.parse_args()

##################
## main
##################

if __name__ == "__main__" :
    try:
        debug("main", "Debug : Starting program")
        debug("conf", "Debug : Instanciation de la classe conf")
        conf = fConfig.Config(default_conf, options.userconf, progname, \
                previous_version)
        conf.load_config_file()
        conf.load_parser(options.__dict__)
        debug("main", "Debug : Instanciation de la classe fetch")

    except KeyboardInterrupt:
       quit_prog("Keyboard interrupt : quitting")

       
debug("main", "Debug : Quitting program")
quit_prog("thank you for using pystock ; have a nice day :)")
