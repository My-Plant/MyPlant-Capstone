# Introduction
myPlant Cloud Computing

## Install Flask

    python -m pip install flask

## Run the app

    python server.py
    
# API Endpoints

## Penyakit

### Request

```http
GET http://127.0.0.1:8080/penyakit
```

### Responses

```javascript
   {
       "id": "1",
       "nama": "Jamur",
       "deskripsi": "Jamur adalah penyakit tanaman yang membuat tanaman layu dan rusak"
    }
```

## Penyakit (id)

### Request

```http
GET http://127.0.0.1:8080/penyakit/2
```

### Responses

```javascript
   {
       "id": "2",
       "nama": "Bintik",
       "deskripsi": "Bintik adalah penyakit tanaman yang disebabkan oleh ulat dan dapat merusak daun",
       "faktor": string,
       "saran": string
    }
```

`id` = id dari penyakit

`nama` = nama dari penyakit

`deskripsi` = deskripsi dari penyakit

## Status Codes

Gophish returns the following status codes in its API:

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 201 | `CREATED` |
| 400 | `BAD REQUEST` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |
