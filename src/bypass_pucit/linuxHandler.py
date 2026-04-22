import platform
import  subprocess
import  logging
from typing import List
def setForLinux():

    pass


def runSubProcessWithStream(ls:List[str]):
    process=subprocess.Popen(
        ls,
        stdout=subprocess.PIPE, # stream the output to PIPE like |
        text=True # decode the bytes and Txt
    )
    for ln in process.stdout:
        print(ln.strip()) # print the output stream

    return process.returncode