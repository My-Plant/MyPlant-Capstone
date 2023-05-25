from flask import Flask, request, jsonify, json

app = Flask(__name__)

with open('myPlant-json/penyakit.json') as json_file:
    data = json.load(json_file)

@app.route('/', methods = ['GET'])
def welcome():
    return("Response Success!")

#Menampilkan list data penyakit
@app.route('/penyakit', methods = ['GET'])
def getPenyakit():
    return jsonify(data)

#Menampilkan list data penyakit berdasarkan id penyakit
@app.route('/penyakit/<string:penyakit>', methods=['GET'])
def namaPenyakit(penyakit):
    penyakit_id = penyakit
    for penyakit_data in data:
        if penyakit_data['id'] == penyakit_id:
            return jsonify(penyakit_data)
    return jsonify({'message': 'Penyakit not found'})

#predict endpoint (ml)