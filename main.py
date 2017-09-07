from flask import Flask, jsonify, request, render_template
import json
import math
app = Flask(__name__)

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

  return 'lat: ' + str(lat) + ' long: ' + str(long)

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
