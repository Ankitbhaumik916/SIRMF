import { writable } from 'svelte/store'

const STORAGE_KEY = 'smartFarmingLanguage'

export const SUPPORTED_LANGUAGES = [
  { code: 'en', name: 'English' },
  { code: 'hi', name: 'हिन्दी (Hindi)' },
  { code: 'bn', name: 'বাংলা (Bengali)' },
  { code: 'ta', name: 'தமிழ் (Tamil)' },
  { code: 'te', name: 'తెలుగు (Telugu)' },
  { code: 'gu', name: 'ગુજરાતી (Gujarati)' },
]

const en = {
  'common.cancel': 'Cancel',
  'common.save': 'Save',
  'common.clear': 'Clear',
  'common.search': 'Search',
  'common.loading': 'Loading...',
  'common.location': 'Location',

  'app.title': 'Smart Farming System',
  'app.loading': 'Loading...',
  'app.irrigationTitle': 'Irrigation Management',
  'app.irrigationComingSoon': 'Irrigation management page coming soon...',

  'sidebar.smartFarming': 'Smart Farming',
  'sidebar.loggedInAs': 'Logged in as',
  'sidebar.user': 'User',
  'sidebar.dashboard': 'Dashboard',
  'sidebar.weather': 'Weather',
  'sidebar.irrigation': 'Irrigation',
  'sidebar.cropStage': 'Crop Stage AI',
  'sidebar.soilCheck': 'Soil Check',
  'sidebar.farmInfo': 'Farm Info',
  'sidebar.profile': 'Profile',
  'sidebar.settings': 'Settings',
  'sidebar.viewProfile': 'View Profile',
  'sidebar.logout': 'Logout',

  'settings.title': 'Settings',
  'settings.subtitle': 'Customize your language preferences',
  'settings.languageTitle': 'Language',
  'settings.languageDescription': 'Change language for the entire app interface.',
  'settings.currentLanguage': 'Current language',
  'settings.applied': 'Language preference saved successfully.',

  'login.header': 'Smart Farming',
  'login.subheader': 'Intelligent Irrigation Management',
  'login.username': 'Username',
  'login.password': 'Password',
  'login.usernamePlaceholder': 'Enter your username',
  'login.passwordPlaceholder': 'Enter your password',
  'login.button': 'Login',
  'login.loggingIn': 'Logging in...',
  'login.demo': 'Demo: username=demo, password=demo123',
  'login.noAccount': "Don't have an account?",
  'login.signup': 'Sign up',
  'login.errorRequired': 'Please enter username and password',
  'login.errorFailed': 'Login failed',

  'signup.title': 'Create Your Farm Account',
  'signup.step': 'Join Smart Farming Community - Step {step} of 2',
  'signup.stepCredentials': 'Credentials',
  'signup.stepFarmDetails': 'Farm Details',
  'signup.username': 'Username',
  'signup.password': 'Password',
  'signup.confirmPassword': 'Confirm Password',
  'signup.showPassword': 'Show password',
  'signup.backToLogin': 'Back to Login',
  'signup.next': 'Next: Farm Details →',
  'signup.farmerName': 'Farmer Name *',
  'signup.farmSize': 'Farm Size *',
  'signup.primaryCrop': 'Primary Crop *',
  'signup.location': 'Location',
  'signup.back': '← Back',
  'signup.createAccount': 'Create Account',
  'signup.creatingAccount': 'Creating Account...',
  'signup.alreadyHave': 'Already have an account?',
  'signup.login': 'Login',

  'profile.title': 'Your Profile',
  'profile.subtitle': 'Manage your farm information',
  'profile.updated': 'Profile updated successfully!',
  'profile.personalInfo': 'Personal Information',
  'profile.farmInfo': 'Farm Information',
  'profile.fullName': 'Full Name',
  'profile.username': 'Username',
  'profile.location': 'Location',
  'profile.notSet': 'Not set',
  'profile.farmSize': 'Farm Size',
  'profile.primaryCrop': 'Primary Crop',
  'profile.accountStatus': 'Account Status',
  'profile.active': 'Active',
  'profile.editProfile': 'Edit Profile',
  'profile.editFarmInfo': 'Edit Farm Information',
  'profile.saveChanges': 'Save Changes',
  'profile.saving': 'Saving...',
  'profile.weatherDetection': 'Used for weather detection',

  'dashboard.title': 'Dashboard',
  'dashboard.subtitle': 'Real-time Irrigation Management',
  'dashboard.loading': 'Loading dashboard data...',
  'dashboard.loadError': 'Failed to load dashboard data',
  'dashboard.welcome': 'Welcome, {name}',
  'dashboard.farmSize': 'Farm Size',
  'dashboard.cropType': 'Crop Type',
  'dashboard.season': 'Season',
  'dashboard.soilMoisture': 'Soil Moisture',
  'dashboard.temperature': 'Temperature',
  'dashboard.humidity': 'Humidity',
  'dashboard.rainfall': 'Rainfall',
  'dashboard.waterManagement': 'Water Management',
  'dashboard.recommendations': 'Recommendations',

  'weather.title': 'Weather Dashboard',
  'weather.subtitle': 'Real-time weather information for your location',
  'weather.enterLocation': 'Enter Location',
  'weather.searching': 'Searching...',
  'weather.lastUpdated': 'Last updated:',
  'weather.error': 'Error',
  'weather.fetching': 'Fetching weather data...',
  'weather.temperature': 'Temperature',
  'weather.feelsLike': 'Feels like',
  'weather.condition': 'Weather Condition',
  'weather.humidity': 'Humidity',
  'weather.windSpeed': 'Wind Speed',
  'weather.pressure': 'Pressure',
  'weather.cloudCover': 'Cloud Cover',
  'weather.rainfall': 'Rainfall',
  'weather.recommendations': 'Irrigation Recommendations',

  'weatherCard.currentWeather': 'Current Weather',
  'weatherCard.viewFull': 'View Full',
  'weatherCard.humidity': 'Humidity',
  'weatherCard.windSpeed': 'Wind Speed',
  'weatherCard.pressure': 'Pressure',
  'weatherCard.clouds': 'Clouds',

  'irrigationStatus.title': 'Irrigation Status',
  'irrigationStatus.systemStatus': 'System Status',
  'irrigationStatus.currentZone': 'Current Zone',
  'irrigationStatus.timeRemaining': 'Time Remaining',
  'irrigationStatus.nextSchedule': 'Next Schedule',
  'irrigationStatus.efficiency': 'System Efficiency',

  'cropStage.title': 'Crop Stage Detection',
  'cropStage.subtitle': 'Upload a crop image to detect the current growth stage using CNN inference.',
  'cropStage.profileCrop': 'Crop type from profile:',
  'cropStage.cropImage': 'Crop Image',
  'cropStage.detect': 'Detect Stage',
  'cropStage.analyzing': 'Analyzing...',
  'cropStage.preview': 'Image preview will appear here.',
  'cropStage.result': 'Prediction Result',
  'cropStage.crop': 'Crop:',
  'cropStage.stage': 'Stage:',
  'cropStage.confidence': 'Confidence:',
  'cropStage.model': 'Model:',
  'cropStage.topPredictions': 'Top Predictions',

  'farmInfo.title': 'Smart Farm Simulator',
  'farmInfo.subtitle': 'Real-time farming simulation with AI irrigation management',
}

