# TrustBridge AI: Deployment Guide

This guide provides setup and deployment instructions for the TrustBridge AI platform, covering the FastAPI backend, Next.js frontend, PostgreSQL database setup, environment variables, and local testing.

---

## 1. Environment Variables Configuration

Both the frontend and backend require specific variables to handle connections, security, and integration.

### 1.1 Backend Environment Variables (`backend/.env`)
Create a file named `.env` in the `backend/` directory:
```env
# Database Settings (Local SQLite fallback or PostgreSQL for Production)
DATABASE_URL=postgresql://db_user:db_password@host:port/db_name

# Security Settings
SECRET_KEY=generate-a-secure-random-32-byte-hex-string
ACCESS_TOKEN_EXPIRE_MINUTES=60
ALLOWED_ORIGINS=http://localhost:3000,https://trustbridge.vercel.app

# AI Layer
GEMINI_API_KEY=AIzaSyYourActualGoogleGeminiAPIKeyHere
```

### 1.2 Frontend Environment Variables (`frontend/.env.local`)
Create a file named `.env.local` in the `frontend/` directory:
```env
# Backend API Integration
NEXT_PUBLIC_API_URL=https://trustbridge-api.onrender.com
```

---

## 2. Backend Deployment (Render)

Render is used to host the FastAPI application and the PostgreSQL database.

### 2.1 Set Up PostgreSQL Database on Render
1.  Log in to the [Render Dashboard](https://dashboard.render.com).
2.  Click **New +** and select **PostgreSQL**.
3.  Fill in the configurations:
    *   **Name**: `trustbridge-db`
    *   **Region**: Select the closest region.
    *   **Database**: `trustbridge`
    *   **User**: `trustbridge_admin`
4.  Select the **Free** tier (or appropriate tier for production).
5.  Click **Create Database**.
6.  Once active, copy the **Internal Database URL** (for services hosted on Render) or **External Database URL** (for local testing/external connections).

### 2.2 Deploy FastAPI Application
1.  Click **New +** and select **Web Service**.
2.  Connect your Git repository containing the TrustBridge AI codebase.
3.  Configure the Web Service:
    *   **Name**: `trustbridge-api`
    *   **Region**: Select the same region as the database.
    *   **Branch**: `main`
    *   **Root Directory**: `backend`
    *   **Runtime**: `Python`
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4.  Add the **Environment Variables** in the Render UI:
    *   `DATABASE_URL`: Set this to your PostgreSQL Connection String. (Make sure to change `postgres://` to `postgresql://` if SQLAlchemy requires it).
    *   `GEMINI_API_KEY`: Paste your Gemini API key.
5.  Click **Advanced** -> Check **Auto Deploy** (optional).
6.  Click **Create Web Service**.

---

## 3. Frontend Deployment (Vercel)

Vercel is used to host the Next.js frontend with Tailwind CSS and ShadCN UI.

### 3.1 Vercel Deployment Steps
1.  Log in to the [Vercel Dashboard](https://vercel.com).
2.  Click **Add New...** and select **Project**.
3.  Import your Git repository.
4.  Configure the Project settings:
    *   **Project Name**: `trustbridge-web`
    *   **Framework Preset**: `Next.js`
    *   **Root Directory**: `frontend`
5.  Configure Build & Development Settings (Defaults are correct):
    *   **Build Command**: `npm run build`
    *   **Output Directory**: `.next`
    *   **Install Command**: `npm install`
6.  Add **Environment Variables**:
    *   `NEXT_PUBLIC_API_URL`: Paste the live URL of your Render backend service (e.g. `https://trustbridge-api.onrender.com`).
7.  Click **Deploy**.
8.  Vercel will build the static assets, optimize images, and deploy serverless functions. Once finished, it will output a production domain (e.g., `https://trustbridge-web.vercel.app`).

---

## 4. Database Setup & Migrations

If deploying with PostgreSQL in production, SQLAlchemy and the FastAPI lifespan handler will automatically initialize database tables on startup.

### 4.1 Automated Initialization
The backend uses a FastAPI `lifespan` event handler (`backend/app/main.py`):
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initializes database tables from both modules
    async with async_engine.begin() as conn:
        await conn.run_sync(async_base.metadata.create_all)
        
    init_db()  # Krrish's sync DB initialization
    try:
        seed_database()  # Seeds alternative sample datasets
    except Exception:
        pass
    yield
```

---

## 5. Local Development Commands

### 5.1 Run Backend Locally
Navigate to the backend directory and run:
```bash
# Navigate to backend
cd backend

# Create Virtual Environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Run Uvicorn Development Server
uvicorn app.main:app --reload --port 8000
```
The local API documentation will be available at `http://127.0.0.1:8000/docs` (Swagger UI).

### 5.2 Run Frontend Locally
Navigate to the frontend directory and run:
```bash
# Navigate to frontend
cd frontend

# Install Packages
npm install

# Run Vite/Next.js Dev Server
npm run dev
```
The web application will open on `http://localhost:3000`.
