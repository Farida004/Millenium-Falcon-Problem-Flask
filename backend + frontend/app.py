from flask import Flask,render_template,request
from mf import *
import json
import sqlite3

# Opening JSON file
milleniumfalcon = open('millenium-falcon.json')
empire = open('empire.json')

# returns JSON object as 
# a dictionary
mf_data = json.load(milleniumfalcon)
e_data = json.load(empire)

# creating file path
dbfile = 'universe.db'
# Create a SQL connection to our SQLite database
con = sqlite3.connect(dbfile)

# creating cursor
cur = con.cursor()

# MF data
autonomy = mf_data['autonomy']
departure = mf_data['departure']
arrival = mf_data['arrival']

#Empire data
countdown = e_data['countdown']
bounty_hunters_info = e_data['bounty_hunters']

# Create a graph given in the above diagram
mf = Millennium_Falcon(autonomy)

#Universe db data
cur.execute("SELECT * FROM routes")

rows = cur.fetchall()

for row in rows:
    mf.addRoute(*row)

app = Flask(__name__)

@app.route("/home")
def hello():
    return render_template('index.html',value = " ")

@app.route('/home', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
    f = request.files['file']
    filename = f.filename
    name,extension = filename.split(".")
    print(extension)
    if extension =="json":
        e_data = json.load(f)
        countdown = e_data['countdown']
        bounty_hunters_info = e_data['bounty_hunters']
        print(bounty_hunters_info)
        return render_template('index.html', value = (f'Probability: {mf.print_all_paths(departure, arrival,countdown, bounty_hunters_info)}%'))
    else:
        return render_template('index.html', value = ("Wrong file format. Please, upload a .json file"))
    
@app.route("/home")
def backtohome():
    return render_template('index.html',value = " ")

@app.route("/about")
def about_project():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

