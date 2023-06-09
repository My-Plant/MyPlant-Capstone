import requests
from flask import Blueprint, Flask, request, jsonify, json

penyakit_blueprint = Blueprint('penyakit', __name__)

with open('app/myPlant-json/penyakit.json', encoding='utf-8') as json_file:
    contoh = json.load(json_file)


@penyakit_blueprint.route('/penyakit', methods=['GET'])
def pagePenyakit():
    try:
        filtered_data = [{"nama": penyakit['nama'], 
                        "deskripsi": penyakit['deskripsi'],
                        "id": penyakit['id'], 
                        "solusi": penyakit['solusi'], 
                        "foto": penyakit['foto']} for penyakit in contoh]
    except:
        return jsonify({'Nama penyakit tidak ditemukan'})
    return jsonify(filtered_data), 200


# Endpoint menampilkan penyakit berdasarkan id
@penyakit_blueprint.route('/penyakit/<string:penyakit_id>', methods=['GET'])
def namaPenyakit(penyakit_id):
    penyakit_nama = penyakit_id
    for penyakit_data in contoh:
        if penyakit_data['id'] == penyakit_nama:
            return jsonify(penyakit_data), 200
    return jsonify({'message': 'Penyakit tidak ditemukan!'}), 400