const hi = {
  ...en,
  'sidebar.dashboard': 'डैशबोर्ड',
  'sidebar.weather': 'मौसम',
  'sidebar.irrigation': 'सिंचाई',
  'sidebar.cropStage': 'फसल चरण AI',
  'sidebar.farmInfo': 'खेत जानकारी',
  'sidebar.profile': 'प्रोफ़ाइल',
  'sidebar.settings': 'सेटिंग्स',
  'settings.title': 'सेटिंग्स',
  'settings.languageTitle': 'भाषा',
  'settings.languageDescription': 'पूरे ऐप की भाषा बदलें।',
  'login.button': 'लॉगिन',
  'signup.createAccount': 'खाता बनाएँ',
  'profile.title': 'आपकी प्रोफ़ाइल',
  'dashboard.title': 'डैशबोर्ड',
  'weather.title': 'मौसम डैशबोर्ड',
  'cropStage.title': 'फसल चरण पहचान',
}

const bn = {
  ...en,
  'sidebar.dashboard': 'ড্যাশবোর্ড',
  'sidebar.weather': 'আবহাওয়া',
  'sidebar.irrigation': 'সেচ',
  'sidebar.cropStage': 'ফসল স্তর AI',
  'sidebar.farmInfo': 'খামার তথ্য',
  'sidebar.profile': 'প্রোফাইল',
  'sidebar.settings': 'সেটিংস',
  'settings.title': 'সেটিংস',
  'settings.languageTitle': 'ভাষা',
  'settings.languageDescription': 'পুরো অ্যাপের ভাষা পরিবর্তন করুন।',
  'login.button': 'লগইন',
  'signup.createAccount': 'অ্যাকাউন্ট তৈরি করুন',
  'profile.title': 'আপনার প্রোফাইল',
  'dashboard.title': 'ড্যাশবোর্ড',
  'weather.title': 'আবহাওয়া ড্যাশবোর্ড',
  'cropStage.title': 'ফসল স্তর শনাক্তকরণ',
}

