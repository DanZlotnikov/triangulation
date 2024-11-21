from flask import Flask, jsonify, request
from triangulation import *
from flask_cors import CORS
import logging

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Home route
@app.route('/')
def home():
    return 'hello'

@app.route('/api/triangulate', methods=['GET'])
def triangulate():
    res = calculate_target_position()
    return jsonify({
        "lat": res[0][0],
        "lon": res[0][1],
        "dep": res[0][2]})

@app.route('/api/getPolygon', methods=['GET'])
def getPolygon():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    rib_length = float(request.args.get('rib_length'))
    return jsonify({"polygon": create_equilateral_triangle(lat, lon, rib_length)})

@app.route('/api/data', methods=['POST'])
def post_data():
    data = request.json
    return jsonify({"received_data": data, "status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
