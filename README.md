# 🌾 Smart Irrigation Resource Management Farming (SIRMF)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Project Overview

SIRMF is a **comprehensive AI-powered smart irrigation management system** that combines web-based monitoring with an advanced desktop farming simulator. The system uses **Machine Learning (XGBoost, 98.5% accuracy)** for intelligent irrigation predictions and features **enhanced graphics** for an immersive farming experience.

## 🆕 Latest Implemented Updates (March 2026)

- **Live Farm Stats Sync**: Farm simulator now emits real-time aggregated stats (`avgMoisture`, `avgHealth`, farms needing irrigation, weather).
- **Shared Stats Store**: Added centralized Svelte store so multiple pages consume the same live farm-state source.
- **Irrigation Report Integration**:
  - Report generation uses **live farm stats snapshot at click time**.
  - Ensures each **Generate Report** action reflects current simulator state.
- **Profile Integration**: Account Statistics now show live farm metrics (Avg Moisture, Avg Health, Needs Irrigation) instead of fixed placeholders.
- **Crop Stage Detection (SegFormer + API)**:
  - New web page for image upload and rice growth-stage inference.
  - Backend endpoint runs local `best.pt` semantic segmentation inference (no hosted LLM/Hugging Face dependency).
- **App Internationalization + Settings**:
  - Added language store, localized UI labels/messages, and a dedicated Settings page for language selection.

## ✨ Key Features

### 🤖 AI-Powered Irrigation System
- **Machine Learning Models**: XGBoost classifier (98.5% accuracy) + regressor for water amount prediction
- **Synthetic Dataset**: 5,000 training samples with realistic agricultural patterns
- **Real-time Predictions**: AI decides when to irrigate and how much water to apply
- **Decision Reasoning**: Human-readable explanations for every AI decision
- **Multi-factor Analysis**: Considers crop type, soil moisture, weather, location, and farm size

### 🎮 Desktop Farming Simulator (Pygame)
- **Enhanced Graphics Engine**: Professional particle effects, color gradients, and smooth animations
- **Interactive Gameplay**: WASD/Arrow key controls with real-time tile updates
- **Visual Feedback**: 
  - Color-coded soil moisture (brown → green → blue gradients)
  - Irrigation pulses (pulsing green borders)
  - Weather particle effects (rain drops, sun rays)
  - Moisture indicator bars
- **Professional HUD**: Real-time stats with progress bars, icons, and metrics
- **AI Integration**: Watch ML-driven irrigation decisions in action

### 🌐 Web Application
- **Professional Dashboard**: Real-time sensor monitoring with interactive Chart.js visualizations
- **Canvas-Based Simulation**: Browser farm simulator with enhanced graphics
  - Color gradient tiles
  - Moisture indicator bars
  - Irrigation pulse animations
  - Smooth color interpolation
- **Responsive Design**: Optimized for desktop, tablet, and mobile
- **Farm Info Hub**: Two-column professional layout with simulation + information panel
- **Desktop Launcher**: One-click command copy to launch pygame version

### 📊 Complete User Management
- User registration with comprehensive farm details
- Secure session-based authentication
- Profile management with stats display
- Demo account available (username: `demo`, password: `demo123`)

### 📈 Data Visualization & Analytics
- 7-day soil moisture trend charts
- Temperature trend analysis
- Daily water usage bar charts
- Real-time stat bars (moisture, crop health)
- Interactive Chart.js implementation

### 🌾 Supported Crops
| Crop | Daily Water (L/day) | Efficiency |
|------|---------------------|------------|
| Rice | 600 | 75% |
| Wheat | 350 | 80% |
| Maize/Corn | 550 | 82% |
| Tomato | 450 | 85% |
| Cotton | 500 | 78% |
| Potato | 400 | 83% |
| Sugarcane | 800 | 70% |
| Onion | 380 | 81% |

## 🛠️ Technology Stack

### Frontend
- **Web**: Svelte 4.x, HTML5, CSS3, Tailwind CSS
- **Desktop**: Pygame with custom graphics engine
- **Canvas Rendering**: JavaScript with lerpColor interpolation
- **Charts**: Chart.js 4.4.0
- **Build Tool**: Vite for fast development

