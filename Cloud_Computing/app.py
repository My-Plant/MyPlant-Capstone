from flask import Flask, request, jsonify, json

app = Flask(__name__)

with open('myPlant-json/penyakit.json') as json_file:
    data = json.load(json_file)

@app.route('/', methods = ['GET'])
def welcome():
    return("Response Success!")

#Menampilkan list data penyakit
@app.route('/penyakit', methods=['GET'])
def pagePenyakit():
    filtered_data = [{"nama": penyakit['nama'], "deskripsi": penyakit['deskripsi']} for penyakit in data]
    return jsonify(filtered_data)

#Menampilkan list data penyakit berdasarkan id penyakit
@app.route('/penyakit/<string:penyakit>', methods=['GET'])
def namaPenyakit(penyakit):
    penyakit_id = penyakit
    for penyakit_data in data:
        if penyakit_data['id'] == penyakit_id:
            return jsonify(penyakit_data)
    return jsonify({'message': 'Penyakit tidak ditemukan!'})

#predict endpoint (ml)