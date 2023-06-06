from pyaccsharedmemory import accSharedMemory

asm = accSharedMemory()
sm = asm.read_shared_memory()

if (sm is not None):
    print(f"CAR :{sm.Static.car_model}")

    print(f"TRACK:{sm.Static.track}")
    print(sm.Graphics.last_time)

asm.close()

