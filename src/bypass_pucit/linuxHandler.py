import platform
import  subprocess
from typing import List
import  os
import  presentation as pr
import  dataDTO

from ColorDTO import  Color as cl


def setForLinux():
    setHttpLinux()




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
    # else:

       # exit()
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
    # in all sessions it will run first
    httpProxy = f'export http_proxy="{dataDTO.PROXY}"'
    httpsProxy = f'export https_proxy="{dataDTO.PROXY}"\n'
    allLines.append(httpProxy)
    allLines.append(httpsProxy)
    toUpateFile = "\n".join(allLines)
    # up =added proxy

    # tee the toUpdate File using sub proccess
    subprocess.run(
        ['tee',path],
        input=toUpateFile.encode(),
        check=True,
    )
    #GPT: can't source current SHELL session using python
    # so make a new SHELL prcess source it there and replace currnet shell session with new one
    subprocess.run(["zsh", "-c", "source ~/.zshrc && exec zsh"])





# jst filter out http related things bro
def unsetHttpLinux():
    pr.showError("here to remove")
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
    # up =filtered out proxy
    subprocess.run(
        ['tee', path],
        input=toUpateFile.encode(),
        check=True,
    )

    # GPT: can't source current SHELL session using python
    # so make a new SHELL prcess source it there and replace currnet shell session with new one
    subprocess.run(["zsh", "-c", "source ~/.zshrc && exec zsh"])


