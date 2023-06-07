from pyaccsharedmemory import accSharedMemory
from appJar import gui

asm = accSharedMemory()
sm = asm.read_shared_memory()

if (sm is not None):
    print(f"CAR :{sm.Static.car_model}")

    print(f"TRACK:{sm.Static.track}")
    print(sm.Graphics.last_time)
    
    carmodel = sm.Static.car_model
asm.close()

app = gui("sharedmemorymanager",useTtk=True)
app.addLabel("CAR MODEL",carmodel)

