from PIL import Image
import tensorflow as tf
import numpy as np
import os
import io
from flask import Blueprint, Flask, request, jsonify, json
from keras.models import load_model
from werkzeug.utils import secure_filename
from google.cloud import storage

with open('app/myPlant-json/penyakit.json', encoding='utf-8') as json_file:
    contoh = json.load(json_file)

prediction_blueprint = Blueprint('prediction',__name__)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'credentials.json'
storage_client = storage.Client()
bucket_name = 'myplant123'  # Replace with your actual bucket name
bucket = storage_client.bucket(bucket_name)

model = tf.keras.models.load_model('app/models/Model_1.h5')

def read_image(img):
    img = Image.open(io.BytesIO(img))
    img = img.resize((224, 224))
    img_tensor = tf.keras.preprocessing.image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.0
    return img_tensor


# Prediksi Penyakit Tanaman
@prediction_blueprint.route("/predict", methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "Please try again. The Image doesn't exist"

    file = request.files.get('file')

    if not file:
        return "Please try again. The Image doesn't exist"

    # Membaca input file
    img_bytes = file.read()

    # Membuat filename unik untuk file yang di upload
    filename = secure_filename(file.filename)
    blob = bucket.blob(filename)

    # Upload gambar ke cloud storage
    blob.upload_from_string(img_bytes, content_type='image/jpeg')

    # Mendapatkan public url
    image_url = blob.public_url

    # File image untuk prediksi
    images = read_image(img_bytes)

    try:
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

        prediction = np.argmax(model.predict(images)[0])
        result = prediction_labels[prediction]

        for penyakit_data in contoh:
            if penyakit_data['nama'] == result:
                penyakit_id = penyakit_data['id']
                deskripsi = penyakit_data['deskripsi']
                solusi = penyakit_data['solusi']
                
                break
        else:
            # Penyakit tidak ditemukan penyakit.json
            return jsonify({'message': 'Penyakit tidak ditemukan!'}), 400

        return {
            'prediction': result,
            'image_url': image_url,
            'id': penyakit_id,
            'deskripsi': deskripsi,
            'solusi' : solusi
        }
    except Exception as e:
        return jsonify({"error": str(e)})