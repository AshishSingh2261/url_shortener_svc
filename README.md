# 🔗 TinyURL Service

A high-performance, container-safe URL shortening service built with **FastAPI**, **MongoDB**, **Redis**, and **asyncio**. This service uses a synchronized counter with locking to generate unique short URLs across containers.

---

## 🚀 Features

- ✅ Shorten long URLs to compact, unique TinyURLs  
- 🔁 Redirect users from TinyURLs to the original URLs  
- 🔐 Counter-based hash generation with container-safe locks  
- ⚡ Caching with Redis for fast URL lookup  
- 🧱 MongoDB for persistent storage  
- ⚙️ Asynchronous & scalable architecture  

---

## 📦 Tech Stack

- **FastAPI** – for building high-performance async APIs  
- **MongoDB** – as the primary datastore for URL mappings  
- **Redis** – for caching shortened URLs  
- **Asyncio** – to handle async tasks and scheduling  
- **Python 3.10+**

---

## 📂 Project Structure

.
├── main.py                 # FastAPI server and routes
├── src/
│   ├── database_layer.py   # MongoDB client and helpers
│   └── tinyurl.py          # URL shortening logic & counter



---

## 📌 API Endpoints

### ➕ Create TinyURL

**POST** `/service/create_tiny_url`

**Request Body:**

```json
{
  "original_url": "https://example.com/long-link"
}

{
  "tiny_url": "https://tinyurl/abc123",
  "original_url": "https://example.com/long-link"
}```

### 🔗 Fetch Original URL

**GET** /service/fetch_original_url/{tiny_url_hash}

Redirects to the original URL if the hash is valid.




## 🧪 Run Locally

### 🔧 Prerequisites

- Python 3.10+
- MongoDB running locally or via Docker
- Redis running locally or via Docker

### 📥 Install dependencies

```bash
pip install -r requirements.txt```

### 🚀 Start the service

```bash
uvicorn main:app --reload```

The service will be live at: http://localhost:8000/service


API Documentation
Swagger UI: http://localhost:8000/service/docs
