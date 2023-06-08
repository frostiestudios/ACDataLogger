from pyaccsharedmemory import accSharedMemory
from appJar import gui
def format_time(time):
    minutes = int(time / 60)
    seconds = int(time % 60)
    mseconds = int((time % 1) * 100)
    return
def format_speed(speed):
    return f"{int(speed)}"
def update_labels():
    global car_model, track, last_time, best_time, driver, speed, gear, rpm, current_time

    asm = accSharedMemory()
    sm = asm.read_shared_memory()

    if sm is not None:
        car_model = sm.Static.car_model
        track = sm.Static.track
        last_time = format_time(sm.Graphics.last_time)
        best_time = format_time(sm.Graphics.best_time)
        current_time =format_time(sm.Graphics.current_time)
        driver = sm.Static.player_nick
        speed = format_speed(sm.Physics.speed_kmh)
        gear = sm.Physics.gear
        max_rpm = sm.Static.max_rpm
        min_rpm = 0
        rpm = sm.Physics.rpm
        
        asm.close()

    app.setLabel("car_model", f"Car Model: {car_model}")
    app.setLabel("track", f"Track: {track}")
    app.setLabel("last_time", f"Last Time: {last_time}")
    app.setLabel("best_time", f"Best Time: {best_time}")
    app.setLabel("current_time",f'current_time:{current_time}')
    app.setLabel("car_count", f"Car Count: {driver}")
    app.setLabel("speed",f"{speed} KPH")
    app.setLabel("gear",gear)
    app.setMeter("tach",rpm,rpm)
    app.after(1000, update_labels)

car_model = ""
track = ""
last_time = ""
best_time = ""
current_time = ""
driver = ""
speed = ""
gear = ""
rpm = ""
app = gui("sharedmemorymanager",useTtk=True)
app.addLabel("SharedMemoryManager")

app.startLabelFrame("Basic Info",0,0)
app.addLabel("car_model", f"Car Model: {car_model}")
app.addLabel("track", f"Track: {track}")
app.addLabel("car_count", f"Car Count: {driver}")
app.stopLabelFrame()

app.startLabelFrame("Time",1,0)
app.addLabel("last_time", f"Last Time: {last_time}")
app.addLabel("best_time", f"Best Time: {best_time}")
app.addLabel("current_time", f"Current Time: {current_time}")
app.stopLabelFrame()

app.startLabelFrame("Speed",0,1)
app.addLabel("speed",speed)
app.setLabelFont("speed",size=20)
app.stopLabelFrame()


app.startLabelFrame("Gear",1,1)
app.addLabel("gear",gear)
app.addMeter("tach")
app.stopLabelFrame()


app.after(0, update_labels)
app.go()