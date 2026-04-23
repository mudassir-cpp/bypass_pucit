import platform
import  subprocess
import  logging
from typing import List
import  os
import  presentation as pr

from samba.dcerpc.dcerpc import response

from ColorDTO import  Color as cl


def setForLinux():
    # set for http and https
    # 1  update bashrc or zshrc file
    SHELL:str=getEnvVar("SHELL")
    print(cl.RED+SHELL+cl.RESET)
    if SHELL=="NONE":
        pr.showError("NO SHELL configured or is'nt at default location")
        return
    SHELL=SHELL.split('/')[-1]

    if SHELL=='zsh':
        # get zsh file

    pass

def runSubProcessWithStream(ls:List[str]):
    process=subprocess.Popen(
        ls,
        stdout=subprocess.PIPE, # stream the output to PIPE like |
        text=True # decode the bytes and Txt
    )
    print(str(process.stdout))
    response:str =""
    for ln in process.stdout:
        response += ln+'\n'
        print(ln.strip()) # print the output stream
    return response

def getEnvVar(var:str)->str:
    res=os.environ.get("SHELL")
    if res is None:
        return "NONE"
    return res