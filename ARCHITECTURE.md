# SIRMF Architecture (Current)

Last updated: 2026-04-15

This document describes the architecture currently implemented in the codebase.

## 1. System Overview

SIRMF is a full-stack smart farming application with:
- A Svelte single-page frontend (Vite dev server)
- An Express backend API with session authentication
- File-based user persistence (`data/users.json`)
- Python crop-stage inference invoked from Node via child process
- A simulation experience embedded through `impl1.html`

Runtime topology:

```text
Browser (Svelte SPA on :5173)
  -> Vite proxy
    -> Express API on :3000
      -> OpenWeatherMap API (optional, via env key)
      -> Python process (crop_stage_inference.py)
      -> JSON persistence (data/users.json)
```

## 2. Frontend Architecture

### 2.1 App Shell and Navigation

- Entry: `src/main.js`
- Root app: `src/App.svelte`

`App.svelte` uses local state (`currentPage`) instead of an external router. Navigation events are emitted from `Sidebar.svelte` and handled centrally.

Page-level composition:
- Auth pages: Login, Signup
- Authenticated pages: Dashboard, Weather, IrrigationReport, CropStageDetection, SoilCheck, FarmInfo, Profile, Settings

### 2.2 Frontend State Stores

- `src/stores/authStore.js`
  - Session-aware auth state
  - API calls: login, signup, logout, checkAuth
  - Uses `credentials: include` to persist session cookies

- `src/stores/weatherStore.js`
  - Fetches weather from `GET /api/weather/:location`
  - Stores weather payload, loading/error, timestamp, and searched location

- `src/stores/farmStatsStore.js`
  - Shared in-app farm metrics (avg moisture, avg health, farms needing irrigation)
  - Consumed by SoilCheck, Profile, and IrrigationReport

- `src/stores/i18nStore.js`
  - Language dictionaries and translation helper `t(...)`
  - Persists language in localStorage

### 2.3 Farm Simulation Path (Current)

`FarmInfo.svelte` currently embeds the simulator UI through an iframe:

```text
FarmInfo.svelte
  -> <iframe src="/impl1">
    -> backend route GET /impl1
      -> serves impl1.html
```

Notes:
- Vite proxy forwards `/impl1` to the backend in development.
- `impl1.html` is a standalone simulator/dashboard page with its own UI logic.

### 2.4 Legacy In-App Simulation Module

The repository still includes an in-app simulation module:
- `src/components/FarmingSimulation.svelte`
- `src/utils/farmingSimulation.js`

This module supports callbacks (`setFarmStatsCallback`, `setFarmInfoCallback`) for direct store integration, but the current `FarmInfo.svelte` path uses iframe embedding instead.

## 3. Backend Architecture

### 3.1 Server and Middleware

Main server: `server.js`

Core middleware:
- `cors` with frontend origin `http://localhost:5173`
- `express.json({ limit: '20mb' })`
- `express.urlencoded({ extended: true, limit: '20mb' })`
- `express-session` for cookie-based auth/session data

### 3.2 Persistence Layer

Module: `userStorage.js`

Storage model:
- File-backed JSON object at `data/users.json`
- Keyed by username
- Helper functions: load, save, create, update, lookup

Security note:
- Password hashing currently uses base64 encoding (`hashPassword`) and is not production-grade cryptography.

### 3.3 API Surface

Auth endpoints:
- `POST /api/auth/login`
- `POST /api/auth/signup`
- `POST /api/auth/logout`
- `GET /api/auth/user`
- `POST /api/auth/update-profile`

Data endpoints:
- `GET /api/dashboard/data` (session required)
- `GET /api/weather/:location`
- `GET /weather` (enhanced weather payload with cache/offline fallback)

Simulation and inference endpoints:
- `GET /impl1` -> serves `impl1.html`
- `GET /simulation` -> serves `sirmf_ml.html` (if present)
- `POST /api/crop-stage/predict` (session required)

Static serving and SPA fallback:
- Serves built frontend from `dist/`
- Wildcard route returns `dist/index.html` for non-API paths

## 4. ML and Python Inference Bridge

