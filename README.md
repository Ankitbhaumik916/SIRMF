# Smart Irrigation Resource Management Farming (SIRMF)

AI-assisted smart farming platform with a Svelte dashboard, Express backend, weather-aware irrigation insights, and crop-stage image inference powered by a local SegFormer checkpoint (`best.pt`).

## What This Project Includes

- Svelte web app with authenticated multi-page workflow
- Express API with session-based auth and profile management
- Weather integration via OpenWeatherMap (with graceful fallback)
- Farm simulation and live farm-stat synchronization in UI
- Irrigation report generation from live farm-state snapshot
- Crop-stage detection endpoint that calls local Python inference
- ML training/inference utilities in `python_sim/`

## Tech Stack

- Frontend: Svelte 4, Vite, Tailwind CSS, Chart.js
- Backend: Node.js, Express, express-session
- Python/ML: PyTorch, Transformers (SegFormer), NumPy, pandas, scikit-learn, XGBoost
- Storage: JSON-based user store (`data/users.json`)

## Project Structure

```text
SEPM/
├─ src/                    # Svelte app
│  ├─ components/
│  ├─ pages/
│  ├─ stores/
│  └─ utils/
├─ python_sim/             # Python ML + crop stage inference scripts
├─ data/users.json         # User persistence
├─ public/                 # Static assets
├─ server.js               # Express API + SPA serving
├─ userStorage.js          # User persistence helpers
└─ README.md
```

## Prerequisites

- Node.js 18+
- npm 9+
- Python 3.8+
- (Recommended) virtual environment for Python dependencies

## Setup

### 1) Install JavaScript dependencies

```bash
npm install
```

### 2) Install Python dependencies

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Linux/Mac
source .venv/bin/activate

pip install numpy pandas scikit-learn xgboost torch torchvision transformers pillow
```

## Environment Variables

Create `.env` in project root as needed:

```env
OPENWEATHER_API_KEY=your_key_here
SESSION_SECRET=change_this_in_production
PYTHON_PATH=python
CROP_STAGE_MODEL_PATH=
```

Notes:
- If `OPENWEATHER_API_KEY` is missing, weather responses fall back to default/cached values.
- If `CROP_STAGE_MODEL_PATH` is empty, inference uses `best.pt` from project root.

## Run the App

### Development (frontend + backend together)

```bash
npm run dev
```

- Frontend (Vite): `http://localhost:5173`
- Backend (Express): `http://localhost:3000`

### Production build + server

```bash
npm run build
npm start
```

## Demo Login

- Username: `demo`
- Password: `demo123`

## Key API Endpoints

- `POST /api/auth/login`
- `POST /api/auth/signup`
- `POST /api/auth/logout`
- `GET /api/auth/user`
- `POST /api/auth/update-profile`
- `GET /api/dashboard/data`
- `GET /api/weather/:location`
- `GET /weather`
- `POST /api/crop-stage/predict` (requires authenticated session)

## Python Utilities

Inside `python_sim/`:

- `ml_setup.py`: end-to-end setup helper
- `ml_dataset_generation.py`: synthetic irrigation dataset generation
- `ml_train_model.py`: classifier/regressor training
- `ml_irrigation_predictor.py`: prediction utilities
- `test_ml_integration.py`: integration checks
- `crop_stage_inference.py`: base64 image crop-stage inference used by backend

Example:

```bash
python python_sim/test_ml_integration.py
```

## Available npm Scripts

- `npm run dev`: run Vite and Express concurrently
- `npm run dev:svelte`: run Vite only
- `npm run dev:server`: run Express server with watch
- `npm run build`: create production frontend build
- `npm run preview`: preview production frontend build
- `npm test`: run Vitest

## Notes

- Session auth is required for most app features and crop-stage prediction.
- User data is stored in `data/users.json`; migrate to a database for production workloads.
- Backend serves `dist/` and falls back to SPA routing for non-API routes.

## License

ISC
