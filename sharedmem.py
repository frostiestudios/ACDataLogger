from pyaccsharedmemory import accSharedMemory
from appJar import gui
import sqlite3
import os

current_directory = os.getcwd()
print(current_directory)
script_directory = os.path.dirname(os.path.abspath(__file__))
db_file_path = os.path.join(script_directory, 'sharedmemmanager.db')
conn = sqlite3.connect(db_file_path)
conn.close()


def format_time(time):
    minutes = int(time // 60000)
    seconds = int((time // 1000) % 60)
    milliseconds = int(time % 1000)
    print(seconds)
    print(milliseconds)
    return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
def format_speed(speed):
    return f"{int(speed)}"
def format_text(data):
    if isinstance(data, bytes):
        return str(data, 'utf-8').rstrip('\x00')
    return str(data).rstrip('\x00')

def store_data(car_model, track, last_lap_time,driver):
    conn = sqlite3.connect(db_file_path)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS laps (lap_time TEXT, track TEXT, car_model TEXT)")
    c.execute("INSERT INTO laps (lap_time, track, car_model, driver) VALUES (?, ?, ?, ?)",(format_text(last_lap_time), format_text(track), format_text(car_model), format_text(driver)))
    conn.commit()
    conn.close()

def update_labels():
    global car_model
    global track
    global last_time
    global best_time, driver, speed, gear, rpm, current_time, distance, laps
    global car_cords

    asm = accSharedMemory()
    sm = asm.read_shared_memory()

    if sm is not None:
        car_cords=sm.Graphics.car_coordinates
        print(car_cords)
        car_model = sm.Static.car_model
        track = sm.Static.track
        print(car_model)
        #LAPS / RANGE
        new_laps = sm.Graphics.completed_lap   
        if new_laps != laps:
            last_lap_time = format_time(sm.Graphics.last_time)
            store_data(car_model,track,last_lap_time, driver)
        laps = new_laps     
        distance = sm.Graphics.distance_traveled
        valid_lap = sm.Graphics.is_valid_lap
        print(valid_lap)
        print(distance)
        #TIME
        last_time = format_time(sm.Graphics.last_time)
        best_time = format_time(sm.Graphics.best_time)
        current_time = format_time(sm.Graphics.current_time)
        delta_time = sm.Graphics.delta_lap_time
        delta_positive = sm.Graphics.is_delta_positive
        if delta_positive == False:
            delta_sign = "-"
            app.setLabelBg("delta_time","red")
        else:
            delta_sign = "+"
            app.setLabelBg("delta_time","green")
        
        print(delta_time)
        print(delta_positive)

        driver = sm.Static.player_nick
        speed = format_speed(sm.Physics.speed_kmh)
        gear = sm.Physics.gear
        rpm = sm.Physics.rpm
        #LAP COUNT

        asm.close()
    
    #Basic Info
    app.setLabel("car_model", f"Car Model: {car_model}")
    app.setLabel("track", f"Track: {track}")
    #Time Info
    app.setLabel("last_time", f"Last Time: {last_time}")
    app.setLabel("best_time", f"Best Time: {best_time}")
    app.setLabel("current_time",f'current_time:{current_time}')
    app.setLabel("delta_time",f"delta:{delta_sign}{delta_time}")
    #Driver Info
    app.setLabel("car_count", f"Car Count: {driver}")
    app.setLabel("speed",f"{speed} KPH")
    app.setLabel("gear",gear)
    #Distance Info
    app.setLabel("laps",f"laps:{laps}")
    app.setLabel("distance",f"{distance}")
    #UPDATE LABELS
    app.after(1000, update_labels)

car_model = ""
track = ""
last_time = ""
best_time = ""
current_time = ""
delta_time = ""
driver = ""
speed = ""
gear = ""
rpm = ""
laps = ""
distance = ""
car_cords = ""
app = gui("sharedmemorymanager")
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
app.addLabel("delta_time",f"DELTA{delta_time}")
app.stopLabelFrame()

app.startLabelFrame("Speed",0,1)
app.addLabel("speed",speed)
app.setLabelFont("speed",size=20)
app.stopLabelFrame()


app.startLabelFrame("Gear",1,1)
app.addLabel("gear",gear)
app.addMeter("tach")
app.stopLabelFrame()

app.startLabelFrame("Laps",0,2)
app.addLabel("laps",laps)
app.addLabel("distance",distance)
app.stopLabelFrame()
app.after(0, update_labels)
app.go()