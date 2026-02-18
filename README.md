# 🌊 OpinionFlow Platform

<div align="center">

**Modern social platform for opinions, discussions, and polls**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Apache Kafka](https://img.shields.io/badge/Apache_Kafka-3.7-231F20?style=for-the-badge&logo=apache-kafka&logoColor=white)](https://kafka.apache.org/)
[![Docker](https://img.shields.io/badge/Docker-24.0-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

</div>

---

## 📖 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Getting Started](#-getting-started)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 About

**OpinionFlow** is a modern social platform designed to facilitate meaningful discussions, opinion sharing, and interactive polls. Built with scalability and performance in mind, it leverages clean architecture principles and modern technologies to deliver a robust backend solution.

### Key Capabilities
- 👤 User authentication and authorization
- 📝 Create and manage posts, opinions, and polls
- 💬 Real-time discussions and comments
- 🔔 Event-driven notifications via Kafka
- 🔐 Secure JWT-based authentication

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Authentication** | Secure JWT-based auth with refresh tokens |
| **User Management** | Complete user profiles and settings |
| **Content Creation** | Posts, opinions, and polls with rich media |
| **Real-time Events** | Event-driven architecture using Apache Kafka |
| **Scalable Design** | Clean architecture with DDD principles |
| **Containerized** | Full Docker support for easy deployment |
| **API Documentation** | Auto-generated OpenAPI/Swagger docs |

---

## 🛠️ Tech Stack

### Backend
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) – Modern async web framework
- **Language:** Python 3.12+
- **Database:** PostgreSQL 16+ with SQLAlchemy (async)
- **Message Broker:** Apache Kafka (via FastStream)
- **Authentication:** JWT (AuthX + PyJWT) + Argon2 password hashing

### Infrastructure
- **Containerization:** Docker & Docker Compose
- **Reverse Proxy:** Traefik
- **Database Migrations:** Alembic
- **Dependency Injection:** Dishka

### Development Tools
- **Code Quality:** Ruff, Black, MyPy
- **Testing:** Pytest + Pytest-Asyncio
- **Environment:** python-dotenv, Pydantic Settings

---

## 🏗️ Architecture

OpinionFlow follows **Clean Architecture** principles with Domain-Driven Design (DDD):

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│  (API Routers, CLI, Schemas, Controllers)                   │
├─────────────────────────────────────────────────────────────┤
│                    Application Layer                         │
│  (Use Cases, Services, DTOs, Interfaces)                    │
├─────────────────────────────────────────────────────────────┤
│                      Domain Layer                            │
│  (Entities, Value Objects, Domain Events, Exceptions)       │
├─────────────────────────────────────────────────────────────┤
│                   Infrastructure Layer                       │
│  (Database, Message Broker, External Services, DI)          │
└─────────────────────────────────────────────────────────────┘
```

### System Architecture

```
                    ┌─────────────┐
                    │   Traefik   │
                    │  (Reverse   │
                    │    Proxy)   │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
┌────────────────┐ ┌──────────────┐ ┌──────────────┐
│    Backend     │ │  PostgreSQL  │ │    Kafka     │
│   (FastAPI)    │ │   Database   │ │   Broker     │
└────────────────┘ └──────────────┘ └──────────────┘
         │                                   │
         └───────────────────────────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Kafka UI   │
                    │  (Dashboard) │
                    └──────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.12+
- **Docker** & **Docker Compose**
- **Git**

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/codesforges/OpinionFlow-Platform.git
   cd OpinionFlow-Platform
   ```

2. **Configure environment variables**
   ```bash
   # Copy example environment files
   cp src/env/database_settings.env.example src/env/database_settings.env
   cp src/env/authx_settings.env.example src/env/authx_settings.env
   cp src/env/kafka_broker_settings.env.example src/env/kafka_broker_settings.env
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Access the services**
   - **API:** http://localhost
   - **Swagger UI:** http://localhost/docs
   - **ReDoc:** http://localhost/redoc
   - **Kafka UI:** http://kafka.localhost

5. **Check logs**
   ```bash
   docker-compose logs -f backend
   ```

### Local Development Setup

1. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

2. **Install dependencies**
   ```bash
   pip install -r src/requirements.txt
   ```

3. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

4. **Start the development server**
   ```bash
   uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000
   ```

---

## 📚 API Documentation

Once the application is running, access the interactive API documentation:

| Documentation | URL |
|--------------|-----|
| **Swagger UI** | http://localhost/docs |
| **ReDoc** | http://localhost/redoc |
| **OpenAPI JSON** | http://localhost/openapi.json |

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/auth/register` | User registration |
| `POST` | `/api/v1/auth/login` | User login |
| `POST` | `/api/v1/auth/refresh` | Refresh access token |
| `GET` | `/api/v1/users` | Get users list |
| `GET` | `/api/v1/users/{id}` | Get user by ID |

---

## 📁 Project Structure

```
OpinionFlow-Platform/
├── src/
│   ├── app/                    # Application entry point
│   │   └── main.py             # FastAPI app factory
│   ├── application/            # Application layer (use cases)
│   ├── common/                 # Shared utilities
│   │   └── logger.py           # Logging configuration
│   ├── config/                 # Configuration files
│   ├── domain/                 # Domain layer (DDD)
│   │   ├── entities/           # Domain entities
│   │   ├── events/             # Domain events
│   │   ├── exceptions/         # Domain exceptions
│   │   ├── interfaces/         # Repository interfaces
│   │   └── value_objects/      # Value objects
│   ├── env/                    # Environment configuration
│   ├── infrastructure/         # Infrastructure layer
│   │   ├── db/                 # Database configuration
│   │   ├── di/                 # Dependency injection
│   │   ├── messages/           # Message broker (Kafka)
│   │   └── repositories/       # Repository implementations
│   ├── presentation/           # Presentation layer
│   │   ├── api/
│   │   │   ├── routers/        # API routers
│   │   │   └── schemas/        # Pydantic schemas
│   │   └── cli/                # CLI commands
│   ├── scripts/                # Utility scripts
│   ├── docker/                 # Docker configuration
│   └── requirements.txt        # Python dependencies
├── alembic.ini                 # Alembic configuration
├── docker-compose.yaml         # Docker Compose services
├── LICENSE                     # MIT License
└── README.md                   # This file
```

---

## 🧪 Development

### Running Tests

```bash
pytest src/tests -v --cov=src
```

### Code Quality

```bash
# Linting
ruff check src/

# Formatting
black src/

# Type checking
mypy src/
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow [PEP 8](https://pep8.org/) style guide
- Write meaningful tests for new features
- Keep commits atomic and well-documented
- Update documentation as needed

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

```
MIT License - Copyright (c) 2026 CodesForge
```

---

## 📬 Contact

- **GitHub:** [@CodesForge](https://github.com/CodesForge)
- **Project Link:** [OpinionFlow-Platform](https://github.com/CodesForge/OpinionFlow-Platform)

---

<div align="center">

**Made with ❤️ by CodesForge**

⭐ Star this repo if you find it helpful!

</div>
