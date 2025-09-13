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
git clone https://github.com/[your-username]/notes-api.git
cd notes-api

# Start the application
docker-compose up
