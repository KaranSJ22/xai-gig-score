# XAI Gig Score — Comprehensive Project Summary

## 1. Project Overview

**XAI Gig Score** (branded in the UI as **GigRisk**) is an end-to-end **explainable AI-based credit scoring system** built specifically for **gig workers and thin-file consumers in India** — people who lack traditional salary slips, stable employment records, or conventional credit histories.

The system collects structured financial and behavioural data from gig platforms (Uber, Zomato, Swiggy, Rapido, Ola, Upwork, etc.), feeds it through a trained machine learning model, generates a **credit risk prediction** (score + default probability + risk level), and provides **SHAP-powered explainability** — surfacing which factors drove the score up or down.

**GitHub Repository:** `https://github.com/KaranSJ22/xai-gig-score`

---

## 2. Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 19, Vite 6, Tailwind CSS v4, React Router v7, Lucide React |
| Backend | FastAPI (Python), SQLAlchemy ORM, PostgreSQL, JWT Auth (python-jose), Passlib/bcrypt |
| Machine Learning | Scikit-learn (Random Forest), XGBoost, SHAP, Pandas, NumPy, Joblib |
| Database | PostgreSQL 15 (via Docker) |
| DevOps | Docker, Docker Compose |
| Package Manager (FE) | pnpm |

---

## 3. Repository Structure

```
Final/
├── backend/                  # FastAPI Python backend
│   ├── app/
│   │   ├── main.py           # App entry point, CORS, router registration
│   │   ├── config.py         # Pydantic settings (env vars)
│   │   ├── database.py       # SQLAlchemy engine + session factory
│   │   ├── deps.py           # DB session dependency injection
│   │   ├── models/           # SQLAlchemy ORM table models
│   │   ├── routes/           # FastAPI route handlers
│   │   ├── schemas/          # Pydantic request/response schemas
│   │   ├── services/         # Business logic layer
│   │   ├── utils/            # Security (JWT/bcrypt), validators
│   │   └── ml/               # Copied model artifacts (model.pkl, explainer.pkl, features.pkl)
│   ├── .env                  # Runtime env vars (gitignored)
│   └── requirements.txt      # Python dependencies
│
├── frontend/
│   └── front_m-main/
│       ├── src/
│       │   ├── App.jsx       # Root router with all routes
│       │   ├── main.jsx      # React DOM mount point
│       │   ├── index.css     # Global styles
│       │   ├── pages/        # Full-page React components
│       │   ├── components/   # Shared layout components
│       │   └── lib/          # API client, auth helpers, utils
│       ├── package.json
│       ├── vite.config.ts
│       └── .env              # VITE_API_URL
│
├── ml/                       # Standalone ML pipeline
│   ├── src/
│   │   ├── train.py          # Model training (RF + XGBoost)
│   │   ├── evaluate.py       # Metrics computation
│   │   ├── scoring.py        # Score/risk-band conversion logic
│   │   ├── shap_explainer.py # SHAP explainer creation & helpers
│   │   └── utils.py          # Dataset loading, feature columns, paths
│   ├── data/
│   │   └── final_dataset.csv # Training dataset (~15,000 rows, gitignored)
│   ├── artifacts/            # Saved model artifacts (gitignored)
│   │   ├── model.pkl         # Best trained model (~65 MB)
│   │   ├── explainer.pkl     # SHAP TreeExplainer (~87 MB)
│   │   ├── features.pkl      # Feature column order list
│   │   └── metrics.json      # Training evaluation results
│   └── requirements.txt
│
├── docker/
│   └── docker-compose.yml    # PostgreSQL 15 container definition
├── .gitignore
├── Readme.md                 # (empty placeholder)
└── readme.txt                # Full setup guide
```

---

## 4. Machine Learning Pipeline (`ml/`)

### 4.1 Dataset

