import express from 'express'
import session from 'express-session'
import axios from 'axios'
import cors from 'cors'
import dotenv from 'dotenv'
import { spawn } from 'child_process'
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'
import { loadUsers, saveUsers, hashPassword, verifyPassword, getUserByUsername, createUser, updateUser } from './userStorage.js'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

dotenv.config()

const app = express()

// Load users from persistent storage
let users = loadUsers()

// Middleware
app.use(cors({
  origin: 'http://localhost:5173',
  credentials: true
}))
app.use(express.json({ limit: '20mb' }))
app.use(express.urlencoded({ extended: true, limit: '20mb' }))
app.use(
  session({
    secret: process.env.SESSION_SECRET || 'irrigation_secret',
    resave: false,
    saveUninitialized: true,
  })
)

// ===================== DATA HELPERS =====================

// Crop data with water requirements
const cropData = {
  Tomato: { baseReq: 450, efficiency: 85, season: 'Summer', duration: '60-70 days' },
  Rice: { baseReq: 600, efficiency: 75, season: 'Monsoon', duration: '120-150 days' },
  Wheat: { baseReq: 350, efficiency: 80, season: 'Winter', duration: '120-140 days' },
  Corn: { baseReq: 550, efficiency: 82, season: 'Summer', duration: '100-120 days' },
  Sugarcane: { baseReq: 800, efficiency: 70, season: 'Year-round', duration: '12 months' },
  Cotton: { baseReq: 500, efficiency: 78, season: 'Summer', duration: '160-180 days' },
  Potato: { baseReq: 400, efficiency: 83, season: 'Winter', duration: '70-90 days' },
  Onion: { baseReq: 380, efficiency: 81, season: 'Winter', duration: '120-150 days' },
}

function getWaterRequirement(crop) {
  return cropData[crop] || { baseReq: 450, efficiency: 80, season: 'Mixed', duration: '90-120 days' }
}

// Fetch weather data from OpenWeatherMap
async function getWeatherData(lat, lon) {
  try {
    const apiKey = process.env.OPENWEATHER_API_KEY
    if (!apiKey) {
      console.warn('OPENWEATHER_API_KEY not set')
      return null
    }

    const response = await axios.get(
      `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${apiKey}&units=metric`
    )

    return {
      temp: Math.round(response.data.main.temp),
      temp_c: Math.round(response.data.main.temp),
      feelsLike: Math.round(response.data.main.feels_like),
      humidity: response.data.main.humidity,
      pressure: response.data.main.pressure,
      windSpeed: Math.round(response.data.wind.speed * 3.6), // m/s to km/h
      wind_kph: Math.round(response.data.wind.speed * 3.6),
      cloudiness: response.data.clouds.all,
      description: response.data.weather[0].description,
      condition: response.data.weather[0].description,
      icon: response.data.weather[0].main,
      rainfall: response.data.rain ? response.data.rain['1h'] : 0,
      rain_probability: Math.max(0, Math.min(1, ((response.data.clouds.all || 0) / 120) + (response.data.rain ? 0.25 : 0))),
      is_raining: Boolean(response.data.rain && response.data.rain['1h'] > 0) || /rain|drizzle|storm/i.test(response.data.weather[0].description || ''),
      uv_index: Math.max(0, Math.min(11, Math.round(11 - (response.data.clouds.all || 0) / 12 + (response.data.main.temp > 30 ? 1 : 0)))),
      weather_severity: /storm|extreme|thunder/i.test(response.data.weather[0].description || '')
        ? 1
        : /cloud|drizzle|rain|mist|haze/i.test(response.data.weather[0].description || '')
          ? 0.5
          : 0,
    }
  } catch (error) {
    console.error('Weather API Error:', error.message)
    return null
  }
}

// Get coordinates for a location (using OpenWeatherMap Geocoding)
async function getCoordinates(location) {
  try {
    const apiKey = process.env.OPENWEATHER_API_KEY
    if (!apiKey) return null

    const response = await axios.get(
      `https://api.openweathermap.org/geo/1.0/direct?q=${location}&limit=1&appid=${apiKey}`
    )

    if (response.data.length > 0) {
      const { lat, lon } = response.data[0]
      return { lat, lon }
    }
    return null
  } catch (error) {
    console.error('Geocoding Error:', error.message)
    return null
  }
}

