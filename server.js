const express = require("express");
const session = require("express-session");
const path = require("path");

const app = express();

// In-memory user database
const users = {};

// View engine
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

// Middleware
app.use(express.static("public"));
app.use(express.urlencoded({ extended: true }));
app.use(
  session({
    secret: "irrigation_secret",
    resave: false,
    saveUninitialized: true,
  })
);

// Helper function to calculate water requirement based on crop
function getWaterRequirement(crop) {
  const cropData = {
    Tomato: { baseReq: 450, efficiency: 85 },
    Rice: { baseReq: 600, efficiency: 75 },
    Wheat: { baseReq: 350, efficiency: 80 },
    Corn: { baseReq: 550, efficiency: 82 },
    Sugarcane: { baseReq: 800, efficiency: 70 },
    Cotton: { baseReq: 500, efficiency: 78 },
    Potato: { baseReq: 400, efficiency: 83 },
    Onion: { baseReq: 380, efficiency: 81 },
  };
  return cropData[crop] || { baseReq: 450, efficiency: 80 };
}

// Routes
app.get("/", (req, res) => {
  if (req.session.user) return res.redirect("/dashboard");
  res.redirect("/login");
});

app.get("/login", (req, res) => {
  res.render("login", { error: null });
});

app.post("/login", (req, res) => {
  const { username, password } = req.body;

  if (!username || !password) {
    return res.render("login", { error: "Please enter username and password" });
  }

  if (users[username] && users[username].password === password) {
    req.session.user = users[username];
    return res.redirect("/dashboard");
  }

  // Demo account
  if (username === "demo" && password === "demo123") {
    req.session.user = {
      username: "demo",
      name: "Farmer Ram",
      farmSize: "1.5 Acre",
      crop: "Tomato",
      location: "Nashik, Maharashtra",
    };
    return res.redirect("/dashboard");
  }

  res.render("login", { error: "Invalid username or password" });
});

app.get("/signup", (req, res) => {
  res.render("signup", { error: null, success: null });
});

app.post("/signup", (req, res) => {
  const { username, name, farmSize, crop, password, confirmPassword } = req.body;

  if (!username || !name || !farmSize || !crop || !password || !confirmPassword) {
    return res.render("signup", { error: "All fields are required", success: null });
  }

  if (password !== confirmPassword) {
    return res.render("signup", { error: "Passwords do not match", success: null });
  }

  if (users[username]) {
    return res.render("signup", { error: "Username already exists", success: null });
  }

  users[username] = {
    username,
    name,
    farmSize,
    crop,
    password,
    location: "India",
  };

  res.render("signup", { error: null, success: "Account created! Please login." });
});

app.get("/profile", (req, res) => {
  if (!req.session.user) return res.redirect("/login");
  res.render("profile", { user: req.session.user });
});

app.get("/dashboard", (req, res) => {
  if (!req.session.user) return res.redirect("/login");

  const user = req.session.user;
  const waterReq = getWaterRequirement(user.crop);

  // Dummy sensor data with comprehensive irrigation info
  const data = {
    moisture: 28,
    temperature: 32,
    humidity: 60,
    rainfall: 5,

    // Crop water requirement based on selected crop
    cropWaterReq: waterReq.baseReq,
    actualWaterUsed: Math.round(waterReq.baseReq * 0.85),
    waterDeficit: Math.round(waterReq.baseReq * 0.15),

    // Irrigation status
    irrigationStatus: "Active",
    currentZone: "Zone 2",
    timeRemaining: "12 minutes",
    nextSchedule: "Tomorrow 6:00 AM",

    // Weekly data for charts
    weeklyMoisture: [35, 28, 32, 25, 28, 30, 28],
    weeklyTemp: [28, 30, 32, 31, 32, 29, 30],
    weeklyWaterUsage: [420, 380, 450, 390, 380, 410, 380],
    weeklyDays: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],

    recommendation: "✓ Soil moisture is optimal. Continue current irrigation schedule.",
    efficiencyScore: waterReq.efficiency,
  };

  res.render("dashboard", { user, data });
});

app.get("/logout", (req, res) => {
  req.session.destroy();
  res.redirect("/login");
});

app.listen(3000, () =>
  console.log("Server running at http://localhost:3000")
);
