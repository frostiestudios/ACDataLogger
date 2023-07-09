from pyaccsharedmemory import accSharedMemory
import dearpygui.dearpygui as dpg
import os
import sqlite3

dpg.create_context()
dpg.create_viewport(title="ACDL",width=600,height=200)

current_directory = os.getcwd()
print(f"Current Directory{current_directory}")
script_directory = os.path.dirname(os.path.abspath(__file__))
db_file_path = os.path.join(script_directory, 'sharedmemorymanager.db')
conn = sqlite3.connect(db_file_path)
conn.close()
print("Database Setup Complete")
#Format Data
def format_time(time):
    minutes = int(time // 60000)
    seconds = int((time // 1000) % 60)
    milliseconds = int(time % 1000)
    return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
def format_speed(speed):
    return f"{int(speed)}"
def format_text(data):
    if isinstance(data, bytes):
        return str(data, 'utf-8').rstrip('\x00')
    return str(data).rstrip('\x00')
#Data Store
def store_data(car_model, track, last_lap_time,driver):
    conn = sqlite3.connect(db_file_path)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS laps (lap_time TEXT, track TEXT, car_model TEXT)")
    c.execute("INSERT INTO laps (lap_time, track, car_model, driver) VALUES (?, ?, ?, ?)",(format_text(last_lap_time), format_text(track), format_text(car_model), format_text(driver)))
    conn.commit()
    conn.close()

def update():
    
    asm = accSharedMemory()
    sm = asm.read_shared_memory()
    
    if sm is not None:
        print("Game is Running")
        car_model = sm.Static.car_model

        asm.close()
    else:
        print("Game Not Running")


#GUI Functions
def style():
    dpg.show_style_editor()
def docs():
    dpg.show_documentation()
    
#Data Variables
car_model = ""
track = ""
las = ""
with dpg.viewport_menu_bar():
    with dpg.menu(label="Config"):
        dpg.add_menu_item(label="Show Style Editor",callback=style)
        dpg.add_menu_item(label="Documentation",callback=docs)
    with dpg.menu(label="windows"):
        dpg.add_menu_item(label="item1")
with dpg.window(label="1"):
    dpg.add_text("Assetto Corsa Data Logger")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()