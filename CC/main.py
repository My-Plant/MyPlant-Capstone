# Import necessary modules
# import firebase_admin
from PIL import Image
import io
import requests
import numpy as np
import os
import tensorflow as tf

from google.cloud import storage
from PIL import Image
from flask import Flask, request, jsonify, json
from keras.models import load_model
from werkzeug.utils import secure_filename
from firebase_admin import credentials, initialize_app, auth
import dotenv

# Load Firebase service account credentials

#Login User
app = Flask(__name__)
app.config['SECRET_KEY'] = 'akusayangkamu'
dotenv.load_dotenv()
cred = credentials.Certificate("firebase-admin.json")
default_app = initialize_app(cred)

@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    try:
        user = auth.get_user_by_email(email)
        if user:
            web_api_key_token = os.getenv("WEB_API_KEY_TOKEN")
            firebase_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={}".format(web_api_key_token)

            req = requests.post(firebase_url, json={"email": email, "password": password})
            response_data = req.json()

            if 'idToken' in response_data:
                # Berhasil masuk
                return jsonify({'message': 'Login berhasil'})
            else:
                # Gagal masuk
                return jsonify({'message': 'Password salah'}), 401
         
    except Exception as e:
        return jsonify({'message': 'Email salah '}), 401



#register
@app.route('/register', methods=['POST'])
def register():
    # data = request.get_json()
    email = request.json['email']
    password = request.json['password']

    try:
        user = auth.create_user(
            email=email,
            password=password
        )

        # User berhasil terdaftar
        return {'message': 'Akun berhasil dibuat'},200

    except Exception as e:
        return {'message': 'Email sudah tersedia'}, 400

# Load model
model = tf.keras.models.load_model('app/models/Model_1.h5')

# Load penyakit data
with open('app/myPlant-json/penyakit.json', encoding='utf-8') as json_file:
    contoh = json.load(json_file)

# Initialize Google Cloud Storage client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'credentials.json'
storage_client = storage.Client()
bucket_name = 'myplant'  # Replace with your actual bucket name
bucket = storage_client.bucket(bucket_name)

# Tes Utama
@app.route('/', methods=['GET'])
def welcome():
    return "Response Success!"


# Endpoint untuk menampilkan semua penyakit
@app.route('/penyakit', methods=['GET'])
def pagePenyakit():
    try:
        filtered_data = [{"nama": penyakit['nama'], "deskripsi": penyakit['deskripsi'],"id": penyakit['id'], "solusi": penyakit['solusi']} for penyakit in contoh]
    except:
        return jsonify({'Nama penyakit tidak ditemukan'})
    return jsonify(filtered_data), 200


# Endpoint menampilkan penyakit berdasarkan id
@app.route('/penyakit/<string:penyakit_id>', methods=['GET'])
def namaPenyakit(penyakit_id):
    penyakit_nama = penyakit_id
    for penyakit_data in contoh:
        if penyakit_data['id'] == penyakit_nama:
            return jsonify(penyakit_data), 200
    return jsonify({'message': 'Penyakit tidak ditemukan!'}), 400


# Preprocessing Gambar
def read_image(img):
    img = Image.open(io.BytesIO(img))
    img = img.resize((224, 224))
    img_tensor = tf.keras.preprocessing.image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.0
    return img_tensor


# Prediksi Penyakit Tanaman
@app.route("/predict", methods=['POST'])
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


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)