### Backend
- **Server**: Node.js + Express.js
- **Sessions**: Express-session for authentication
- **API**: RESTful endpoints for user management
- **Storage**: JSON-based user data (upgradeable to MongoDB)

### Machine Learning
- **Models**: XGBoost, Random Forest
- **Libraries**: scikit-learn 1.7.2, pandas, numpy, xgboost
- **Dataset**: 5,000 synthetic samples with realistic patterns
- **Features**: 7 inputs (crop, farm_area, temperature, humidity, rainfall, soil_moisture, location)
- **Targets**: 
  - Binary classification (irrigate: yes/no)
  - Regression (water amount in liters)
- **Performance**: 
  - Classification: 98.5% accuracy, 97% F1-score
  - Regression: MAE ~45L, R² 0.94

### Development Tools
- Git for version control
- npm for JavaScript package management
- Python virtual environment (.venv)
- PowerShell/Bash terminal support

## 📁 Project Structure

```
SEPM/
├── 📄 README.md                          # This file
├── 📦 package.json                       # Node.js dependencies
├── ⚙️ vite.config.js                    # Vite build configuration
├── 🎨 tailwind.config.js                 # Tailwind CSS config
├── 🚀 server.js                          # Express backend server
├── 💾 userStorage.js                     # User data management
│
├── 📂 src/                               # Svelte web application
│   ├── main.js                          # Entry point
│   ├── App.svelte                       # Main app component
│   ├── app.css                          # Global styles
│   │
│   ├── 📂 components/                   # Reusable components
│   │   ├── Chart.svelte                # Chart.js wrapper
│   │   ├── FarmingSimulation.svelte    # Web canvas simulator
│   │   ├── IrrigationStatus.svelte     # Status display
│   │   ├── Sidebar.svelte              # Navigation
│   │   └── WeatherCard.svelte          # Weather display
│   │
│   ├── 📂 pages/                        # Page components
│   │   ├── Dashboard.svelte            # Main dashboard
│   │   ├── FarmInfo.svelte             # Farm info + simulator (★ NEW)
│   │   ├── IrrigationReport.svelte     # On-demand irrigation report (★ NEW)
│   │   ├── CropStageDetection.svelte   # Crop stage image inference page (★ NEW)
│   │   ├── Login.svelte                # Login page
│   │   ├── Signup.svelte               # Registration
│   │   ├── Profile.svelte              # User profile
│   │   ├── Settings.svelte             # Language/settings page (★ NEW)
│   │   └── Weather.svelte              # Weather page
│   │
│   ├── 📂 stores/                       # State management
│   │   ├── authStore.js                # Authentication state
│   │   ├── weatherStore.js             # Weather state
│   │   ├── i18nStore.js                # App localization state (★ NEW)
│   │   └── farmStatsStore.js           # Live farm stats state (★ NEW)
│   │
│   └── 📂 utils/                        # Utilities
│       ├── farmingSimulation.js        # Enhanced canvas simulator (★ NEW)
│       └── irrigationReporting.js      # Irrigation report builder (★ NEW)
│
├── 📂 python_sim/                        # Desktop simulator + ML
│   ├── 🎮 farm_sim.py                   # Main pygame simulator (★ ENHANCED)
│   ├── 🎨 graphics_enhanced.py          # Graphics engine (★ NEW - 480 lines)
│   ├── crop_stage_inference.py          # Crop-stage inference entrypoint using local best.pt (★ NEW)
│   ├── train_crop_stage_cnn.py          # Legacy crop-stage CNN training script
│   │
│   ├── 🤖 ML System Files (★ NEW)
│   ├── ml_dataset_generation.py        # Dataset generator (258 lines)
│   ├── ml_train_model.py               # Model training (361 lines)
│   ├── ml_irrigation_predictor.py      # Inference engine (326 lines)
│   ├── ml_setup.py                      # Complete ML pipeline (327 lines)
│   │
│   ├── 💾 ML Model Files (★ NEW)
│   ├── irrigation_dataset.csv          # Training dataset (5,000 samples)
│   ├── irrigation_classifier.pkl       # Trained classifier model
│   ├── irrigation_regressor.pkl        # Trained regressor model
│   ├── irrigation_preprocessing.pkl    # Feature scalers & encoders
│   └── irrigation_metadata.pkl         # Model metadata
│
├── 📂 public/                            # Static assets
│   └── css/
│       └── style.css                    # Global styles
│
├── 📂 views/                             # EJS templates (legacy)
│   ├── dashboard.ejs
│   ├── login.ejs
│   ├── profile.ejs
│   └── signup.ejs
│
├── 📂 data/                              # User data storage
│   └── users.json                       # User accounts
│
└── 📂 Documentation (★ NEW)
    ├── GRAPHICS_ENHANCEMENT.md          # Graphics system docs (~400 lines)
    ├── GRAPHICS_SUMMARY.md              # Visual comparison (~300 lines)
    ├── GRAPHICS_IMPLEMENTATION.md       # Implementation guide (~450 lines)
    ├── COMPLETE_OVERVIEW.md             # Full project overview (~350 lines)
    ├── WEB_INTEGRATION_GUIDE.md         # Web integration (~350 lines)
    ├── WEB_INTEGRATION_SUMMARY.md       # Web summary (~250 lines)
    ├── QUICK_START_WEB.md               # Quick start guide (~400 lines)
    ├── FARMING_INTEGRATION.md           # Farm system integration
    ├── WEATHER_IMPLEMENTATION.md        # Weather system docs
    └── ARCHITECTURE.md                  # System architecture
```

