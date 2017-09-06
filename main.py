from flask import Flask, jsonify, request, render_template
import json
app = Flask(__name__)

@app.route("/")
def test():
  return render_template('a.html')

@app.route("/post/", methods=['POST'])
def post():
  lat = str(request.form['lat'])
  long = str(request.form['long'])

  print str(request.form)

  return 'lat: ' + lat + ' long: ' + long

if __name__ == "__main__":
  app.run(host='0.0.0.0', threaded=True)
