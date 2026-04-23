import platform
import  subprocess
from typing import List
import  os
import  presentation as pr
import  dataDTO

from ColorDTO import  Color as cl
from ColorDTO import Color

def setForLinux():
    print(Color.GREEN + "Applying HTTP & HTTPs Proxies system-wide." + Color.RESET)
    setHttpLinux()

    # now set for git

    # set pip

    #set for NPM

    # SET for snap

    #set for dnf


    print(Color.BLUE + "Changes applied successfully. Close this terminal and start a new one to take effect." + Color.RESET)




# unset all proxies
def unsetAllProxiesForLinux():
    # Unset HTTP configs
    print(Color.GREEN + "Applying HTTP & HTTPs Proxies system-wide." + Color.RESET)
    unsetHttpLinux()
    print(Color.BLUE + "Changes applied successfully. Close this terminal and start a new one to take effect." + Color.RESET)

    # git


    # pip


    # npm




def runSubProcessWithStream(ls: List[str], shouldPrint: bool = True) -> str:
    process = subprocess.Popen(
        ls,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    res = ""

    for line in process.stdout:
        res += line
        if shouldPrint:
            print(line.strip())

    # process.stdout.

    # wait for process to fully finish
    process.wait()

    return res

def getEnvVar(var:str)->str:
    res=os.environ.get("SHELL")
    if res is None:
        return "NONE"
    return res


def setHttpLinux():

    SHELL: str = getEnvVar("SHELL")
    # print(cl.RED + SHELL + cl.RESET)
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
    p=subprocess.run(
        ['tee',path],
        input=toUpateFile.encode(),
        check=True,
        stdout=subprocess.DEVNULL,
    )

    #GPT: can't source current SHELL session using python
    # so make a new SHELL prcess source it there and replace currnet shell session with new one
    subprocess.run(
        ["zsh", "-c", "source ~/.zshrc && exec zsh"],
        stdin=subprocess.DEVNULL,
    )

def setGitLinux():
    #TODO

    pass


def setPipLinux():
    #TODO


    pass

def setNpmLinux():
    #TODO
    pass


# jst filter out http related things bro
def unsetHttpLinux():
    SHELL: str = getEnvVar("SHELL")
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
        stdout=subprocess.DEVNULL
    )

    # GPT: can't source current SHELL session using python
    # # so make a new SHELL prcess source it there and replace currnet shell session with new one
    if SHELL == "zsh":
        subprocess.run(["zsh", "-c", "source ~/.zshrc && exec zsh"],
                       stdin=subprocess.DEVNULL,)
    else:
        subprocess.run(["bash", "-c", "source ~/.bashrc && exec bash"],
                       stdout=subprocess.DEVNULL,)

    # for current session jst unset is enough
    os.environ.pop("http_proxy",None)
    os.environ.pop("https_proxy",None)


def unsetGitLinux():
    #TODO
    pass


def unsetPipLinux():
    #TODO
    pass

def unsetNpmLinux():
    #TODO
    pass

