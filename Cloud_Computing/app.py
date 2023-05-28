import uuid
import firebase_admin
import keras
import io
import requests
import numpy as np
import os
import tensorflow as tf


from flask import Flask, request, jsonify, json
from firebase_admin import credentials, auth, firestore
from keras.models import load_model
from PIL import Image

app = Flask(__name__)

# db = firestore.client()
# user_Ref = db.collection('user')

cred = credentials.Certificate("serviceAccountKey.json")
firebase = firebase_admin.initialize_app(cred)
# auth = firebase.auth()

# Login dan Register masih dalam tahap pengerjaan!
# @app.route('/register',methods=["GET","POST"])
# def register():
#     email = request.get_json()['email']
#     password = request.get_json()['password']

#     if email is None or password is None:
#         return {'message':'Email atau Password Anda Belum Diisi!'},400
#     try:
#         user = auth.create_user(email=email,password=password)
#         return {'message':'Akun Telah Berhasil Dibuat!'},200
#     except:
#         return {'message':'Email Sudah Digunakan!'},400

# @app.route("/login" ,methods=["GET","POST"])
# def login():
#     email = request.get_json()["email"]
#     password = request.get_json()["password"]

#     try:
#         user = user.auth().sign_in_with_email_and_password(email,password)
#         return {"msg":"Anda Berhasil Login!"}, 200
#     except:
#         return {'msg':'Email atau Password Salah'}, 400

# with open('myPlant-json/penyakit.json') as json_file:
#     data = json.load(json_file)

@app.route('/', methods = ['GET'])
def welcome():
    return("Response Success!")

#Menampilkan list data penyakit
@app.route('/penyakit', methods=['GET'])
def pagePenyakit():
    filtered_data = [{"nama": penyakit['nama'], "deskripsi": penyakit['deskripsi']} for penyakit in data]
    return jsonify(filtered_data), 200

#Menampilkan list data penyakit berdasarkan id penyakit
@app.route('/penyakit/<string:penyakit>', methods=['GET'])
def namaPenyakit(penyakit):
    penyakit_id = penyakit
    for penyakit_data in data:
        if penyakit_data['id'] == penyakit_id:
            return jsonify(penyakit_data), 200
    return jsonify({'message': 'Penyakit tidak ditemukan!'}), 400

#predict endpoint (ml)
#Image Pre-processing
def load_image_from_url(image_url):
    '''Image Preprocessing Function'''
    response = requests.get(image_url)
    img = Image.open(io.BytesIO(response.content))
    img = img.resize((224, 224))
    img_tensor = tf.keras.preprocessing.image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.0

    return img_tensor

#Load Model
model_url = "https://storage.googleapis.com/myplant_storage/Model_1.h5"  # Replace with the correct model URL
model_response = requests.get(model_url)
model_file_path = "model.h5"  # Local file path to save the model
with open(model_file_path, "wb") as f:
    f.write(model_response.content)
model = load_model(model_file_path)


# PREDICT
@app.route("/predict", methods=["GET","POST"])
def predict():
    if "image_url" not in request.args:
        return jsonify({"error": "no image_url"})

    image_url = request.args.get("image_url")

    try:
        new_image = load_image_from_url(image_url)
        prediction_labels = [
            "Apple Scab",
            "Apple Black Rot",
            "Apple Cedar rust",
            "Apple Healthy",
            "Corn Cercospora Leaf Spot | Gray Leaf Spot",
            "Corn Common Rust",
            "Corn Northern Leaf Blight",
            "Corn Healthy",
            "Grape Black Rot",
            "Grape Esca | Black Measles",
            "Grape Leaf Blight | Isariopsis Leaf Spot",
            "Grape Healthy",
            "Potato Early Blight",
            "Potato Late Blight",
            "Potato Healthy",
            "Strawberry Leaf Scorch",
            "Strawberry Healthy"
        ]

        prediction = np.argmax(model.predict(new_image)[0])
        result = prediction_labels[prediction]

        data = {"prediction": result}

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

# Remove the model file after using
os.remove(model_file_path)