function buildWeatherResponse(location, coords, weather, offline = false) {
  const temp_c = weather.temp_c ?? weather.temp ?? 32
  const humidity = weather.humidity ?? 60
  const wind_kph = weather.wind_kph ?? weather.windSpeed ?? 12
  const rain_probability = weather.rain_probability ?? 0.15
  const condition = weather.condition ?? weather.description ?? 'Partly cloudy'

  return {
    location,
    lat: coords?.lat ?? null,
    lon: coords?.lon ?? null,
    temp_c,
    humidity,
    rain_probability,
    wind_kph,
    condition,
    is_raining: weather.is_raining ?? /rain|drizzle|storm/i.test(condition),
    uv_index: weather.uv_index ?? 7,
    weather_severity: weather.weather_severity ?? (/storm|extreme|thunder/i.test(condition) ? 1 : /cloud|drizzle|rain|mist|haze/i.test(condition) ? 0.5 : 0),
    offline,
    source: offline ? 'cached' : 'live',
    ...weather,
  }
}

function runCropStageInference(imageBase64, cropType) {
  return new Promise((resolve, reject) => {
    const scriptPath = join(__dirname, 'python_sim', 'crop_stage_inference.py')
    const pythonCommand = process.env.PYTHON_PATH || 'python'

    const pythonProcess = spawn(pythonCommand, [scriptPath], {
      stdio: ['pipe', 'pipe', 'pipe'],
    })

    let stdout = ''
    let stderr = ''

    pythonProcess.stdout.on('data', (data) => {
      stdout += data.toString()
    })

    pythonProcess.stderr.on('data', (data) => {
      stderr += data.toString()
    })

    pythonProcess.on('error', (error) => {
      reject(new Error(`Failed to start Python process: ${error.message}`))
    })

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(stderr || `Crop stage inference failed with code ${code}`))
        return
      }

      try {
        const parsed = JSON.parse(stdout)
        resolve(parsed)
      } catch (error) {
        reject(new Error(`Invalid response from inference script: ${error.message}`))
      }
    })

    const payload = {
      cropType,
      imageBase64,
      modelPath: process.env.CROP_STAGE_MODEL_PATH || '',
    }

    pythonProcess.stdin.write(JSON.stringify(payload))
    pythonProcess.stdin.end()
  })
}

// Generate irrigation recommendations based on weather
function generateIrrigationRecommendations(weather, crop) {
  const req = getWaterRequirement(crop)
  const recommendations = []

  if (weather.humidity < 40) {
    recommendations.push('Low humidity detected - irrigation may be needed soon')
  }
  if (weather.rainfall > 0) {
    recommendations.push(`Rainfall detected (${weather.rainfall}mm) - reduce irrigation`)
  }
  if (weather.temp > 35) {
    recommendations.push('High temperature - increase irrigation frequency')
  }
  if (weather.cloudiness > 60) {
    recommendations.push('Cloudy weather - reduce evapotranspiration loss')
  }

  return recommendations.length > 0 
    ? recommendations 
    : ['✓ Current weather conditions are optimal for irrigation']
}

// ===================== AUTH ROUTES =====================

app.post('/api/auth/login', (req, res) => {
  const { username, password } = req.body

  if (!username || !password) {
    return res.status(400).json({ error: 'Username and password required' })
  }

  const user = getUserByUsername(username, users)

  // Check registered user
  if (user && verifyPassword(password, user.passwordHash)) {
    req.session.user = {
      username: user.username,
      name: user.name,
      farmSize: user.farmSize,
      crop: user.crop,
      soilType: user.soilType || 'Loamy',
      location: user.location,
      lat: user.lat,
      lon: user.lon,
    }
    return res.json({ success: true, user: req.session.user })
  }

  // Demo account fallback
  if (username === 'demo' && password === 'demo123') {
    req.session.user = {
      username: 'demo',
      name: 'Farmer Ram',
      farmSize: '1.5 Acre',
      crop: 'Tomato',
      soilType: 'Loamy',
      location: 'Nashik, Maharashtra',
      lat: 19.9975,
      lon: 73.7898,
    }
    return res.json({ success: true, user: req.session.user })
  }

  res.status(401).json({ error: 'Invalid credentials' })
})