- **File:** `ml/data/final_dataset.csv` (~5.3 MB, gitignored)
- **Total rows:** 15,000 (train/test split 80/20 → 12,000 train / 3,000 test)
- **Target column:** `default` (binary: 0 = no default, 1 = default)

### 4.2 Feature Set (24 features)

| Category | Features |
|---|---|
| **Demographics** | `age` |
| **Platform Activity** | `platform_tenure`, `avg_active_days`, `avg_hours`, `task_completion_rate`, `avg_rating`, `activity_stability` |
| **Financial / Transactions** | `wallet_txn_freq`, `inward_txn_freq`, `avg_income`, `income_volatility`, `income_growth`, `savings_ratio`, `avg_balance` |
| **Safety Buffers** | `has_insurance` (bool→float), `emergency_buffer` (bool→float) |
| **Debt & Credit** | `loan_utilization`, `fixed_emi_burden_ratio`, `credit_inquiries` |
| **Payment Behaviour** | `delay_score`, `recent_payment_delays_90`, `utility_delay_score`, `recent_missed_rent_3m`, `rent_consistency_ratio` |

### 4.3 Model Training (`ml/src/train.py`)

- Trains two candidate models: **Random Forest** (300 estimators, `class_weight="balanced"`) and **XGBoost** (300 estimators, `lr=0.05`, `max_depth=6`)
- Best model selected by **ROC-AUC then F1 score**
- Artifacts saved: `model.pkl`, `features.pkl`, `metrics.json`, `explainer.pkl`

### 4.4 Evaluation Results (`ml/artifacts/metrics.json`)

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| **Random Forest** ✅ (selected) | 75.67% | 61.48% | 39.67% | 48.23% | **76.66%** |
| XGBoost | 75.93% | 63.26% | 37.57% | 47.14% | 76.18% |

Random Forest was selected (higher ROC-AUC = 76.66%).

### 4.5 Scoring Logic (`ml/src/scoring.py`)

```
credit_score = 300 + (1.0 - default_probability) × 600
Range: [300, 900]

Risk Bands:
  score >= 750 → "Low"
  score >= 600 → "Medium"
  score <  600 → "High"
```

### 4.6 SHAP Explainability (`ml/src/shap_explainer.py`)

- Uses `shap.TreeExplainer` for Random Forest / XGBoost models
- Generates per-feature SHAP contributions for each prediction
- Top-3 positive factors (features increasing risk) and top-3 negative factors (features reducing risk) are surfaced to the user

---

## 5. Backend (`backend/`)

### 5.1 Entry Point (`app/main.py`)

- Creates a FastAPI app titled **"Gig Credit Backend"**
- CORS configured to allow `http://localhost:3000` and `http://127.0.0.1:3000`
- Auto-creates all DB tables on startup via `Base.metadata.create_all()`
- Registers 6 routers: `auth`, `pan`, `platforms`, `predict`, `loans`, `dashboard`

### 5.2 Configuration (`app/config.py`)

Uses `pydantic-settings` to load from `.env`:

| Variable | Default |
|---|---|
| `DATABASE_URL` | `postgresql://postgres:password@localhost:5432/gig_credit` |
| `SECRET_KEY` | `change-this-in-production` |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |

### 5.3 Database (`app/database.py`)

- SQLAlchemy `create_engine` with `pool_pre_ping=True`
- `SessionLocal` factory (no autocommit, no autoflush)
- `Base = declarative_base()` — all models inherit from this

### 5.4 Data Models (`app/models/`)

#### `User` (table: `users`)
| Column | Type | Notes |
|---|---|---|
| `id` | Integer PK | Auto |
| `name` | String(100) | |
| `email` | String(150) | Unique, indexed |
| `password_hash` | String(255) | bcrypt |
| `created_at` | DateTime | Server default |
| Relationships | | `pan_details` (1:1), `platforms` (1:N), `predictions` (1:N), `loans` (1:N) — all cascade delete |