const ta = {
  ...en,
  'sidebar.dashboard': 'டாஷ்போர்டு',
  'sidebar.weather': 'வானிலை',
  'sidebar.irrigation': 'நீர்ப்பாசனம்',
  'sidebar.cropStage': 'பயிர் நிலை AI',
  'sidebar.farmInfo': 'பண்ணை தகவல்',
  'sidebar.profile': 'சுயவிவரம்',
  'sidebar.settings': 'அமைப்புகள்',
  'settings.title': 'அமைப்புகள்',
  'settings.languageTitle': 'மொழி',
  'settings.languageDescription': 'முழு பயன்பாட்டின் மொழியை மாற்றவும்.',
  'login.button': 'உள்நுழை',
  'signup.createAccount': 'கணக்கு உருவாக்கு',
  'profile.title': 'உங்கள் சுயவிவரம்',
  'dashboard.title': 'டாஷ்போர்டு',
  'weather.title': 'வானிலை டாஷ்போர்டு',
  'cropStage.title': 'பயிர் நிலை கண்டறிதல்',
}

const te = {
  ...en,
  'sidebar.dashboard': 'డ్యాష్‌బోర్డ్',
  'sidebar.weather': 'వాతావరణం',
  'sidebar.irrigation': 'పారుదల',
  'sidebar.cropStage': 'పంట దశ AI',
  'sidebar.farmInfo': 'ఫారం సమాచారం',
  'sidebar.profile': 'ప్రొఫైల్',
  'sidebar.settings': 'సెట్టింగ్స్',
  'settings.title': 'సెట్టింగ్స్',
  'settings.languageTitle': 'భాష',
  'settings.languageDescription': 'మొత్తం యాప్ భాషను మార్చండి.',
  'login.button': 'లాగిన్',
  'signup.createAccount': 'ఖాతా సృష్టించండి',
  'profile.title': 'మీ ప్రొఫైల్',
  'dashboard.title': 'డ్యాష్‌బోర్డ్',
  'weather.title': 'వాతావరణ డ్యాష్‌బోర్డ్',
  'cropStage.title': 'పంట దశ గుర్తింపు',
}

const gu = {
  ...en,
  'sidebar.dashboard': 'ડેશબોર્ડ',
  'sidebar.weather': 'હવામાન',
  'sidebar.irrigation': 'સિંચાઈ',
  'sidebar.cropStage': 'પાક તબક્કો AI',
  'sidebar.farmInfo': 'ખેત માહિતી',
  'sidebar.profile': 'પ્રોફાઇલ',
  'sidebar.settings': 'સેટિંગ્સ',
  'settings.title': 'સેટિંગ્સ',
  'settings.languageTitle': 'ભાષા',
  'settings.languageDescription': 'સંપૂર્ણ એપની ભાષા બદલો.',
  'login.button': 'લૉગિન',
  'signup.createAccount': 'એકાઉન્ટ બનાવો',
  'profile.title': 'તમારી પ્રોફાઇલ',
  'dashboard.title': 'ડેશબોર્ડ',
  'weather.title': 'હવામાન ડેશબોર્ડ',
  'cropStage.title': 'પાક તબક્કો ઓળખ',
}

const dictionaries = { en, hi, bn, ta, te, gu }

function getInitialLanguage() {
  if (typeof window === 'undefined') return 'en'
  const saved = localStorage.getItem(STORAGE_KEY)
  return dictionaries[saved] ? saved : 'en'
}

export const languageStore = writable(getInitialLanguage())

if (typeof window !== 'undefined') {
  languageStore.subscribe((lang) => {
    if (dictionaries[lang]) {
      localStorage.setItem(STORAGE_KEY, lang)
      document.documentElement.lang = lang
    }
  })
}

export function setLanguage(lang) {
  if (dictionaries[lang]) {
    languageStore.set(lang)
  }
}

export function t(key, lang = 'en', vars = {}) {
  let text = dictionaries[lang]?.[key] || dictionaries.en[key] || key
  Object.keys(vars).forEach((varName) => {
    text = text.replaceAll(`{${varName}}`, String(vars[varName]))
  })
  return text
}
