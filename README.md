# BSCS-2022-001 — DevOps Final Project

> **Student:** BSCS-2022-001
> **Course:** DevOps Fundamentals
> **Live URL:** http://YOUR_EC2_IP:8000

---

## Architecture

```
GitHub Push
    │
    ├── CI Pipeline (GitHub Actions)
    │       ├── flake8 lint
    │       └── pytest (with PostgreSQL service container)
    │
    └── CD Pipeline (GitHub Actions)
            └── SSH into EC2
                    └── git pull + docker compose up --build
```

**Services:**
- `web` — FastAPI application on port 8000
- `db`  — PostgreSQL 15 with persistent named volume

---

## Local Setup

**Prerequisites:** Docker, Docker Compose, Python 3.12

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/BSCS-2022-001-devops-project
cd BSCS-2022-001-devops-project

# 2. Create your .env file
cp .env.example .env
# Edit .env with your values

# 3. Start all services
docker compose up --build

# 4. Test the API
curl http://localhost:8000/health
curl http://localhost:8000/students
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check + DB connection status |
| POST | /students | Create a new student record |
| GET | /students | List all students |
| GET | /students/{reg_no} | Get student by registration number |

---

## EC2 Deployment

```bash
# SSH into your EC2 instance
ssh -i your-key.pem ubuntu@YOUR_EC2_IP

# Install Docker
sudo apt update && sudo apt install -y docker.io docker-compose-plugin
sudo usermod -aG docker ubuntu

# Clone and run
git clone https://github.com/YOUR_USERNAME/BSCS-2022-001-devops-project ~/devops-project
cd ~/devops-project
cp .env.example .env   # Edit with production values
docker compose -f docker-compose.prod.yml up -d --build
```

**GitHub Secrets required:**
- `EC2_HOST` — your EC2 public IP address
- `EC2_SSH_KEY` — your private SSH key (contents of .pem file)

---

## Running Tests

```bash
pip install -r requirements.txt
pytest app/tests/ -v
```

---

*DevOps Fundamentals — Instructor: Afaq Ahmed*
