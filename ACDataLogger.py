import sys
import ac
import acsys
from pyaccsharedmemory import accSharedMemory
asm = accSharedMemory()
sm = asm.read_shared_memory()

def acMain(ac_version):
    appWindow = ac.newApp("ACDataLogger")
    ac.setSize(appWindow, 400,200)

    label_1 = ac.addLabel(appWindow,sm.Static.player_name)
    ac.setPosition(label_1,30,100)
    ac.console("App Now Running")

    return "ACDataLogger"
