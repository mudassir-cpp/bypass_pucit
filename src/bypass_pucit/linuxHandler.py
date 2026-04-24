import platform
import  subprocess
from typing import List
import  os
import  presentation as pr
import  dataDTO
from pathlib import  Path

from ColorDTO import  Color as cl
from ColorDTO import Color

def setForLinux():
    print(Color.GREEN + "Applying HTTP & HTTPs Proxies system-wide." + Color.RESET)
    setHttpLinux()

    # now set for git
    # cmd = git config --global https.proxy http://172.16.0.6:8080
    print(Color.GREEN + "Applying git config system-wide." + Color.RESET)
    setGitLinux()


    # set pip
    print(Color.GREEN + "Applying pip configs system-wide." + Color.RESET)

    setPipLinux()

    #set for NPM
    setNpmLinux()


    #APT
    setAptLinux()

    #docker
    setDockerLinux()

    #yarn


    #wget


    #maven

    #gradle

    #snap


    #ssh

    #pnpm

    print(Color.BLUE + "Changes applied successfully. Close this terminal and start a new one to take effect." + Color.RESET)




# unset all proxies
def unsetAllProxiesForLinux():
    # Unset HTTP configs
    print(Color.GREEN + "unsetting HTTP & HTTPs Proxies system-wide." + Color.RESET)
    unsetHttpLinux()

    # git
    #  git config --global --unset https.proxy
    print(Color.GREEN + "unsetting git Proxies system-wide." + Color.RESET)
    unsetGitLinux()

    # pip
    print(Color.GREEN + "unsetting Pip Proxies system-wide." + Color.RESET)
    unsetPipLinux()

    # npm
    print(Color.GREEN + "unsetting Pip Proxies system-wide." + Color.RESET)
    unsetNpmLinux()

    # APT
    print(Color.GREEN + "unsetting APT Proxies system-wide." + Color.RESET)
    unsetAptLinux()



    print(Color.BLUE + "Changes applied successfully. Close this terminal and start a new one to take effect." + Color.RESET)


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
    allProxy = f'export all_proxy="{dataDTO.PROXY}"\n'
    noProxy="export no_proxy=localhost,127.0.0.1,::1"

    # export no_proxy=localhost,127.0.0.1
    allLines.append(httpProxy)
    allLines.append(httpsProxy)
    allLines.append(allProxy)
    allLines.append(noProxy)
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
    p = subprocess.run(
        ["git", "config" ,"--global","https.proxy", dataDTO.PROXY],
        stdout=subprocess.DEVNULL,
        check=True,
    )
    return p.returncode


def setPipLinux():
    # cat ~/.config/pip/pip.conf                                                                                                                              ✔
    # [global]
    # proxy = http://172.16.0.6:8080
    # jst make that file and set proxy there in file is all we need to implemnt in the following code

    # if not already folder is made
    # as may not allow python to create file in that path so using bash/zsh commands

    try:
        # using python Path lib to create Folder
        pip_dir=Path.home()/".config"/"pip"
        pip_dir.mkdir(parents=True, exist_ok=True) # parents true=make parent directories if not exist
        # exists ok say do nothingg jst ok haii
        # then make file
        pip_conf_file=pip_dir/"pip.conf"
        # open the file overwrite it & save simply
        dataToPutForPipConfig=f"[global]\nproxy = {dataDTO.PROXY}\n"
        pip_conf_file.write_text(dataToPutForPipConfig)
    except:
        print(Color.GREEN+"Seems pip Folder already exist..."+Color.RESET)



def setNpmLinux():
    subprocess.run(
        ["npm","config","set","proxy",dataDTO.PROXY],
        stdout=subprocess.DEVNULL,
        check=True
    )
    subprocess.run(
        ["npm", "config", "set", "https-proxy", dataDTO.PROXY],
        stdout=subprocess.DEVNULL,
        check=True
    )


def setAptLinux():
    path = Path("/etc/apt/apt.conf.d/95proxies")
    content = f'''
    Acquire::http::Proxy "{dataDTO.PROXY}";
    Acquire::https::Proxy "{dataDTO.PROXY}";
    '''
    path.write_text(content)


def setDockerLinux():
    #TODO
    pass



     #yarn
def setYarnLinux():
    #TODO
    pass


    #wget
def setWgetLinux():
    #TODO

    pass


    #maven
def setMavenLinux():
    #TODO

    pass


    #gradle
def setGradleLinux():
    #TODO
    pass

    #snap
def setSnapLinux():
    #TODO
    pass

    #ssh

def setSshLinux():
    #TODO
    pass


    #pnpm
def setPnpmLinux():
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
        if "http_proxy" in line or "https_proxy" in line or len(line.strip())==0 or "all_proxy" in line or "no_proxy" in line:
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
    p = subprocess.run(
        ["git", "config", "--global", "--unset" ,"https.proxy"],
        stdout=subprocess.DEVNULL,
    )
    p = subprocess.run(
        ["git", "config", "--global", "--unset", "http.proxy"],
        stdout=subprocess.DEVNULL,
    )
    return p.returncode

def unsetPipLinux():
    # cat ~/.config/pip/pip.conf                                                                                                                              ✔
    # [global]
    # proxy = http://172.16.0.6:8080
    # jst make that file and set proxy there in file is all we need to implemnt in the following code

    # if not already folder is made
    # as may not allow python to create file in that path so using bash/zsh commands

    try:
        # using python Path lib to create Folder
        pip_dir = Path.home() / ".config" / "pip"
        pip_dir.mkdir(parents=True, exist_ok=True)  # parents true=make parent directories if not exist
        # exists ok say do nothingg jst ok haii
        # then make file
        pip_conf_file = pip_dir / "pip.conf"
        # open the file overwrite it & save simply
        blankPage = ""
        pip_conf_file.write_text(blankPage)
    except:
        print(Color.GREEN + "Seems pip Folder already exist..." + Color.RESET)


def unsetNpmLinux():
    subprocess.run(
        ["npm", "config", "delete", "proxy"],
        stdout=subprocess.DEVNULL,
        check=True
    )
    subprocess.run(
        ["npm", "config", "delete", "https-proxy"],
        stdout=subprocess.DEVNULL,
        check=True
    )


def unsetAptLinux():
    path = Path("/etc/apt/apt.conf.d/95proxies")
    # apt will not find place where to proxies live soo you knowwee
    if path.exists():
        path.unlink()


def unsetDockerLinux():
    # TODO
    pass

    # yarn


def unsetYarnLinux():
    # TODO
    pass

    # wget


def unsetWgetLinux():
    # TODO

    pass

    # maven


def unsetMavenLinux():
    # TODO

    pass

    # gradle


def unsetGradleLinux():
    # TODO
    pass

    # snap


def unsetSnapLinux():
    # TODO
    pass

    # ssh


def unsetSshLinux():
    # TODO
    pass

    # pnpm


def unsetPnpmLinux():
    # TODO
    pass



