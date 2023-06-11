from bottle import request, route, run, static_file, template
import sqlite3
#Index
@route("/")
def index():
    return template('pages/index')
# Static Files (CSS)
@route("/pages/<filename:path>")
def static(filename):
    return static_file(filename, root="pages/")
#Lap Browser
@route('/laps')
def laps():
    conn = sqlite3.connect('sharedmemmanager.db')
    c = conn.cursor()
    c.execute("SELECT lap_time, track, car_model FROM laps")
    result = c.fetchall()
    c.close()
    output = template('pages/laprecords',rows=result)
    return output
#Run
run(host='localhost',port=5159,reloader=True,debug=True)