#### `PanDetails` (table: `pan_details`)
| Column | Type | Notes |
|---|---|---|
| `id` | Integer PK | |
| `user_id` | FK → users | Unique constraint |
| `pan_number` | String(10) | Unique, format: `ABCDE1234F` |
| `is_verified` | Boolean | Mock-set to `True` on submit |
| `created_at` | DateTime | |

#### `PlatformData` (table: `platform_data`)
Stores all 24 ML features + metadata per connected platform per user. Key columns:
- `platform_name` (String 50)
- All 24 feature columns as `Float` or `Boolean`
- `created_at`

#### `Prediction` (table: `predictions`)
| Column | Type |
|---|---|
| `credit_score` | Float |
| `default_probability` | Float |
| `risk_level` | String(20) |
| `positive_factors` | ARRAY(String) |
| `negative_factors` | ARRAY(String) |
| `created_at` | DateTime |

#### `Loan` (table: `loans`)
| Column | Type | Notes |
|---|---|---|
| `bank_name` | String(100) | |
| `amount` | Float | |
| `status` | String(20) | Default: `"Pending"` |

### 5.5 API Routes (`app/routes/`)

#### `/auth` — Authentication
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register user, return JWT token |
| POST | `/auth/login` | Verify credentials, return JWT token |
| GET | `/auth/me` | Return current authenticated user info |

Auth uses **HTTP Bearer token** scheme. JWT payload contains `sub` (user ID string).

#### `/pan` — PAN Verification
| Method | Endpoint | Description |
|---|---|---|
| POST | `/pan/submit` | Submit & mock-verify PAN number |
| GET | `/pan/` | Get current PAN status |

PAN validation regex: `^[A-Z]{5}[0-9]{4}[A-Z]$`

#### `/platforms` — Gig Platform Connection
| Method | Endpoint | Description |
|---|---|---|
| POST | `/platforms/connect` | Connect a platform (generates mock data) |
| GET | `/platforms/` | List all connected platforms |

Supported platforms: `uber`, `zomato`, `swiggy`, `rapido`, `freelance`, `delivery`, `ride-hailing`, `ola`, `upwork`

#### `/predict` — Credit Score Prediction
| Method | Endpoint | Description |
|---|---|---|
| POST | `/predict/` | Run ML prediction for current user |

#### `/loans` — Loan Management
| Method | Endpoint | Description |
|---|---|---|
| POST | `/loans/apply` | Submit a loan application |
| GET | `/loans/` | List all user loans |

#### `/dashboard` — Aggregated Dashboard
| Method | Endpoint | Description |
|---|---|---|
| GET | `/dashboard/` | Returns user info, PAN status, platform summary, latest prediction, prediction history (last 5), loans |

### 5.6 Services (`app/services/`)

#### `mock_data.py` — Platform Data Simulator
- Generates realistic randomised values for all 24 ML features per platform
- Platform-specific income/hours ranges (e.g., Uber: ₹18K–42K/month; Freelance: ₹12K–50K/month)
- Used because real platform OAuth integration is not implemented

#### `feature_engineering.py` — Feature Aggregation
- `build_features()`: Averages feature values across all connected platforms
- `attach_numeric_flags()`: Converts `has_insurance` / `emergency_buffer` booleans to floats

#### `model_service.py` — ML Model Inference
- Lazy-loads `model.pkl` and `features.pkl` from `app/ml/` on first call
- `predict_default_probability()`: Returns `(probability, predicted_class)` tuple

#### `scoring_service.py` — Orchestration
1. Fetches all user platform records
2. Calls `attach_numeric_flags()` on each
3. Calls `build_features()` to aggregate
4. Calls `predict_default_probability()` → gets probability
5. Converts to credit score (`300 + (1 - p) × 600`)
6. Determines risk level (Low/Medium/High)
7. Calls `explain_prediction()` → SHAP factors
8. Saves `Prediction` record to DB
9. Returns full result dict

