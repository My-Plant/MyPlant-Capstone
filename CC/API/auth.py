from dotenv import load_dotenv
from firebase_admin import credentials, initialize_app, auth
from flask import Blueprint, Flask, request, jsonify, json
import requests
import os

auth_blueprint = Blueprint('auth', __name__)
load_dotenv()
cred = credentials.Certificate("firebase-admin.json")
default_app = initialize_app(cred)

@auth_blueprint.route('/login', methods=['POST'])
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
@auth_blueprint.route('/register', methods=['POST'])
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