app.post('/api/auth/signup', (req, res) => {
  const { username, name, farmSize, crop, password, confirmPassword, location } = req.body

  if (!username || !name || !farmSize || !crop || !password || !confirmPassword) {
    return res.status(400).json({ error: 'All fields are required' })
  }

  if (password !== confirmPassword) {
    return res.status(400).json({ error: 'Passwords do not match' })
  }

  if (password.length < 6) {
    return res.status(400).json({ error: 'Password must be at least 6 characters' })
  }

  if (getUserByUsername(username, users)) {
    return res.status(400).json({ error: 'Username already exists' })
  }

  // Create new user with hashed password
  const newUser = {
    username,
    name,
    farmSize,
    crop,
    soilType: 'Loamy',
    location: location || 'India',
    passwordHash: hashPassword(password),
    lat: null,
    lon: null,
  }

  if (createUser(username, newUser, users)) {
    // Reload users from storage
    users = loadUsers()
    return res.json({ success: true, message: 'Account created! Please login.' })
  } else {
    return res.status(500).json({ error: 'Failed to create account' })
  }
})

app.post('/api/auth/logout', (req, res) => {
  req.session.destroy()
  res.json({ success: true })
})

app.get('/api/auth/user', (req, res) => {
  if (!req.session.user) {
    return res.status(401).json({ error: 'Not authenticated' })
  }
  res.json(req.session.user)
})

// Update user profile
app.post('/api/auth/update-profile', (req, res) => {
  if (!req.session.user) {
    return res.status(401).json({ error: 'Not authenticated' })
  }

  const { name, farmSize, crop, soilType, location } = req.body
  const username = req.session.user.username

  const updates = {}
  if (name) updates.name = name
  if (farmSize) updates.farmSize = farmSize
  if (crop) updates.crop = crop
  if (soilType) updates.soilType = soilType
  if (location) updates.location = location

  if (updateUser(username, updates, users)) {
    // Update session
    req.session.user = { ...req.session.user, ...updates }
    return res.json({ success: true, user: req.session.user })
  } else {
    return res.status(500).json({ error: 'Failed to update profile' })
  }
})

// ===================== DASHBOARD API ROUTES =====================

app.get('/api/dashboard/data', async (req, res) => {
  if (!req.session.user) {
    return res.status(401).json({ error: 'Not authenticated' })
  }

  const user = req.session.user
  const waterReq = getWaterRequirement(user.crop)

  // Get weather data
  let weatherData = null
  if (user.lat && user.lon) {
    weatherData = await getWeatherData(user.lat, user.lon)
  } else if (user.location) {
    const coords = await getCoordinates(user.location)
    if (coords) {
      weatherData = await getWeatherData(coords.lat, coords.lon)
      // Store coordinates for future use
      user.lat = coords.lat
      user.lon = coords.lon
    }
  }

  // Default sensor data
  const sensorData = {
    moisture: 28,
    temperature: weatherData ? weatherData.temp : 32,
    humidity: weatherData ? weatherData.humidity : 60,
    rainfall: weatherData ? weatherData.rainfall : 0,
  }

  // Calculate water requirements
  const data = {
    weather: weatherData || {
      temp: 32,
      humidity: 60,
      rainfall: 0,
      windSpeed: 12,
      description: 'Partly Cloudy',
      icon: 'Clouds',
    },
    sensors: sensorData,
    crop: {
      name: user.crop,
      ...waterReq,
    },
    water: {
      requirement: waterReq.baseReq,
      actual: Math.round(waterReq.baseReq * 0.85),
      deficit: Math.round(waterReq.baseReq * 0.15),
      efficiency: waterReq.efficiency,
    },
    irrigation: {
      status: 'Active',
      currentZone: 'Zone 2',
      timeRemaining: '12 minutes',
      nextSchedule: 'Tomorrow 6:00 AM',
    },
    weekly: {
      days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      moisture: [35, 28, 32, 25, 28, 30, 28],
      temperature: [28, 30, 32, 31, 32, 29, 30],
      waterUsage: [420, 380, 450, 390, 380, 410, 380],
    },
    recommendations: generateIrrigationRecommendations(sensorData, user.crop),
  }

  res.json(data)
})