#### `explain_service.py` — SHAP Explanations
- Lazy-loads `explainer.pkl` and `features.pkl`
- Calls `explainer.shap_values(X)` and normalises output via `_extract_1d_shap_values()` (handles various SHAP output shapes)
- Returns top-3 positive factors ("X increased the predicted risk") and top-3 negative factors ("X reduced the predicted risk")

### 5.7 Utilities (`app/utils/`)

- **`security.py`**: `hash_password()`, `verify_password()` (bcrypt via passlib), `create_access_token()`, `decode_access_token()` (JWT via python-jose). Passwords truncated to 72 chars (bcrypt limit).
- **`validators.py`**: `validate_pan()` — regex match for Indian PAN format.
- **`deps.py`**: `get_db()` generator — yields SQLAlchemy session and closes it in `finally`.

---

## 6. Frontend (`frontend/front_m-main/`)

### 6.1 Tech Stack
- **React 19** + **Vite 6** + **TypeScript config** (but `.jsx` files)
- **Tailwind CSS v4** (via `@tailwindcss/vite` plugin)
- **React Router v7** (BrowserRouter)
- **Lucide React** icons
- **pnpm** package manager
- Dev server runs at `http://localhost:3000`

### 6.2 Routing (`src/App.jsx`)

| Route | Component | Auth Required |
|---|---|---|
| `/` | `LandingPage` | No |
| `/login` | `LoginPage` | No |
| `/register` | `RegisterPage` | No |
| `/dashboard` | `Dashboard` | Yes (AuthGuard) |
| `/pan` | `PANPage` | Yes |
| `/connect` | `ConnectPage` | Yes |
| `/predict` | `PredictPage` | Yes |
| `/loans` | `LoansPage` | Yes |
| `*` | Redirect to `/` | — |

### 6.3 Auth Flow (`src/lib/auth.js`)

JWT token stored in `localStorage` under key `"token"`. `AuthGuard.jsx` checks `isAuthenticated()` and redirects to `/login` if no token present. On 401 response, `api.js` automatically redirects to `/login`.

### 6.4 API Client (`src/lib/api.js`)

- Base URL: `import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'`
- Attaches `Authorization: Bearer <token>` header on every request if token exists
- Throws `Error(data.detail)` on non-2xx responses
- Auto-redirects to `/login` on 401

### 6.5 Pages

#### `Landing.jsx` — Public landing page
- Brand hero: "GigRisk — Decentralized Credit Scoring for the Gig Economy"
- Three feature callouts: Platform Sync, Dynamic Prediction, Bank Connectivity
- CTA buttons: "Get Started" → `/register`, "Sign In" → `/login`

#### `Login.jsx` / `Register.jsx`
- Form-based auth pages
- POST to `/auth/login` or `/auth/register`
- On success, save JWT token and redirect to `/dashboard`

#### `Dashboard.jsx`
- Fetches `/dashboard/` on mount
- Displays: Credit Score (gauge bar, out of 850), Risk Level badge, Default Probability %, Monthly Avg Income, Avg Platform Rating
- Active Credit Lines table (bank, amount, date, status)
- Impact Analysis panel (SHAP positive & negative factors)
- Score History table (last 5 predictions: score, risk level, date)

#### `Connect.jsx` — Platform Integration
- Lists 6 platforms: Uber, Zomato, Swiggy, Rapido, Upwork, Ola (each with brand colour)
- Fetches `/platforms/` to show already-connected platforms (green "Active" badge)
- "Connect" button → POST `/platforms/connect` with `{ platform_name }`
- "Missing a Platform?" section at bottom

#### `PAN.jsx` — Identity Verification
- Input for 10-character PAN number (auto-uppercase, regex enforced client-side)
- POST `/pan/submit` on form submit (mock-verified instantly)
- Shows "Identity Verified" or "Awaiting Input" status badge

