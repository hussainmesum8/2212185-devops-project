# 2212185 — DevOps Final Project

> **Student:** Mohammad Mesum Hussain  
> **Registration Number:** 2212185  
> **Course:** DevOps Fundamentals  
> **Live URL:** http://YOUR_EC2_IP:8000

---

## Architecture

```text
GitHub Push (main)
    │
    ├── CI Pipeline (GitHub Actions)
    │       ├── flake8 lint
    │       └── pytest (with PostgreSQL service container)
    │
    └── CD Pipeline (GitHub Actions)
            └── SSH into EC2
                    └── git pull + docker compose -f docker-compose.prod.yml up -d --build
```

**Services:**

- `web` — FastAPI application running on port `8000`
- `db`  — PostgreSQL 15 with persistent named volume `postgres_data`

---

## Local Setup

**Prerequisites:** Docker, Docker Compose, Python 3.12

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/2212185-devops-project.git
cd 2212185-devops-project

# 2. Create your .env file
cp .env.example .env
# Edit .env with your database credentials

# 3. Start all services
docker compose up --build

# 4. Test the API
curl http://localhost:8000/health
curl http://localhost:8000/students
```

---

## API Endpoints

| Method | Endpoint             | Description                                 |
|--------|----------------------|---------------------------------------------|
| GET    | `/health`            | Health check + DB connection status         |
| POST   | `/students`          | Create a new student record                 |
| GET    | `/students`          | List all students                           |
| GET    | `/students/{reg_no}` | Get a single student by registration number |

### Example: Create a student

```bash
curl -X POST http://localhost:8000/students \
  -H "Content-Type: application/json" \
  -d '{
    "reg_no": "2212185",
    "name": "Mohammad Mesum Hussain",
    "semester": 6,
    "section": "A"
  }'
```

### Example: Health check

```bash
curl http://localhost:8000/health
# Expected response:
# {"status":"ok","db":"connected","student":"2212185"}
```

---

## EC2 Deployment

### 1. Launch an Ubuntu EC2 instance

- AMI: Ubuntu Server 22.04 LTS (free tier)
- Instance type: `t2.micro`
- Security Group inbound rules:
  - SSH (port 22) from your IP
  - HTTP (port 8000) from anywhere `0.0.0.0/0`

### 2. SSH into the instance and install Docker

```bash
ssh -i your-key.pem ubuntu@YOUR_EC2_IP

sudo apt update && sudo apt upgrade -y
sudo apt install -y docker.io docker-compose-plugin
sudo usermod -aG docker ubuntu
# Log out and log back in for group changes to take effect
```

### 3. Clone the repository and start production containers

```bash
git clone https://github.com/YOUR_USERNAME/2212185-devops-project.git ~/devops-project
cd ~/devops-project
cp .env.example .env   # Edit with production database credentials
docker compose -f docker-compose.prod.yml up -d --build
```

### 4. Configure GitHub Secrets for CD

In your GitHub repository, go to **Settings → Secrets and variables → Actions** and add:

| Secret        | Description                                          |
|---------------|------------------------------------------------------|
| `EC2_HOST`    | Your EC2 public IP address                           |
| `EC2_SSH_KEY` | Contents of your private `.pem` key file             |
| `DB_USER`     | PostgreSQL username (must match `.env` on EC2)       |
| `DB_PASSWORD` | PostgreSQL password (must match `.env` on EC2)       |
| `DB_NAME`     | PostgreSQL database name (must match `.env` on EC2)  |

---

## Running Tests Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest app/tests/ -v
```

---

## Project Structure

```text
2212185-devops-project/
├── app/
│   ├── main.py               # FastAPI routes
│   ├── database.py           # SQLAlchemy DB engine & session
│   ├── models.py             # Student SQLAlchemy model
│   └── tests/
│       ├── conftest.py       # pytest fixtures
│       ├── test_health.py    # /health endpoint tests
│       └── test_students.py  # /students endpoint tests
├── Dockerfile
├── docker-compose.yml        # Local development
├── docker-compose.prod.yml   # Production (EC2)
├── requirements.txt
├── .env.example
├── .gitignore
├── .dockerignore
├── .github/
│   └── workflows/
│       ├── ci.yml            # Lint + test
│       └── cd.yml            # Deploy to EC2
└── README.md
```

---

*DevOps Fundamentals — Final Project*
