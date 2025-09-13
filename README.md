# Notes API - AI Powered Note Taking System

A modern REST API with authentication, async AI summarization, and Docker deployment.

## 🚀 Features

- **JWT Authentication** with role-based access (ADMIN/AGENT)
- **AI-Powered Summarization** with background workers
- **PostgreSQL Database** with multi-tenancy support
- **Redis** for message queueing
- **Docker Containerization** for easy deployment
- **Automatic API Documentation** with Swagger

## 📦 Tech Stack

- **Backend:** Python FastAPI
- **Database:** PostgreSQL
- **Cache & Queue:** Redis
- **Async Tasks:** Celery
- **Containerization:** Docker
- **Deployment:** Koyeb + Neon

## 🛠️ Installation

### Prerequisites
- Docker
- Docker Compose

### Quick Start

```bash
# Clone the repository
git clone https://github.com/emindalkilic/notes-api.git
cd notes-api

# Start the application
docker-compose up

```

The API will be available at: http://localhost:8000

## 📚 API Documentation

Once running, access the interactive Swagger docs at:
http://localhost:8000/docs

### Key Endpoints

    POST /signup - User registration

    POST /login - User login (returns JWT token)

    POST /notes - Create a new note (triggers AI summarization)

    GET /notes/{id} - Get note details with status

    GET /notes - List all notes (role-based access)

## 🔧 Environment Variables

Create a .env file:

```bash

DATABASE_URL=postgresql://user:password@db:5432/notesdb
SECRET_KEY=your-secret-key-here

```

## 🐳 Docker Architecture

The application consists of 4 services:

   **1. web** - FastAPI server (port 8000)

   **2. db** - PostgreSQL database

   **3. redis** - Redis server for message queue

   **4. worker** - Celery worker for async tasks

## 🎯 Usage Example

**1. Register a user:**

```bash

curl -X POST "http://localhost:8000/signup" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

```

**2. Login to get JWT token:**

```bash

curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

```

**3. Create a note (with AI summarization)**

```bash

curl -X POST "http://localhost:8000/notes" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"raw_text": "This is a long text that will be summarized by the AI background worker..."}'

```

## 🌐 Live Demo

**API URL:** https://notes-api-nphd.onrender.com  
**Documentation:** https://notes-api-nphd.onrender.com/docs

## 🎥 Demo Video

Watch the Loom demo: .... 

## 📄 License

This project is created for assignment purposes.
