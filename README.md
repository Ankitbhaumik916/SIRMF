# 🌾 Smart Irrigation Resource Management Farming (SIRMF)

A **professional, full-stack smart farming platform** designed for precision irrigation management and crop monitoring. SIRMF combines a modern web dashboard with AI-powered crop stage detection to help farmers optimize water usage, monitor farm health, and make data-driven irrigation decisions.

**Version:** 2.0.0 | **Status:** Production Ready ✅

---

## 🎯 Overview

SIRMF provides an integrated system for farmers to:
- 📊 **Monitor Farm Health**: Real-time soil moisture, temperature, and humidity tracking
- 🌦️ **Weather-Aware Irrigation**: Integration with OpenWeatherMap for location-based weather insights
- 🌾 **Crop Stage Detection**: AI-powered image analysis using deep learning (SegFormer model)
- 📈 **Analytics & Reporting**: Generate irrigation reports and view farm statistics
- 💧 **Smart Irrigation**: Get automated recommendations based on weather and crop requirements
- 🛠️ **Multi-Crop Support**: Built-in data for Tomato, Rice, Wheat, Corn, Sugarcane, Cotton, Potato, Onion

---

## 📋 Table of Contents

1. [Quick Start](#-quick-start)
2. [Tech Stack](#-tech-stack)
3. [Project Structure](#-project-structure)
4. [Features](#-features)
5. [Setup & Installation](#-setup--installation)
6. [Running the Application](#-running-the-application)
7. [API Documentation](#-api-documentation)
8. [Architecture](#-architecture)
9. [Configuration](#-configuration)
10. [Demo & Testing](#-demo--testing)
11. [Development Workflow](#-development-workflow)
12. [Troubleshooting](#-troubleshooting)

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ and **npm** 9+
- **Python** 3.8+ with pip
- Modern web browser
- (Optional) OpenWeatherMap API key for live weather

### 30-Second Setup

```bash
# Install dependencies
npm install

# Set up Python environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate    # Linux/Mac
pip install numpy pandas scikit-learn xgboost torch torchvision transformers pillow

# Start the app
npm run dev
```

Visit `http://localhost:5173` and log in with:
- **Username:** `demo`
- **Password:** `demo123`

---

## 🛠️ Tech Stack

### Frontend
- **Svelte 4** - Reactive UI framework
- **Vite 5** - Ultra-fast build tool and dev server
- **Tailwind CSS 3** - Utility-first CSS framework
- **Chart.js** - Interactive data visualization
- **Axios** - HTTP client for API calls

### Backend
- **Node.js + Express.js 4** - REST API server
- **express-session** - Session-based authentication
- **CORS & Body Parser** - Middleware for requests
- **dotenv** - Environment variable management

### Machine Learning & Data
- **PyTorch** - Deep learning framework
- **Hugging Face Transformers** - SegFormer model for semantic segmentation
- **NumPy & Pandas** - Data processing
- **scikit-learn & XGBoost** - Classical ML for irrigation prediction
- **Pillow** - Image processing

### Data Storage
- **JSON** - File-based user persistence (`data/users.json`)

---

## 📁 Project Structure

```
SEPM/
├── 📄 README.md                      # This file
├── 📄 package.json                   # Node dependencies & scripts
├── 📄 server.js                      # Express API server (main backend)
├── 📄 userStorage.js                 # User persistence helpers
├── 📄 vite.config.js                 # Vite build configuration
├── 📄 tailwind.config.js             # Tailwind CSS configuration
├── 📄 postcss.config.js              # PostCSS configuration
├── 📄 best.pt                        # SegFormer crop-stage detection model
│
├── 📂 src/                           # Svelte Frontend Application
│   ├── 📄 main.js                    # Application entry point
│   ├── 📄 App.svelte                 # Root component & navigation
│   ├── 📄 app.css                    # Global styles
│   │
│   ├── 📂 components/                # Reusable UI components
│   │   ├── Chart.svelte              # Chart.js wrapper for data visualization
│   │   ├── FarmingSimulation.svelte  # Interactive farm simulation display
│   │   ├── IrrigationStatus.svelte   # Real-time irrigation status panel
│   │   ├── Sidebar.svelte            # Navigation sidebar
│   │   └── WeatherCard.svelte        # Weather display component
│   │
│   ├── 📂 pages/                     # Full-page views
│   │   ├── Login.svelte              # User login page
│   │   ├── Signup.svelte             # New user registration
│   │   ├── Dashboard.svelte          # Main dashboard (charts, stats, weather)
│   │   ├── Weather.svelte            # Detailed weather page with search
│   │   ├── FarmInfo.svelte           # Interactive farm visualization
│   │   ├── IrrigationReport.svelte   # Generate & view irrigation reports
│   │   ├── CropStageDetection.svelte # Image upload for crop analysis
│   │   ├── SoilCheck.svelte          # Soil health monitoring
│   │   ├── Profile.svelte            # User profile management
│   │   └── Settings.svelte           # Application settings
│   │
│   ├── 📂 stores/                    # Svelte reactive stores (state management)
│   │   ├── authStore.js              # Authentication state & session
│   │   ├── weatherStore.js           # Weather data & caching
│   │   ├── farmStatsStore.js         # Farm statistics state
│   │   └── i18nStore.js              # Internationalization support
│   │
│   └── 📂 utils/                     # Utility functions
│       ├── farmingSimulation.js      # Core farm sim engine (600+ lines)
│       └── irrigationReporting.js    # Report generation utilities
│
├── 📂 python_sim/                    # Python ML & Inference Scripts
│   ├── 📄 crop_stage_inference.py    # SegFormer-based crop detection
│   ├── 📄 ml_irrigation_predictor.py # XGBoost irrigation prediction
│   ├── 📄 ml_dataset_generation.py   # Synthetic dataset creation
│   ├── 📄 ml_train_model.py          # Model training pipeline
│   ├── 📄 ml_setup.py                # End-to-end setup helper
│   ├── 📄 test_ml_integration.py     # Integration tests
│   ├── 📄 train_crop_stage_cnn.py    # Crop stage CNN training
│   ├── 📄 CROP_STAGE_SETUP.md        # ML setup documentation
│   └── 📄 irrigation_dataset.csv     # Sample training data
│
├── 📂 data/
│   └── 📄 users.json                 # User account storage (persistent)
│
├── 📂 public/
│   └── 📂 css/
│       └── 📄 style.css              # Additional stylesheets
│
└── 📂 views/                         # Legacy EJS templates (Express)
    ├── 📄 login.ejs
    ├── 📄 signup.ejs
    ├── 📄 dashboard.ejs
    └── 📄 profile.ejs

```

### Key Documentation Files
- `ARCHITECTURE.md` - System design and component relationships
- `WEB_INTEGRATION_GUIDE.md` - Frontend-backend integration details
- `GRAPHICS_IMPLEMENTATION.md` - Visual component specifications
- `FARMING_SIMULATION_SUMMARY.md` - Simulation engine documentation
- `WEATHER_IMPLEMENTATION.md` - Weather integration details
- `SETUP.md` - Detailed installation guide
- `QUICKSTART.md` - Quick reference guide

---

## ✨ Features

### 🔐 Authentication & User Management
- **Secure Login/Signup** - Password hashing with bcrypt
- **Session-Based Auth** - Express-session with cookie management
- **User Profiles** - Customizable farm details (name, size, crop type, location)
- **Profile Updates** - Edit farm information at any time
- **Demo Account** - Quick testing with pre-configured farm

### 📊 Dashboard & Analytics
- **Real-Time Statistics** - Live farm metrics and health indicators
- **Weekly Charts** - Moisture, temperature, and water usage trends
- **Water Management** - Requirement vs. actual usage tracking
- **Efficiency Metrics** - Irrigation efficiency percentages
- **Recommendations Engine** - AI-generated irrigation suggestions

### 🌦️ Weather Integration
- **Live Weather Data** - Real-time data from OpenWeatherMap API
- **Location Search** - Find weather for any location
- **Offline Fallback** - Cached weather for offline operation
- **Crop-Specific Insights** - Weather impact on your specific crop
- **UV Index & Rainfall** - Comprehensive weather metrics
- **Weather Severity** - Storm and extreme condition warnings

### 🌾 Farm Simulation
- **Interactive Canvas** - Pixel-art farm visualization
- **Dynamic Grid** - Automatically sized grid based on farm area
- **Soil States** - Visual representation of soil moisture levels
  - Dry (Brown) → Healthy (Green) → Wet (Blue)
- **Moisture Bars** - Real-time moisture visualization
- **Irrigation Animation** - Visual feedback when irrigation is active
- **Crop Health Tracking** - Monitor individual tile health

### 🖼️ Crop Stage Detection
- **Image Upload** - Upload crop photos for analysis
- **AI Analysis** - SegFormer-based deep learning inference
- **Stage Prediction** - Automatic crop growth stage detection
- **Confidence Scores** - Model confidence metrics
- **Supports Multiple Crops** - Tomato, Rice, Wheat, Corn, Sugarcane, Cotton, Potato, Onion

### 📈 Irrigation Management
- **Smart Recommendations** - Weather + soil-based suggestions
- **Report Generation** - Downloadable irrigation reports
- **Zone Management** - Multiple irrigation zone support
- **Schedule Tracking** - Next irrigation time predictions
- **Water Efficiency** - Track actual vs. required water usage

### 🌱 Soil & Crop Monitoring
- **Soil Health** - Moisture, temperature, humidity monitoring
- **Crop Requirements** - Built-in water requirements for 8+ crop types
- **Growth Tracking** - Monitor crop health over time
- **Seasonal Data** - Season-specific growing information

### 🔧 System Features
- **Responsive Design** - Works on desktop, tablet, mobile
- **Multi-Language Ready** - i18n store structure in place
- **Error Handling** - Graceful fallbacks for API failures
- **Session Persistence** - Remember user across sessions
- **Environment Configuration** - Flexible settings via .env

---

## 📦 Setup & Installation

### Step 1: Clone/Extract Project

```bash
cd SEPM
```

### Step 2: Install JavaScript Dependencies

```bash
npm install
```

This installs:
- Svelte 4 & Vite (frontend)
- Express & middleware (backend)
- Chart.js, Axios (utilities)
- Concurrently (for parallel scripts)
- Tailwind CSS, PostCSS (styling)

### Step 3: Set Up Python Environment

**Windows (PowerShell):**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install numpy pandas scikit-learn xgboost torch torchvision transformers pillow
```

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install numpy pandas scikit-learn xgboost torch torchvision transformers pillow
```

### Step 4: Create Environment Configuration (Optional)

Create `.env` in project root:

```env
# OpenWeatherMap API (optional - required for live weather)
OPENWEATHER_API_KEY=your_key_here

# Session security (change in production)
SESSION_SECRET=your_secret_key_here

# Python executable path (defaults to 'python')
PYTHON_PATH=python

# Crop stage model path (defaults to './best.pt')
CROP_STAGE_MODEL_PATH=

# Server port (optional, defaults to 3000)
PORT=3000

# Node environment
NODE_ENV=development
```

**Notes on Configuration:**
- **OPENWEATHER_API_KEY**: Get a free key at [openweathermap.org](https://openweathermap.org/api)
  - Without it, weather falls back to default values
  - The app fully works without it
- **CROP_STAGE_MODEL_PATH**: Leave empty to use `best.pt` from project root
- **SESSION_SECRET**: Use a strong random string in production

---

## 🎮 Running the Application

### Development Mode (Recommended)

Start both frontend and backend concurrently:

```bash
npm run dev
```

This command:
- Starts Vite dev server on `http://localhost:5173` (with hot reload)
- Starts Express backend on `http://localhost:3000`
- Automatically proxies `/api` calls to backend
- Watches for file changes

**Access the app:** Open browser to `http://localhost:5173`

### Alternative: Run Frontend & Backend Separately

**Terminal 1 - Frontend only:**
```bash
npm run dev:svelte
```
Runs Vite on port 5173

**Terminal 2 - Backend only:**
```bash
npm run dev:server
```
Runs Express on port 3000 with auto-restart on changes

### Production Build & Run

Build optimized production bundle:
```bash
npm run build
```

Run production server:
```bash
npm start
```

This:
- Builds Svelte to `dist/` folder
- Serves optimized bundle from Express
- No development servers, fully static frontend
- Access on `http://localhost:3000`

### Preview Production Build (without running server)

```bash
npm run preview
```

Runs Vite preview server on `http://localhost:4173`

### Run Tests

```bash
npm test
```

Runs test suite using Vitest

---

## 🔗 API Documentation

### Base URL
- **Development:** `http://localhost:3000`
- **Production:** Your deployment domain

### Authentication Endpoints

#### POST `/api/auth/login`
Log in an existing user

**Request:**
```json
{
  "username": "demo",
  "password": "demo123"
}
```

**Response (200):**
```json
{
  "success": true,
  "user": {
    "username": "demo",
    "name": "Farmer Ram",
    "farmSize": "1.5 Acre",
    "crop": "Tomato",
    "soilType": "Loamy",
    "location": "Nashik, Maharashtra",
    "lat": 19.9975,
    "lon": 73.7898
  }
}
```

#### POST `/api/auth/signup`
Create a new user account

**Request:**
```json
{
  "username": "farmer123",
  "name": "John Farmer",
  "farmSize": "2.5 Acre",
  "crop": "Wheat",
  "password": "securepass123",
  "confirmPassword": "securepass123",
  "location": "Punjab, India"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Account created! Please login."
}
```

#### POST `/api/auth/logout`
End current session

**Response (200):**
```json
{
  "success": true
}
```

#### GET `/api/auth/user`
Get current logged-in user info (requires authentication)

**Response (200):**
```json
{
  "username": "demo",
  "name": "Farmer Ram",
  "farmSize": "1.5 Acre",
  "crop": "Tomato",
  "soilType": "Loamy",
  "location": "Nashik, Maharashtra",
  "lat": 19.9975,
  "lon": 73.7898
}
```

#### POST `/api/auth/update-profile`
Update user profile (requires authentication)

**Request:**
```json
{
  "name": "Farmer Ram Updated",
  "farmSize": "2 Acre",
  "crop": "Tomato",
  "soilType": "Sandy Loam",
  "location": "Pune, Maharashtra"
}
```

**Response (200):**
```json
{
  "success": true,
  "user": { /* updated user data */ }
}
```

### Dashboard Endpoints

#### GET `/api/dashboard/data`
Get comprehensive farm and weather data (requires authentication)

**Response (200):**
```json
{
  "weather": {
    "temp": 32,
    "humidity": 60,
    "rainfall": 0,
    "windSpeed": 12,
    "description": "Partly Cloudy",
    "icon": "Clouds",
    "is_raining": false,
    "uv_index": 7
  },
  "sensors": {
    "moisture": 28,
    "temperature": 32,
    "humidity": 60,
    "rainfall": 0
  },
  "crop": {
    "name": "Tomato",
    "baseReq": 450,
    "efficiency": 85,
    "season": "Summer",
    "duration": "60-70 days"
  },
  "water": {
    "requirement": 450,
    "actual": 383,
    "deficit": 68,
    "efficiency": 85
  },
  "irrigation": {
    "status": "Active",
    "currentZone": "Zone 2",
    "timeRemaining": "12 minutes",
    "nextSchedule": "Tomorrow 6:00 AM"
  },
  "weekly": {
    "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "moisture": [35, 28, 32, 25, 28, 30, 28],
    "temperature": [28, 30, 32, 31, 32, 29, 30],
    "waterUsage": [420, 380, 450, 390, 380, 410, 380]
  },
  "recommendations": [
    "Low humidity detected - irrigation may be needed soon",
    "High temperature - increase irrigation frequency"
  ]
}
```

### Weather Endpoints

#### GET `/api/weather/:location`
Get weather for a specific location

**Parameters:**
- `location` (path) - City name or location string

**Response (200):**
```json
{
  "location": "Nashik, Maharashtra",
  "lat": 19.9975,
  "lon": 73.7898,
  "weather": {
    "temp_c": 32,
    "humidity": 60,
    "rainfall": 0,
    "wind_kph": 43,
    "condition": "Partly cloudy",
    "is_raining": false,
    "uv_index": 7,
    "weather_severity": 0.5
  }
}
```

#### GET `/weather`
Get weather for current user's location or fallback location

**Query Parameters (optional):**
- `location` - Override location

**Response (200):**
```json
{
  "location": "Nashik, Maharashtra",
  "lat": 19.9975,
  "lon": 73.7898,
  "temp_c": 32,
  "humidity": 60,
  "condition": "Partly cloudy",
  "is_raining": false,
  "offline": false,
  "source": "live"
}
```

### Machine Learning Endpoints

#### POST `/api/crop-stage/predict`
Predict crop growth stage from image (requires authentication)

**Request:**
```json
{
  "imageBase64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEA..."
}
```

**Response (200):**
```json
{
  "stage": "Grain Filling",
  "confidence": 0.92,
  "features": {
    "green_ratio": 0.65,
    "panicle_ratio": 0.18,
    "senescent_ratio": 0.25
  },
  "recommendation": "Increase irrigation for grain filling phase"
}
```

---

## 🏗️ Architecture

### System Topology

```
┌─────────────────────────────────────────────────────────────┐
│                        Browser (Client)                      │
│  Svelte SPA on http://localhost:5173 (Vite Dev Server)      │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/WebSocket (Vite Proxy)
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                     Express API Server                       │
│                 http://localhost:3000                        │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Routes:                                                 ││
│  │  - POST   /api/auth/*            (Login/Signup)        ││
│  │  - GET    /api/auth/user         (Auth Check)          ││
│  │  - GET    /api/dashboard/data    (Farm Data)           ││
│  │  - GET    /api/weather/*         (Weather)             ││
│  │  - POST   /api/crop-stage/predict (AI Inference)       ││
│  │  - GET    /               (SPA Fallback)              ││
│  └─────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Middleware:                                             ││
│  │  - express-session (Auth)                              ││
│  │  - CORS (Cross-origin)                                 ││
│  │  - Body Parser (JSON/URL)                              ││
│  └─────────────────────────────────────────────────────────┘│
└────┬──────────┬──────────────┬──────────────────────────────┘
     │          │              │
     ↓          ↓              ↓
┌────────┐  ┌──────────────┐  ┌─────────────────┐
│ JSON   │  │ OpenWeatherMap   │  Python         │
│ Storage│  │ API (External)   │  Process        │
│        │  │ (Optional)       │ (Inference)     │
│data/   │  └──────────────┘  └─────────────────┘
│users.  │                    crop_stage_
│json    │                    inference.py
└────────┘
```

### Data Flow Example: Farm Dashboard

```
User Navigates to Dashboard
         ↓
  App.svelte renders Dashboard
         ↓
  Dashboard.svelte mounts
         ↓
  onMount() calls checkAuth()
         ↓
  GET /api/auth/user (verify session)
         ↓
  GET /api/dashboard/data (fetch farm data)
         ↓
  Backend aggregates:
    - Gets user session data
    - Fetches weather from OpenWeatherMap API
    - Calculates water requirements
    - Generates recommendations
         ↓
  Response sent to frontend
         ↓
  Svelte stores updated (weatherStore, farmStatsStore)
         ↓
  UI re-renders with live data
         ↓
  Charts display (Chart.svelte)
```

### Data Flow Example: Crop Stage Detection

```
User Uploads Image
         ↓
  CropStageDetection.svelte converts image to Base64
         ↓
  POST /api/crop-stage/predict (with image + auth)
         ↓
  Backend validates authentication
         ↓
  Spawns Python child process:
    → crop_stage_inference.py
    → Loads best.pt (SegFormer model)
    → Runs inference on image
    → Returns JSON predictions
         ↓
  Backend forwards response to frontend
         ↓
  Frontend displays results
  (Stage, confidence, recommendations)
```

### Component Hierarchy

```
App.svelte (root)
├── Sidebar.svelte (navigation)
└── Main Content Area
    ├── Login.svelte
    ├── Signup.svelte
    └── (Authenticated Pages)
        ├── Dashboard.svelte
        │   ├── Chart.svelte (3x)
        │   ├── WeatherCard.svelte
        │   └── IrrigationStatus.svelte
        ├── Weather.svelte
        ├── FarmInfo.svelte
        │   └── FarmingSimulation.svelte
        ├── IrrigationReport.svelte
        ├── CropStageDetection.svelte
        ├── SoilCheck.svelte
        ├── Profile.svelte
        └── Settings.svelte
```

---

## ⚙️ Configuration

### Environment Variables (.env)

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `OPENWEATHER_API_KEY` | No | (none) | OpenWeatherMap API key for live weather |
| `SESSION_SECRET` | No | 'irrigation_secret' | Session encryption (change in production) |
| `PYTHON_PATH` | No | 'python' | Python executable path |
| `CROP_STAGE_MODEL_PATH` | No | './best.pt' | SegFormer model location |
| `PORT` | No | 3000 | Express server port |
| `NODE_ENV` | No | 'development' | Environment mode (development/production) |

### Crop Database

Built-in crop data with water requirements:

| Crop | Base Req. (mm) | Efficiency | Season | Duration |
|------|---|---|---|---|
| Tomato | 450 | 85% | Summer | 60-70 days |
| Rice | 600 | 75% | Monsoon | 120-150 days |
| Wheat | 350 | 80% | Winter | 120-140 days |
| Corn | 550 | 82% | Summer | 100-120 days |
| Sugarcane | 800 | 70% | Year-round | 12 months |
| Cotton | 500 | 78% | Summer | 160-180 days |
| Potato | 400 | 83% | Winter | 70-90 days |
| Onion | 380 | 81% | Winter | 120-150 days |

### Tailwind CSS Configuration

Configured in `tailwind.config.js`:
- Custom color palette with green/blue farming theme
- Responsive breakpoints
- Extended spacing and shadows

---

## 🧪 Demo & Testing

### Demo Account

Credentials available immediately without signup:

```
Username: demo
Password: demo123
```

**Demo Farm Details:**
- Name: Farmer Ram
- Location: Nashik, Maharashtra (India)
- Farm Size: 1.5 Acre
- Crop: Tomato
- Soil Type: Loamy

### Test ML Integration

Run Python ML tests:

```bash
cd python_sim
python test_ml_integration.py
```

Verifies:
- PyTorch installation
- Model loading
- Inference execution
- Output validation

### API Testing

#### Using cURL

Login:
```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo123"}'
```

Get Dashboard Data:
```bash
curl -X GET http://localhost:3000/api/dashboard/data \
  -H "Cookie: connect.sid=YOUR_SESSION_ID"
```

#### Using Postman

1. Import API collection (if available)
2. Set base URL to `http://localhost:3000`
3. Test endpoints with included requests

---

## 💻 Development Workflow

### Project Layout Best Practices

**Add a new page:**
1. Create `src/pages/MyPage.svelte`
2. Import in `App.svelte`
3. Add navigation case in `currentPage` handling
4. Add sidebar link in `Sidebar.svelte`

**Add a new component:**
1. Create `src/components/MyComponent.svelte`
2. Import where needed

**Add a new API endpoint:**
1. Define route in `server.js`
2. Add authentication check if needed (check `req.session.user`)
3. Return JSON response
4. Call from frontend using `fetch` or `axios`

**Add a new Svelte store:**
1. Create `src/stores/myStore.js`
2. Define writable/derived stores
3. Export functions for store updates
4. Import and use `$storeName` in components

### Code Style

- **Svelte Components**: Use `<script>`, `<style>` scoped (default)
- **JavaScript**: ES6+ modules, async/await
- **CSS**: Tailwind classes + scoped styles
- **Python**: Type hints where helpful, docstrings for functions

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes, test
npm run dev
npm test

# Commit with clear messages
git add .
git commit -m "feat: add new feature"

# Push and create PR
git push origin feature/my-feature
```

### Building & Deploying

**Development:**
```bash
npm run dev
```

**Staging/Preview:**
```bash
npm run build
npm run preview
```

**Production:**
```bash
npm run build
npm start
```

For cloud deployment (Heroku, AWS, Vercel):
1. Build: `npm run build`
2. Start script: `npm start`
3. Ensure Node.js 18+ and Python 3.8+ available
4. Set environment variables in cloud platform
5. Point to production domain

---

## 🔧 Troubleshooting

### Common Issues & Solutions

#### "Cannot find module" errors

**Problem:** Dependencies not installed
```bash
npm install
```

**Python side:**
```bash
pip install numpy pandas scikit-learn xgboost torch torchvision transformers pillow
```

#### Port already in use

**Problem:** Port 5173 or 3000 in use
```bash
# Linux/Mac: Find process using port
lsof -i :5173
kill -9 <PID>

# Windows PowerShell:
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

Or specify different ports in `vite.config.js` and `server.js`

#### Weather not working

**Issue:** OpenWeatherMap API key missing or invalid
- Solution: Get free key at [openweathermap.org](https://openweathermap.org/api)
- Add to `.env`: `OPENWEATHER_API_KEY=your_key`
- Restart server
- Note: App still works without weather (uses defaults)

#### Crop Stage Detection failing

**Issue:** Python process not found or model missing
```bash
# Check Python installed
python --version

# Ensure model exists
ls -la best.pt

# Check Python path in .env
PYTHON_PATH=python  # or full path like C:\Python39\python.exe
```

#### Session/Auth not working

**Issue:** Cookie not persisting across requests
- Ensure `credentials: 'include'` in fetch calls (frontend)
- Check CORS settings in `server.js`
- Clear browser cookies and login again

#### Vite proxy issues

**Problem:** API calls not reaching backend
- Restart dev servers
- Check proxy config in `vite.config.js`
- Backend must be running on port 3000
- Frontend must be on port 5173

#### High CPU/Memory usage

**Problem:** Crop stage inference is resource-intensive
- SegFormer model requires GPU (CUDA) for fast inference
- Without GPU: CPU inference slower but functional
- Reduce image size before upload for faster processing

#### Database/User storage issues

**Problem:** User data not persisting
- `data/` folder must exist
- `users.json` must be writable
- Check file permissions
- Manually create `users.json` if missing:
```json
{}
```

### Getting Help

1. Check **ARCHITECTURE.md** for design details
2. Review **SETUP.md** for detailed setup
3. Look at **WEATHER_IMPLEMENTATION.md** for weather API
4. Check console errors (browser DevTools + terminal)
5. Review server logs for API errors
6. Test endpoints with curl/Postman

---

## 🚀 Performance Optimization

### Frontend
- Vite build produces optimized chunks
- Svelte components are compiled to minimal JS
- Tailwind CSS tree-shakes unused styles
- Charts only render when visible

### Backend
- Express middleware optimized for response time
- Session data cached in memory
- Weather API results cached per session
- JSON persistence suitable for < 10k users

### ML/Inference
- SegFormer model loaded once at startup (if GPU available)
- Image preprocessing optimized
- Batch inference support for multiple images

---

## 📈 Future Enhancements

Potential features for future versions:

- **Mobile App** - Native iOS/Android version
- **Database Migration** - PostgreSQL/MongoDB instead of JSON
- **Real IoT Integration** - Connect actual soil sensors
- **Advanced ML** - Custom model training pipeline
- **Multi-Farm** - Manage multiple farms per user
- **Export Reports** - PDF/Excel irrigation reports
- **Mobile Notifications** - Push alerts for critical events
- **Collaborative Features** - Share farm data with consultants
- **Marketplace** - Buy/sell irrigation equipment
- **API for Partners** - REST API for third-party integrations

---

## 📄 License

ISC

---

## 📞 Support & Contact

For issues, questions, or contributions:

1. **Bug Reports**: Create detailed issue descriptions
2. **Feature Requests**: Explain use case and benefits
3. **Documentation**: Submit PRs for docs improvements
4. **Code**: Follow project style and include tests

---

## 🌍 Resources

- **Svelte Docs**: [svelte.dev](https://svelte.dev)
- **Vite Docs**: [vitejs.dev](https://vitejs.dev)
- **Express Docs**: [expressjs.com](https://expressjs.com)
- **PyTorch Docs**: [pytorch.org](https://pytorch.org)
- **Transformers Docs**: [huggingface.co/transformers](https://huggingface.co/transformers)
- **Tailwind CSS**: [tailwindcss.com](https://tailwindcss.com)
- **Chart.js**: [chartjs.org](https://www.chartjs.org)

---

**Made with 🌾 for farmers everywhere**