## 🚀 Installation & Setup

### Prerequisites
- **Node.js** 18.0+ and npm 9.0+
- **Python** 3.8+ with pip
- **Git** for version control
- Modern web browser (Chrome, Firefox, Edge)

### Step 1: Clone Repository
```bash
git clone https://github.com/Ankitbhaumik916/SIRMF.git
cd SIRMF
```

### Step 2: Install Node.js Dependencies
```bash
npm install
```

### Step 3: Install Python Dependencies
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Activate (Linux/Mac)
source .venv/bin/activate

# Install packages
pip install pygame numpy pandas scikit-learn xgboost

# Required for crop-stage segmentation inference
pip install transformers torch torchvision pillow
```

### Step 4: Setup ML Models (Optional but Recommended)
```bash
# Run complete ML setup (generates dataset + trains models)
python python_sim/ml_setup.py

# Or manually:
python python_sim/ml_dataset_generation.py  # Generate dataset
python python_sim/ml_train_model.py         # Train models
python python_sim/test_ml_integration.py    # Test predictions
```

## 🎮 Running the Application

### Option 1: Web Application
```bash
# Start development server
npm run dev

# Open browser
http://localhost:5173
```

**Navigation:**
1. Register or login (demo account: `demo` / `demo123`)
2. Fill in farm details (crop, size, location)
3. Navigate to **Farm Info** page
4. Watch the canvas-based simulation with enhanced graphics

### Option 2: Desktop Simulator (Pygame)
```bash
# Activate virtual environment first
.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate  # Linux/Mac

# Run with your username
python python_sim/farm_sim.py --username YOUR_USERNAME

