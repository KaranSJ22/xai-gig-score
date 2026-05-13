# 🚀 GigScore: Institutional-Grade XAI Credit Intelligence

**GigScore** is an explainable AI-based credit scoring ecosystem designed for gig workers and thin-file consumers. It bridges the gap between digital platform performance and institutional credit trust.

![Version](https://img.shields.io/badge/version-1.2.0-black?style=for-the-badge)
![Tech](https://img.shields.io/badge/Stack-FastAPI%20|%20React%20|%20PostgreSQL-blue?style=for-the-badge)
![License](https://img.shields.io/badge/Intelligence-Explainable_AI-green?style=for-the-badge)

---

## 🌟 Key Features

### 🧠 Intelligence Engine & XAI
Our "XAI Engine" processes behavioral signals from connected gig platforms (Uber, Swiggy, Zomato) to predict creditworthiness. 
- **Explainable Decisions**: Every score includes a **SHAP (SHapley Additive exPlanations)** breakdown, showing exactly which factors (active days, income stability, discipline) impacted the score.
- **Confidence Scoring**: A statistical reliability metric (0.0 - 1.0) based on data density, providing lenders with transparency into the AI's certainty.

### 👥 Dual-Portal Ecosystem
- **Borrower Portal (Port 3000)**: A premium dashboard for workers to sync platforms, view their GigScore, understand their risk drivers, and apply for loans.
- **Lender Console (Port 3001)**: An institutional interface for credit analysts to review applications, audit XAI metrics, and manage risk parameters.

### 🛡️ Privacy & Control
- **Dynamic Sync Control**: Borrowers can "Stop Sync" at any time, which immediately purges their behavioral data from the active signal cache.
- **Identity Verification**: Integrated PAN protocol and RSA-4096 security for institutional-grade integrity.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React, Vite, TailwindCSS, Lucide Icons |
| **Backend** | FastAPI (Python 3.10+), SQLAlchemy, JWT, Pydantic |
| **Intelligence** | Scikit-Learn (Random Forest), SHAP, Pandas, NumPy |
| **Storage** | PostgreSQL (Dockerized) |
| **Security** | RSA-4096, BCrypt Hashing, Role-Based Access Control (RBAC) |

---

## 📂 Project Structure

```txt
xai-gig-score/
├── backend/                # FastAPI Application & XAI Engine Logic
│   ├── app/
│   │   ├── ml/             # Serialized Model Artifacts (.pkl)
│   │   ├── routes/         # API Endpoints (Auth, Lender, User)
│   │   ├── services/       # Business Logic (Scoring, XAI, Feature Eng)
│   │   └── main.py         # App Entry Point
├── frontend/
│   ├── frontend_user/      # Borrower Dashboard (Port 3000)
│   └── frontend_lender/    # Institutional Console (Port 3001)
├── docker/                 # Infrastructure (PostgreSQL)
└── ml/                     # ML Research & Notebooks
```

---

## 🚀 Quick Start Guide

### 1. Database Initialization
Start the PostgreSQL environment using Docker Compose:
```bash
docker compose -f docker/docker-compose.yml up -d
```

### 2. XAI Engine (Backend) Setup
```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --port 8001 --host 0.0.0.0 --reload
```

### 3. Portal Deployment
Open two terminals for the dual portals:

**Borrower Portal:**
```bash
cd frontend/frontend_user
npm install
npm run dev
```

**Lender Console:**
```bash
cd frontend/frontend_lender
npm install
npm run dev
```

---

## 📈 XAI Engine Metadata (v1.2)
- **Primary Algorithm**: Random Forest Ensemble
- **Explainability Layer**: KernelExplainer (SHAP)
- **Risk Range**: 300 (High Risk) - 850 (Institutional Trust)
- **Confidence Metric**: Dynamic (Platform Density Based)

---

## 🛡️ Security & Compliance
- **CORS Configuration**: Fully optimized for cross-origin portal orchestration.
- **Audit Trail**: Every lender decision (Approval/Rejection) is timestamped and recorded with institutional justification.
- **Data Minimization**: Enforces strict PII (Personally Identifiable Information) handling through PAN-only verification.

---

Designed with ❤️ for the Indian Gig Economy.
