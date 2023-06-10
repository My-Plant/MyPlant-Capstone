# Introduction
myPlant Backend (Cloud Comptuting)

## Overview
Private endpoint designed using Flask framework and firebase as authentication for login and register

#### Backend Stack

- Flask
- Firebase
- Tensorflow
- dotenv

#### Cloud Stack

- App Engine
- Cloud Storage

## Install Flask

    python -m pip install flask

## Run the app
1. `git clone https://github.com/henryand1/MyPlant.git`
2. `cd CC`
3. `pip install -r requirements.txt`
4. `python main.py`
    
# API Endpoints

## Register

### Request

```http
POST /register
```

### Responses

```javascript
{
    "message": "Akun berhasil dibuat"
}
```

`email` = email user

`password` = password user

## Login

### Request

```http
POST /login
```

### Responses

```javascript
{
    "message": "Login Berhasil"
}
```

`email` = email user

`password` = password user

## Penyakit

### Request

```http
GET /penyakit
```

### Responses

```javascript
[
  {
    "id": "0",
    "foto": "https://storage.googleapis.com/asia.artifacts.myplant-389306.appspot.com/foto_penyakit/apple_scab.jpg",
    "nama": "Apple Scab",
    "deskripsi": [
      "Kudis apel adalah penyakit paling umum pada pohon apel dan crabapple di Minnesota.",
      "Kudis disebabkan oleh jamur yang menginfeksi daun dan buah.",
      "Buah kudis seringkali tidak layak untuk dimakan.",
      "Daun yang terinfeksi memiliki bintik-bintik hijau hingga coklat.",
      "Daun dengan banyak bercak daun menguning dan rontok lebih awal.",
      "Kehilangan daun melemahkan pohon ketika terjadi bertahun-tahun berturut-turut.",
      "Menanam varietas tahan penyakit adalah cara terbaik untuk mengelola kudis."
    ],
    "solusi": [
      "Pilih varietas yang tahan jika memungkinkan.",
      "Sapu daun di bawah pohon dan hancurkan daun yang terinfeksi untuk mengurangi jumlah spora jamur yang tersedia untuk memulai siklus penyakit lagi musim semi berikutnya.",
      "Siram di malam hari atau dini hari (hindari sprinkler di atas kepala) untuk memberi waktu daun mengering sebelum infeksi dapat terjadi.",
      "Sebarkan lapisan kompos berukuran 3 hingga 6 inci di bawah pohon, jauhkan dari batang, untuk menutupi tanah dan mencegah penyebaran percikan spora jamur.",
      "Untuk kontrol terbaik, semprotkan sabun tembaga cair lebih awal, dua minggu sebelum gejala biasanya muncul. Alternatifnya, mulailah aplikasi saat penyakit pertama kali muncul, dan ulangi dengan interval 7 hingga 10 hari hingga bunganya rontok."
    ]
  }
  ...
```

## Penyakit (id)

### Request

```http
GET /penyakit/0
```

### Responses

```javascript
[
  {
    "id": "0",
    "foto": "https://storage.googleapis.com/asia.artifacts.myplant-389306.appspot.com/foto_penyakit/apple_scab.jpg",
    "nama": "Apple Scab",
    "deskripsi": [
      "Kudis apel adalah penyakit paling umum pada pohon apel dan crabapple di Minnesota.",
      "Kudis disebabkan oleh jamur yang menginfeksi daun dan buah.",
      "Buah kudis seringkali tidak layak untuk dimakan.",
      "Daun yang terinfeksi memiliki bintik-bintik hijau hingga coklat.",
      "Daun dengan banyak bercak daun menguning dan rontok lebih awal.",
      "Kehilangan daun melemahkan pohon ketika terjadi bertahun-tahun berturut-turut.",
      "Menanam varietas tahan penyakit adalah cara terbaik untuk mengelola kudis."
    ],
    "solusi": [
      "Pilih varietas yang tahan jika memungkinkan.",
      "Sapu daun di bawah pohon dan hancurkan daun yang terinfeksi untuk mengurangi jumlah spora jamur yang tersedia untuk memulai siklus penyakit lagi musim semi berikutnya.",
      "Siram di malam hari atau dini hari (hindari sprinkler di atas kepala) untuk memberi waktu daun mengering sebelum infeksi dapat terjadi.",
      "Sebarkan lapisan kompos berukuran 3 hingga 6 inci di bawah pohon, jauhkan dari batang, untuk menutupi tanah dan mencegah penyebaran percikan spora jamur.",
      "Untuk kontrol terbaik, semprotkan sabun tembaga cair lebih awal, dua minggu sebelum gejala biasanya muncul. Alternatifnya, mulailah aplikasi saat penyakit pertama kali muncul, dan ulangi dengan interval 7 hingga 10 hari hingga bunganya rontok."
    ]
  }
```

`id` = id dari penyakit

`nama` = nama dari penyakit

`deskripsi` = deskripsi dari penyakit

`solusi` = solusi dari penyakit

`foto` = foto dari penyakit

## Predict

### Request

```http
POST /predict
```

### Responses

```javascript
{
    "deskripsi": [
        "Kudis apel adalah penyakit paling umum pada pohon apel dan crabapple di Minnesota.",
        "Kudis disebabkan oleh jamur yang menginfeksi daun dan buah.",
        "Buah kudis seringkali tidak layak untuk dimakan.",
        "Daun yang terinfeksi memiliki bintik-bintik hijau hingga coklat.",
        "Daun dengan banyak bercak daun menguning dan rontok lebih awal.",
        "Kehilangan daun melemahkan pohon ketika terjadi bertahun-tahun berturut-turut.",
        "Menanam varietas tahan penyakit adalah cara terbaik untuk mengelola kudis."
    ],
    "id": "0",
    "image_url": "https://storage.googleapis.com/myplant123/scab-on-foliage.jpg",
    "prediction": "Apple Scab",
    "solusi": [
        "Pilih varietas yang tahan jika memungkinkan.",
        "Sapu daun di bawah pohon dan hancurkan daun yang terinfeksi untuk mengurangi jumlah spora jamur yang tersedia untuk memulai siklus penyakit lagi musim semi berikutnya.",
        "Siram di malam hari atau dini hari (hindari sprinkler di atas kepala) untuk memberi waktu daun mengering sebelum infeksi dapat terjadi.",
        "Sebarkan lapisan kompos berukuran 3 hingga 6 inci di bawah pohon, jauhkan dari batang, untuk menutupi tanah dan mencegah penyebaran percikan spora jamur.",
        "Untuk kontrol terbaik, semprotkan sabun tembaga cair lebih awal, dua minggu sebelum gejala biasanya muncul. Alternatifnya, mulailah aplikasi saat penyakit pertama kali muncul, dan ulangi dengan interval 7 hingga 10 hari hingga bunganya rontok."
    ]
}
```

`id` = id dari penyakit

`nama` = nama dari penyakit

`deskripsi` = deskripsi dari penyakit

`solusi` = solusi dari penyakit

`foto` = foto dari penyakit




## Status Codes

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 201 | `CREATED` |
| 400 | `BAD REQUEST` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |
