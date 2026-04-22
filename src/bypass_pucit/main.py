import platform
import os
import sys
import logging
import presentation as pr
import ColorDTO as cl
import  handler
import subprocess
import   linuxHandler

def main():
    pass
PROXY="http://172.16.0.6:8080" # as sys wide 

args=sys.argv[1:]
if len(args)==0 or args[0]=="--help":
    pr.showHelpPage()
elif args[0]=="set":
    handler.setProxyGlobally()
elif args[0]=="unset":
    handler.rollBackItBro()
else:
    print(cl.Color.RED+"No Such Command: plz Respect Parameters",cl.Color.RESET)
    print(cl.Color.YELLOW+"type "+cl.Color.GREEN,"bypass_pucit --help"+cl.Color.YELLOW+ " to get Following Guide ",cl.Color.RESET)
    pr.showHelpPage()