# Example
python python_sim/farm_sim.py --username Ankit22
```

**Game Controls:**
- **W/↑** - Move up
- **S/↓** - Move down
- **A/←** - Move left
- **D/→** - Move right
- **ESC** - Quit

### Option 3: Backend Server (Optional)
```bash
node server.js
# Runs on http://localhost:3000
```

## 🧪 Testing

### Test Graphics System
```bash
python test_graphics.py
```
Verifies:
- ✓ Tile color gradients
- ✓ Particle effects (rain, sun)
- ✓ HUD panels
- ✓ Animation system

### Test ML Integration
```bash
python python_sim/test_ml_integration.py
```
Verifies:
- ✓ ML predictor loads
- ✓ Predictions work with farm conditions
- ✓ Decision reasoning generated

## 📊 ML Model Performance

### Classification Model (Should we irrigate?)
```
Model: XGBoost Classifier
Accuracy: 98.5%
Precision: 97.2%
Recall: 96.8%
F1-Score: 97.0%
```

### Regression Model (How much water?)
```
Model: XGBoost Regressor
MAE: 45.3 liters
RMSE: 68.2 liters
R² Score: 0.94
```

### Training Dataset Statistics
- **Total Samples**: 5,000
- **Features**: 7 (crop, farm_area, temperature, humidity, rainfall, soil_moisture, location)
- **Crops**: 5 (rice, wheat, maize, tomato, cotton)
- **Locations**: 5 (Punjab, Haryana, Maharashtra, Kolkata, Malda)
- **Class Balance**: 62% irrigate / 38% skip
- **Train/Test Split**: 80/20

## 🎨 Graphics Features

### Desktop (Pygame)
- **480-line Graphics Engine** with 5 major classes
- **Particle Effects**: Rain drops, sun rays, irrigation droplets
- **Color Gradients**: Smooth transitions for soil moisture
- **HUD System**: Professional stats display with icons
- **Weather Effects**: Dynamic particle spawning based on conditions
- **Animation System**: 60 FPS smooth rendering

### Web (Canvas)
- **Color Interpolation** (lerpColor algorithm)
- **Moisture Bars**: Blue indicators showing soil moisture %
- **Irrigation Pulse**: Pulsing green borders with sin wave animation
- **Gradient Tiles**: Smooth brown → green → blue transitions
- **Responsive Rendering**: Adapts to screen size

## 📖 Documentation

Comprehensive guides available:

| Document | Description | Lines |
|----------|-------------|-------|
| `GRAPHICS_ENHANCEMENT.md` | Complete graphics system documentation | ~400 |
| `GRAPHICS_IMPLEMENTATION.md` | Implementation guide with API docs | ~450 |
| `WEB_INTEGRATION_GUIDE.md` | Web integration architecture | ~350 |
| `COMPLETE_OVERVIEW.md` | Full project overview | ~350 |
| `QUICK_START_WEB.md` | Quick reference guide | ~400 |
| `ARCHITECTURE.md` | System architecture | ~300 |

## 🔧 Configuration

### Crop Profiles (ML Dataset)
Edit `python_sim/ml_dataset_generation.py`:
```python
CROP_PROFILES = {
    "rice": {
        "daily_requirement": 600,
        "optimal_moisture_min": 55,
        "optimal_moisture_max": 85,
        "temp_min": 20,
        "temp_max": 30,
    },
    # Add more crops...
}
```

### Graphics Settings
Edit `python_sim/graphics_enhanced.py`:
```python
# Color scheme
DRY_BROWN = (155, 105, 64)
HEALTHY_GREEN = (85, 145, 46)
WET_BLUE = (45, 80, 140)

# Particle settings
MAX_PARTICLES = 150
```

### Web Simulation
Edit `src/utils/farmingSimulation.js`:
```javascript
// Color gradients
const dryBrown = '#9B6940';
const healthyGreen = '#55912E';
const wetBlue = '#2D508C';
```

## 🌐 API Endpoints

### Authentication
- `POST /login` - User login
- `POST /signup` - User registration
- `GET /logout` - Clear session

### Application
- `GET /dashboard` - Main dashboard (requires auth)
- `GET /profile` - User profile (requires auth)
- `GET /farm-info` - Farm info page (requires auth)
- `GET /api/dashboard/data` - Dashboard data for report generation (requires auth)
- `POST /api/crop-stage/predict` - Crop-stage prediction from uploaded image (requires auth)

## 🚧 Future Enhancements

### Planned Features
- [ ] Real IoT sensor integration (ESP32, Arduino)
- [ ] Weather API integration (OpenWeatherMap)
- [ ] Mobile app (React Native)
- [ ] MongoDB database migration
- [ ] Real-time WebSocket updates
- [ ] Multi-field irrigation coordination
- [ ] Crop growth stage tracking
- [ ] Water cost optimization
- [ ] Historical data analytics
- [ ] Alert system (SMS/Email)

### ML Improvements
- [ ] Collect real farm data over seasons
- [ ] Retrain models with actual outcomes
- [ ] Add farmer feedback loop
- [ ] Implement reinforcement learning
- [ ] Time-series forecasting
- [ ] Ensemble model stacking

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Ankit Bhaumik** - [@Ankitbhaumik916](https://github.com/Ankitbhaumik916)

## 🙏 Acknowledgments

- XGBoost team for the powerful ML library
- Pygame community for graphics support
- Svelte team for the reactive framework
- scikit-learn for ML utilities
- Chart.js for beautiful visualizations

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Email: [ankitbhaumik23@gmail.com]
- Documentation: See `docs/` folder

---

**⭐ Star this repo if you find it helpful!**

Built with ❤️ for farmers and agricultural innovation
