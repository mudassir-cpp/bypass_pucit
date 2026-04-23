from ColorDTO import Color as cl
def showHelpPage():
    print("Will print help page")


def httpFailure(whatNotFound:str):
    print(cl.RED+f"{whatNotFound} SHELL is NOT SUPPORTED so can't set http|https proxy ")
    print("All tools depending on http|https methods wouldn't access internet i.e pub.dev")
    print(cl.RESET)


def showError(errStr:str):
    print(cl.RED+errStr+cl.RESET)
    print(cl.RESET)


def showHowToContributeInTool():
    print("iSTRHA contribute krna haii")