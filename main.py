from flask import Flask, jsonify, request, render_template, g
import json
import math
import sqlite3
import csv
app = Flask(__name__)
db_location = 'var/accident.db'

def get_db():
  db = getattr(g, 'db', None)
  if db is None:
    db = sqlite3.connect(db_location)
    g.db = db
  return db

def init_db():
  with app.app_context():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
      db.cursor().executescript(f.read())
    db.commit()

def pop_db():
  with app.app_context():
    db = get_db()
    with app.open_resource('var/Accidents_2015.csv', mode='r') as f:
      reader = csv.reader(f)
      data = next(reader)
      query = 'INSERT INTO accidents VALUES ({0})'
      query = query.format(','.join('?' * len(data)))
      cursor = db.cursor()
      cursor.execute(query, data)
      for data in reader:
        cursor.execute(query, data)
      db.commit()

@app.route("/")
def test():
  return render_template('a.html')

@app.route("/post/", methods=['POST'])
def post():
  lat = float(str(request.form['lat']))
  long = float(str(request.form['long']))

  print str(request.form)

  westLimit = calcNewLat(lat, long, 135)
  eastLimit = [lat, long-(westLimit[1]-long)]
  northLimit = calcNewLat(lat, long, 90)
  southLimit = [lat-(northLimit[0]-lat), long]

  print(str(westLimit))
  print(str(eastLimit))
  print(str(northLimit))
  print(str(southLimit))

  db = get_db()

  sql = "SELECT * FROM accidents WHERE (Latitude <= " + str(northLimit[0]) + " AND Latitude >= " + str(southLimit[0]) + ") AND (Longitude <= " + str(eastLimit[1]) + " AND Longitude >= " + str(westLimit[1]) + ")"
  print sql

  data = []

  for row in db.cursor().execute(sql):
    print str(row)
    data.append(row)

  return jsonify(data = data)

def calcNewLat(oldLat, oldLong, b):
  earthR = 6378.1
  brng = b
  d = 75

  lat1 = math.radians(oldLat)
  lon1 = math.radians(oldLong)

  dx = d*math.cos(brng)
  dy = d*math.sin(brng)

  delta_lon = dx/(111320*math.cos(lat1))
  delta_lat = dy/110540

  lon2 = lon1 + delta_lon
  lat2 = lat1 + delta_lat

  lat2 = math.degrees(lat2)
  lon2 = math.degrees(lon2)

  print(lat2)
  print(lon2)

  return [lat2,lon2]

def calcNewLong(oldLong, distance):
  return []

if __name__ == "__main__":
  app.run(host='0.0.0.0', threaded=True)