app.get('/api/weather/:location', async (req, res) => {
  const { location } = req.params
  
  const coords = await getCoordinates(location)
  if (!coords) {
    return res.status(404).json({ error: 'Location not found' })
  }

  const weatherData = await getWeatherData(coords.lat, coords.lon)
  if (!weatherData) {
    return res.status(500).json({ error: 'Failed to fetch weather data' })
  }

  res.json({ location, ...coords, weather: weatherData })
})

app.get('/weather', async (req, res) => {
  const location = req.query.location || req.session.user?.location || 'Nashik, Maharashtra'
  const hasSessionCoords = req.session.user?.lat != null && req.session.user?.lon != null
  const coords = hasSessionCoords
    ? { lat: req.session.user.lat, lon: req.session.user.lon }
    : await getCoordinates(location)

  if (!coords) {
    const cachedWeather = req.session.lastWeather
    if (cachedWeather) {
      return res.json({ ...cachedWeather, offline: true, source: 'cached' })
    }

    return res.json(
      buildWeatherResponse(location, null, {
        temp_c: 32,
        humidity: 60,
        rain_probability: 0.15,
        wind_kph: 12,
        condition: 'Partly cloudy',
        is_raining: false,
        uv_index: 7,
        weather_severity: 0.5,
      }, true)
    )
  }

  const weatherData = await getWeatherData(coords.lat, coords.lon)
  if (!weatherData) {
    const cachedWeather = req.session.lastWeather
    if (cachedWeather) {
      return res.json({ ...cachedWeather, offline: true, source: 'cached' })
    }

    return res.json(
      buildWeatherResponse(location, coords, {
        temp_c: 32,
        humidity: 60,
        rain_probability: 0.15,
        wind_kph: 12,
        condition: 'Partly cloudy',
        is_raining: false,
        uv_index: 7,
        weather_severity: 0.5,
      }, true)
    )
  }

  const payload = buildWeatherResponse(location, coords, weatherData, false)
  req.session.lastWeather = payload
  res.json(payload)
})

app.get('/simulation', (req, res) => {
  res.sendFile(join(__dirname, 'sirmf_ml.html'))
})

app.get('/impl1', (req, res) => {
  res.sendFile(join(__dirname, 'impl1.html'))
})

app.post('/api/crop-stage/predict', async (req, res) => {
  if (!req.session.user) {
    return res.status(401).json({ error: 'Not authenticated' })
  }

  const cropType = req.session.user.crop
  const { imageBase64 } = req.body

  if (!cropType) {
    return res.status(400).json({ error: 'Crop type is not set in profile' })
  }

  if (!imageBase64 || typeof imageBase64 !== 'string') {
    return res.status(400).json({ error: 'imageBase64 is required' })
  }

  try {
    const result = await runCropStageInference(imageBase64, cropType)
    res.json(result)
  } catch (error) {
    console.error('Crop stage prediction error:', error)
    res.status(500).json({ error: error.message || 'Crop stage prediction failed' })
  }
})

// ===================== STATIC FILES & SERVER =====================

// Serve static files from dist
app.use(express.static('dist'))

// SPA fallback - serve index.html for all non-API routes
app.get('*', (req, res) => {
  res.sendFile(join(__dirname, 'dist/index.html'))
})

const PORT = process.env.PORT || 3000
app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`)
  console.log(`🌾 Smart Farming System - Professional Edition`)
  console.log(`📡 Demo account: username=demo, password=demo123`)
})
