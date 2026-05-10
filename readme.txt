
 XAI Gig Score

An explainable AI-based credit scoring system for gig workers and thin-file consumers in India.

The project predicts credit risk using gig worker-related financial and behavioral data. It includes a FastAPI backend, React frontend, PostgreSQL database, and ML pipeline with explainability support.

---

 Tech Stack

 Frontend
- React
- Vite
- JavaScript
- CSS
- pnpm

 Backend
- FastAPI
- Python
- PostgreSQL
- SQLAlchemy
- JWT Authentication

 Machine Learning
- Python
- Scikit-learn
- SHAP
- Pandas
- NumPy

 Database / DevOps
- PostgreSQL
- Docker
- Docker Compose

---

 Project Structure

```txt
xai-gig-score/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   └── main.py
│   └── requirements.txt
│
├── frontend/
│   └── front_m-main/
│       ├── src/
│       ├── package.json
│       ├── pnpm-lock.yaml
│       └── vite.config.ts
│
├── ml/
│   ├── src/
│   │   ├── train.py
│   │   ├── evaluate.py
│   │   ├── scoring.py
│   │   ├── shap_explainer.py
│   │   └── utils.py
│   └── requirements.txt
│
├── docker/
│   └── docker-compose.yml
│
├── .gitignore
└── Readme.md

Installation and Setup
Prerequisites
Make sure these are installed on your system:
Git
Python 3.10 or above
Node.js
npm
pnpm
Docker Desktop
Check versions:
git --version
python --version
node -v
npm -v
docker --version

Check pnpm:
pnpm -v

If pnpm is not installed:
npm install -g pnpm

Check again:
pnpm -v


1. Clone the Repository
git clone https://github.com/KaranSJ22/xai-gig-score.git
cd xai-gig-score


2. Database Setup Using Docker
Start PostgreSQL using Docker Compose:
docker compose -f docker/docker-compose.yml up -d

Check running containers:
docker ps

To stop the database:
docker compose -f docker/docker-compose.yml down

To restart the database:
docker compose -f docker/docker-compose.yml down
docker compose -f docker/docker-compose.yml up -d


3. Backend Setup
Go to the backend folder:
cd backend

Create a virtual environment:
python -m venv venv

Activate the virtual environment.
Windows PowerShell
venv\Scripts\Activate.ps1

Windows CMD
venv\Scripts\activate.bat

Linux / macOS
source venv/bin/activate

Install backend dependencies:
pip install -r requirements.txt

Create a .env file inside the backend folder:
DATABASE_URL=postgresql://postgres:password@localhost:5432/gig_score_db
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

Run the backend server:
uvicorn app.main:app --reload

Backend will run at:
http://localhost:8000

FastAPI Swagger documentation:
http://localhost:8000/docs

ReDoc documentation:
http://localhost:8000/redoc


4. Frontend Setup
Open a new terminal from the project root.
Go to the frontend folder:
cd frontend/front_m-main

Install frontend dependencies:
pnpm install

Create a .env file inside frontend/front_m-main:
VITE_API_BASE_URL=http://localhost:8000

Run the frontend:
pnpm run dev

Frontend will run at:
http://localhost:3000

If Vite starts on another port, use the URL shown in the terminal.

5. Machine Learning Setup
Open a new terminal from the project root.
Go to the ML folder:
cd ml

Create a virtual environment:
python -m venv venv

Activate the virtual environment.
Windows PowerShell
venv\Scripts\Activate.ps1

Windows CMD
venv\Scripts\activate.bat

Linux / macOS
source venv/bin/activate

Install ML dependencies:
pip install -r requirements.txt

Train the model:
python src/train.py

Evaluate the model:
python src/evaluate.py

Run scoring script:
python src/scoring.py

Generate SHAP explanations:
python src/shap_explainer.py


Running the Full Project
Start services in this order.
Terminal 1: Start Database
From project root:
docker compose -f docker/docker-compose.yml up -d


Terminal 2: Start Backend
cd backend
venv\Scripts\Activate.ps1
uvicorn app.main:app --reload

For Linux/macOS:
cd backend
source venv/bin/activate
uvicorn app.main:app --reload


Terminal 3: Start Frontend
cd frontend/front_m-main
pnpm run dev

Open the app:
http://localhost:3000


Useful Git Commands
Check current status:
git status

Add all files:
git add .

Commit changes:
git commit -m "your commit message"

Add GitHub remote:
git remote add origin https://github.com/KaranSJ22/xai-gig-score.git

Push to GitHub:
git branch -M main
git push -u origin main

For future pushes:
git add .
git commit -m "updated project"
git push


Important Files Not Included in Git
The following files and folders are ignored using .gitignore:
.env
venv/
__pycache__/
*.pyc
node_modules/
dist/
build/
ml/data/
ml/artifacts/
backend/app/ml/
*.pkl
*.joblib
*.csv

These files are ignored because they may contain secrets, generated files, large datasets, or machine-specific dependencies.

Environment Variables
Backend .env
Create this file inside the backend folder:
DATABASE_URL=postgresql://postgres:password@localhost:5432/gig_score_db
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

Frontend .env
Create this file inside:
frontend/front_m-main/.env

Add:
VITE_API_BASE_URL=http://localhost:8000


Common Issues and Fixes
pnpm is not recognized
Install pnpm globally:
npm install -g pnpm

Then check:
pnpm -v


PowerShell blocks pnpm or venv activation
Run this once in PowerShell:
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

Close PowerShell, reopen it, and try again.

Backend cannot connect to database
Make sure Docker database is running:
docker ps

If not running:
docker compose -f docker/docker-compose.yml up -d


Port already in use
For backend port 8000, stop the existing process or run on another port:
uvicorn app.main:app --reload --port 8001

For frontend, Vite will usually automatically select another port.

API Documentation
After starting the backend, open:
http://localhost:8000/docs

This provides an interactive API testing interface.

Project Summary
XAI Gig Score is a credit risk prediction system designed for gig workers and thin-file consumers. The system collects structured gig platform-related data, processes it through a machine learning model, generates a credit risk prediction, and provides explainable insights using SHAP-based explanations.
The main goal is to improve credit access for workers who may not have traditional salary slips, stable employment records, or strong credit history.

One thing I strongly recommend: rename your file from `Readme.md` to the standard GitHub format:

```bash
git mv Readme.md README.md

Then commit:
git add .
git commit -m "add complete README setup guide"
git push