#### `Predict.jsx` — Risk Calibration Engine
- Single "Run Analysis Engine" button → POST `/predict/`
- Shows Projected Score, Risk Magnitude, Positive Drivers, Risk Constraints panels
- Processing steps displayed as decorative list (not real-time, UI only)

#### `Loans.jsx` — Credit Liquidity
- 3 hardcoded pre-approved offers (HDFC ₹1.5L @ 8.5%, ICICI ₹2L @ 9.2%, IDFC ₹50K @ 10.5%)
- "Fast Apply" pre-fills form fields
- Form: bank name + amount → POST `/loans/apply`
- Active Disbursements table fetched from GET `/loans/`

### 6.6 Shared Components

| Component | Purpose |
|---|---|
| `AuthGuard.jsx` | Wraps protected routes; redirects unauthenticated users to `/login` |
| `DashboardLayout.jsx` | Wraps all authenticated pages with `<Sidebar>` + content area |
| `Sidebar.jsx` | Fixed left nav with links: Dashboard, Platform Sync, Risk Factors, Loan Status; Logout button |
| `Header.jsx` | Top header bar (user info, possibly greeting) |

---

## 7. Infrastructure (`docker/`)

### `docker-compose.yml`
```yaml
services:
  postgres:
    image: postgres:15
    container_name: gig_credit_postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: gig_credit
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5433:5432"   # host 5433 → container 5432
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

> **Note:** The compose file exposes PostgreSQL on host port **5433**, but the backend `.env` default points to port `5432`. This requires either updating the backend `DATABASE_URL` to use `5433` or adjusting the compose port mapping.

---

## 8. Environment Variables

### Backend (`backend/.env`)
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/gig_credit
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (`frontend/front_m-main/.env`)
```
VITE_API_URL=http://localhost:8000
```

---

## 9. Data Flow — End to End

```
User (Browser)
    │
    │  1. Register / Login → JWT token stored in localStorage
    │
    ▼
React Frontend (localhost:3000)
    │
    │  2. Connect Platform → POST /platforms/connect
    │
    ▼
FastAPI Backend (localhost:8000)
    │
    │  3. generate_mock_platform_features() → 24 randomised features
    │  4. Save PlatformData to PostgreSQL
    │
    ▼
PostgreSQL (localhost:5433)
    │
    │  5. User triggers POST /predict/
    │
    ▼
FastAPI Backend
    │
    │  6. Fetch all PlatformData for user
    │  7. Aggregate features (average across platforms)
    │  8. Load model.pkl + features.pkl (lazy, cached)
    │  9. model.predict_proba(X) → default_probability
    │ 10. credit_score = 300 + (1 - p) × 600
    │ 11. risk_level = Low / Medium / High
    │ 12. Load explainer.pkl, run SHAP → top-3 positive & negative factors
    │ 13. Save Prediction record to DB
    │
    ▼
React Frontend
    │ 14. Display: Credit Score, Risk Level, Default Probability,
    │            Positive Drivers, Risk Constraints
    ▼