### 4.1 Crop Stage Flow

Frontend (`CropStageDetection.svelte`):
1. User uploads image
2. Image converted to base64 in browser
3. Sends `POST /api/crop-stage/predict` with `{ imageBase64 }`

Backend (`server.js`):
1. Verifies session and crop profile
2. Spawns Python process (`python_sim/crop_stage_inference.py`)
3. Sends JSON payload via stdin
4. Parses JSON response from stdout
5. Returns prediction to frontend

Python (`python_sim/crop_stage_inference.py`):
- Loads SegFormer checkpoint (default `best.pt` unless overridden)
- Preprocesses image
- Runs segmentation
- Derives stage via rule-based logic from mask features
- Returns stage, confidence, model metadata, optional warning note

### 4.2 Configurable Runtime Inputs

Environment variables used by backend:
- `OPENWEATHER_API_KEY`
- `SESSION_SECRET`
- `PYTHON_PATH`
- `CROP_STAGE_MODEL_PATH`

## 5. Data and Control Flows

### 5.1 Authentication Flow

```text
App mount
  -> checkAuth() in authStore
    -> GET /api/auth/user
      -> session present? yes: authenticated state
      -> no: login/signup state
```

### 5.2 Dashboard Flow

```text
Dashboard page mount
  -> GET /api/dashboard/data
    -> backend combines crop profile + weather + computed metrics
      -> frontend renders cards, charts, and recommendations
```

### 5.3 Weather Flow

```text
Weather page search
  -> weatherStore.fetchWeatherData(location)
    -> GET /api/weather/:location
      -> geocode + weather lookup
      -> return normalized weather payload
```

### 5.4 Irrigation Report Flow

```text
Generate Report click
  -> snapshot farmStatsStore (at click time)
  -> fetch dashboard data (5s timeout)
  -> buildIrrigationReport(dashboardData, liveFarmStats)
  -> render performance, deficits, recommendations
```

## 6. Build and Runtime Model

Development mode:
- `npm run dev`
- Runs Vite (`:5173`) and Express (`:3000`) concurrently
- Vite proxies `/api`, `/impl1`, `/simulation`

Production mode:
- `npm run build`
- `npm start`
- Express serves API and `dist/` static bundle

## 7. Key Design Characteristics

- Session-first architecture: backend remains source of auth truth
- Hybrid intelligence stack: JS UI + Node orchestration + Python ML
- Graceful weather degradation: cached/default responses when API unavailable
- Modular stores for frontend state
- Dual simulation implementations: iframe-based standalone sim (active) and Svelte-embedded sim module (available)

## 8. Known Architectural Gaps

- Password hashing should be replaced with a secure algorithm (for example bcrypt/argon2).
- JSON file persistence does not provide transactional guarantees or multi-instance safety.
- Iframe simulator path is isolated from Svelte stores unless explicit bridge messaging is added.
- `/simulation` route references `sirmf_ml.html`; ensure file exists if route is used.

## 9. File Map (Primary)

Frontend core:
- `src/main.js`
- `src/App.svelte`
- `src/components/Sidebar.svelte`
- `src/pages/Dashboard.svelte`
- `src/pages/Weather.svelte`
- `src/pages/IrrigationReport.svelte`
- `src/pages/CropStageDetection.svelte`
- `src/pages/SoilCheck.svelte`
- `src/pages/Profile.svelte`
- `src/pages/FarmInfo.svelte`
- `src/pages/Settings.svelte`

Stores and utilities:
- `src/stores/authStore.js`
- `src/stores/weatherStore.js`
- `src/stores/farmStatsStore.js`
- `src/stores/i18nStore.js`
- `src/utils/irrigationReporting.js`
- `src/utils/farmingSimulation.js`

Backend and persistence:
- `server.js`
- `userStorage.js`
- `data/users.json`

Python ML:
- `python_sim/crop_stage_inference.py`
- `python_sim/ml_setup.py`
- `python_sim/ml_train_model.py`
- `python_sim/ml_irrigation_predictor.py`
- `python_sim/test_ml_integration.py`
- `best.pt`
