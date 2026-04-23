import platform
import  subprocess
from typing import List
import  os
import  presentation as pr
import  dataDTO

from ColorDTO import  Color as cl


def setForLinux():
    setHttpLinux()

    pass



# unset all proxies
def unsetAllProxiesForLinux():
    unsetHttpLinux()

def runSubProcessWithStream(ls:List[str],shouldPrint:bool=True)->str:
    process=subprocess.Popen(
        ls,
        stdout=subprocess.PIPE, # stream the output to PIPE like |
        text=True # decode the bytes and Txt
    )
    res:str =""
    for ln in process.stdout:
        res += ln
        if shouldPrint:
            print(ln.strip) # print the output stream
    return res

def getEnvVar(var:str)->str:
    res=os.environ.get("SHELL")
    if res is None:
        return "NONE"
    return res




def setHttpLinux():
    SHELL: str = getEnvVar("SHELL")
    print(cl.RED + SHELL + cl.RESET)
    if SHELL == "NONE":
        pr.showError("NO SHELL configured or is'nt at default location")
        return
    SHELL = SHELL.split('/')[-1]
    cmd: str = ""
    path: str = ""
    if SHELL == 'zsh':
        # get zsh file
        path = os.path.expanduser("~/.zshrc")
    elif SHELL == 'bash':
        path = os.path.expanduser("~/.bashrc")

    # we gotta the path of shell config file
    res = runSubProcessWithStream(["cat", path], False)  # get it content
    allLines = res.split('\n')
    toPut = []
    # if user is setting and its is already sett then filter to avoid redundancy

    for line in allLines:
        if "http_proxy" in line or "https_proxy" in line:
            continue
        toPut.append(line)
    allLines = toPut

    httpProxy = f"http_proxy={dataDTO.PROXY}"
    httpsProxy = f"https_proxy={dataDTO.PROXY}"
    allLines.append(httpProxy)
    allLines.append(httpsProxy)
    toUpateFile = "\n".join(allLines)
    # up =added proxy
    pr.showError(toUpateFile)




# jst filter out http related things bro
def unsetHttpLinux():
    SHELL: str = getEnvVar("SHELL")
    print(cl.RED + SHELL + cl.RESET)
    if SHELL == "NONE":
        pr.showError("NO SHELL configured or is'nt at default location")
        return
    SHELL = SHELL.split('/')[-1]
    cmd: str = ""
    path: str = ""
    if SHELL == 'zsh':
        # get zsh file
        path = os.path.expanduser("~/.zshrc")
    elif SHELL == 'bash':
        path = os.path.expanduser("~/.bashrc")

    # we gotta the path of shell config file
    res = runSubProcessWithStream(["cat", path], False)  # get it content
    allLines = res.split('\n')
    toPut = []
    # if user is setting and its is already sett then filter to avoid redundancy

    for line in allLines:
        if "http_proxy" in line or "https_proxy" in line:
            continue
        toPut.append(line)
    allLines = toPut
    toUpateFile = "\n".join(allLines)
    # up =added proxy
    pr.showError(toUpateFile)