User sees their GigRisk Score™
```

---

## 10. ML Artifacts (Pre-trained)

The following files exist in **two places** (both copies are gitignored):

| Path | Size | Purpose |
|---|---|---|
| `ml/artifacts/model.pkl` | ~65 MB | Trained Random Forest classifier |
| `ml/artifacts/explainer.pkl` | ~87 MB | SHAP TreeExplainer for Random Forest |
| `ml/artifacts/features.pkl` | ~452 B | Python list of 24 feature column names |
| `ml/artifacts/metrics.json` | ~1.5 KB | Training evaluation metrics |
| `backend/app/ml/model.pkl` | ~65 MB | Copy used by the running backend |
| `backend/app/ml/explainer.pkl` | ~87 MB | Copy used by the running backend |
| `backend/app/ml/features.pkl` | ~452 B | Copy used by the running backend |

---

## 11. Key Design Decisions

| Decision | Rationale |
|---|---|
| **Mock platform data** | Real gig platform APIs (Uber, Zomato) require business-level OAuth partnerships. Mock generation simulates realistic distributions per platform type. |
| **SHAP TreeExplainer** | Efficient for tree-based models. Provides model-faithful explanations of individual predictions. |
| **PAN mock-verification** | Real PAN verification requires NSDL/UTI API integration. Marked as `True` immediately on submit. |
| **Score range 300–900** | Mirrors India's CIBIL score range, making it familiar to lenders. |
| **Random Forest selected over XGBoost** | Marginally higher ROC-AUC (76.66% vs 76.18%). |
| **JWT in localStorage** | Simpler implementation. For production, HttpOnly cookies would be more secure. |
| **Averaged features across platforms** | Multi-platform users get a single aggregated feature vector, preventing model re-training per platform. |

---

## 12. Known Issues / Gaps

1. **Port mismatch:** Docker exposes PostgreSQL on `5433`, but backend default `DATABASE_URL` uses `5432`.
2. **Loan status:** All loans are permanently `"Pending"` in the DB — no status update mechanism exists.
3. **Loan offers hardcoded:** HDFC/ICICI/IDFC offers in `Loans.jsx` are static UI elements, not fetched from any API.
4. **`ml/src/utils.py` syntax error:** Line 72 has an extra leading space (`     unique_targets = ...`) causing an `IndentationError`. The ML pipeline will fail to run without fixing this.
5. **SHAP code commented out:** `explain_service.py` and `model_service.py` contain two full sets of commented-out legacy implementations alongside the active code — indicating iterative debugging.
6. **PAN page navigation:** The `/pan` route exists and is linked from the sidebar's PAN section but `Sidebar.jsx` does not list it in `navItems` — users must navigate directly.
7. **No real platform OAuth:** All platform data is randomly generated via `mock_data.py`.
8. **No email verification:** User registration is immediate with no email confirmation step.
9. **Gemini API key in vite.config.ts:** `process.env.GEMINI_API_KEY` is exposed via `define` in Vite config — suggests AI features may be partially planned but not implemented in any page.

---

## 13. How to Run the Full Project

### Prerequisites
- Git, Python 3.10+, Node.js, npm, pnpm, Docker Desktop

### Step 1 — Start Database
```bash
docker compose -f docker/docker-compose.yml up -d
```
> Then update `backend/.env` to use port `5433` to match Docker.

### Step 2 — Start Backend
```bash
cd backend
python -m venv venv
venv\Scripts\Activate.ps1        # Windows PowerShell
pip install -r requirements.txt
uvicorn app.main:app --reload
# Runs at http://localhost:8000
# Swagger UI at http://localhost:8000/docs
```

### Step 3 — Start Frontend
```bash
cd frontend/front_m-main
pnpm install
pnpm run dev
# Runs at http://localhost:3000
```

### Step 4 — (Optional) Retrain ML Model
```bash
cd ml
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/train.py
# Then copy artifacts to backend/app/ml/
```

---

## 14. Dependencies Summary

### Backend (`backend/requirements.txt`)
```
fastapi, uvicorn[standard], sqlalchemy, psycopg2-binary,
pydantic, pydantic-settings, python-jose[cryptography],
passlib[bcrypt], bcrypt==4.0.1, email-validator,
python-multipart, joblib, scikit-learn, shap, numpy, pandas
```

### ML (`ml/requirements.txt`)
```
pandas, numpy, scikit-learn, xgboost, shap, joblib, matplotlib, seaborn
```

### Frontend (`package.json` dependencies)
```
react@19, react-dom@19, react-router-dom@7, vite@6,
@vitejs/plugin-react, tailwindcss@4, @tailwindcss/vite,
lucide-react, motion, clsx, tailwind-merge,
@google/genai, dotenv, express
```
