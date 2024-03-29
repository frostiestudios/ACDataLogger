from bottle import request, route, run, static_file, template, redirect
import sqlite3
import socket
import os

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

script_directory = os.path.dirname(os.path.abspath(__file__))


db_file_path = os.path.join(script_directory, 'sharedmemmanager.db')
template_dir = os.path.join(script_directory, 'pages')
laps_templ = os.path.join(template_dir, 'laps.html')
index_templ = os.path.join(template_dir, 'index.html')
content_templ = os.path.join(template_dir, 'content.html')
css = os.path.join(template_dir, 'style.css')

# Connect to the database using the absolute file path
conn = sqlite3.connect(db_file_path)
conn.close()
print(IPAddr)


# Index
@route("/")
def index():
    return template(index_templ,
                    addr=IPAddr)


# Static Files (CSS)
@route("/pages/<filename:path>")
def static(filename):
    return static_file(filename, root=template_dir)



# Lap Browser
# Lap Browser
@route('/laps')
def laps():
    conn = sqlite3.connect(db_file_path)
    c = conn.cursor()
    c.execute("SELECT DISTINCT track FROM laps")
    tracks = [row[0] for row in c.fetchall()]
    c.close()

    track = request.query.get('track') # type: ignore
    sort_by = request.query.get('sort_by') # type: ignore

    query = "SELECT lap_time, track, car_model, driver, date FROM laps"
    params = ()
    c = conn.cursor()
    if track:
        query = "SELECT lap_time, track, car_model, driver, date FROM laps WHERE track=?"
        params = (track,)
    else:
        query = "SELECT lap_time, track, car_model, driver, date FROM laps"

    if sort_by:
        query += f" ORDER BY {sort_by}"

    c.execute(query, params)
    result = c.fetchall()
    c.close()

    output = template(laps_templ, rows=result, tracks=tracks, request=request)
    return output


# Run
@route('/map')
def more():
    return ("More Has Not Been Configured <a href='/'>Back</a>")


@route('/dashboard')
def dash():
    current_time = sharedmem.current_time
    return template('./pages/dash.html',
                    current_time=current_time
                    )


@route('/content')
def content():
    return ("More Has Not Been Configured <a href='/'>Back</a>")

@route('/media')
def media():
    return template('./pages/media.html')

run(host=IPAddr, port=5159, reloader=True, debug=True)
