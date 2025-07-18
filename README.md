# 🚉 RailSathi Complaint Microservice (Dockerized)

This is a FastAPI-based complaint management microservice for handling train passenger grievances. It supports complaint creation, retrieval, updates, and media uploads. Fully containerized using Docker and uses PostgreSQL for storage.

---

## ✅ Features

* Submit complaints with media files
* View complaints by ID or date + mobile number
* Edit or delete complaints (permission-based)
* Upload/delete associated media files
* Train → Depot → Division → Zone hierarchy
* Swagger UI for API testing (`/rs_microservice/docs`)
* Dockerized FastAPI + PostgreSQL setup

---

## ⚙️ Tech Stack

* **Backend:** FastAPI
* **Database:** PostgreSQL
* **Containerization:** Docker, Docker Compose
* **Docs:** Swagger UI (auto-generated)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/patchadevikasai/railsathi-dockerized.git
cd railsathi-dockerized
```
### 2. Setup Environment
Create and configure your .env file:

```bash
cp .env.example .env
```

### 3. Run using Docker Compose

```bash
docker-compose up --build
```

API: http://localhost:8000/items/

Docs: http://localhost:8000/rs_microservice/docs

📁 Project Structure

📦 railsathi-dockerized/
├── app/
│   ├── main.py
│   ├── services.py
│   └── database.py
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── README.md


🧪 Testing the API
After starting the server, open:
```bash
http://localhost:8000/rs_microservice/docs
```
Test all endpoints via Swagger UI without needing Postman or a frontend.

