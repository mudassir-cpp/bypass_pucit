import platform
import  subprocess

import linuxHandler as lh, windowHandler as wh
import ColorDTO


def setProxyGlobally():
    # setup the whole environment
    # setup http and https proxy

    if platform.system()=="Linux":
        # check whether it is running bash or ZSH
        lh.setForLinux()
    elif platform.system()=="Windows":
        wh.setForWindow()
    else:
        print(ColorDTO.Color.RED+"OPERATING SYSTEM NOT SUPPORTED")







def rollBackItBro():
    if platform.system()=="Linux":
        pass





