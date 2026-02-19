# Smart Farming System - Quick Setup Guide

## 🚀 One-Minute Setup

### Step 1: Get Weather API Key (FREE)
1. Go to https://openweathermap.org/api
2. Sign up for a free account
3. Copy your API key from API keys section
4. Open `.env` file and replace:
   ```
   OPENWEATHER_API_KEY=your_actual_key_here
   ```

### Step 2: Build & Run

**First time setup:**
```bash
npm install  # Already done
npm run build
npm start
```

**For development (with hot reload):**
```bash
npm run dev
```

### Step 3: Access the App
- Open http://localhost:3000
- Demo account:
  - Username: `demo`
  - Password: `demo123`

## 📦 What's Included

✅ **Frontend:** Modern Svelte with Tailwind CSS  
✅ **Backend:** Express.js with REST API  
✅ **Real API:** OpenWeatherMap weather integration  
✅ **Components:** Reusable, professional UI components  
✅ **Authentication:** Secure login/signup system  
✅ **Dashboard:** Real-time data visualization  

## 🌾 Features

- **Real-time Weather Data** - Location-based updates
- **Smart Irrigation** - Crop-specific recommendations
- **Analytics** - Weekly charts and trends
- **Responsive Design** - Works on all devices
- **Professional UI** - Modern gradient design

## 📊 Dashboard Includes

- Current weather display
- Soil moisture levels
- Temperature monitoring
- Humidity tracking
- Water requirement calculations
- Weekly performance charts
- System efficiency metrics
- Smart irrigation recommendations

## 🔧 Available NPM Commands

| Command | Purpose |
|---------|---------|
| `npm start` | Run production server (port 3000) |
| `npm run dev` | Start dev server with hot reload |
| `npm run build` | Build frontend for production |
| `npm run preview` | Preview production build |

## 📁 Project Structure

```
src/
  ├── pages/           ← Page components (Login, Signup, Dashboard, Profile)
  ├── components/      ← Reusable UI components (Weather, Irrigation, Chart)
  ├── stores/          ← Authentication store
  └── utils/           ← Helper functions

server.js             ← Express backend with API routes
index.html            ← HTML entry point
vite.config.js        ← Build configuration
tailwind.config.js    ← Styling configuration
.env                  ← Environment variables (add API key here)
```

## 🤔 Troubleshooting

**Q: Weather not showing?**
A: Add OpenWeatherMap API key to `.env` and restart the server

**Q: Port already in use?**
A: Change PORT in `.env` or kill the process on port 3000

**Q: Build fails?**
A: Run `npm install` again and ensure Node.js 18+ is installed

## 📚 Next Steps

1. Get OpenWeatherMap API key
2. Add it to `.env`
3. Run `npm start`
4. Test with demo account
5. Create your own account
6. Explore the dashboard

## 🌐 Deployment Ready

This app is production-ready for:
- Heroku
- AWS
- DigitalOcean
- Vercel
- Any Node.js hosting

## 💡 Pro Tips

- Use the demo account to explore features
- Check browser console for detailed weather data
- Weekly charts update after 7 days of data
- Each crop has optimized water calculations

## 🎯 Demo Account Benefits

- Pre-configured farm in Nashik, Maharashtra
- Tomato crop with real weather data
- Full access to all features
- No setup required - just login!

---

**Version 2.0.0** | Professional Smart Farming Edition
