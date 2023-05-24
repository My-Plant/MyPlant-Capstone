from flask import Flask, request, jsonify, json

app = Flask(__name__)

with app.open_resource('myPlant-json\penyakit.json') as data:
    penyakit = json.load(data)

#login (with firebase)

@app.route('/', methods = ['GET'])
def welcome():
    return jsonify("welcome")

@app.route('/penyakit', methods = ['GET'])
def display():
    return jsonify(penyakit)

#predict (ml)