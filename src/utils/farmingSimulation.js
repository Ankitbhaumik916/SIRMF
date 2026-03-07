/**
 * Pixel-Art Precision Farming Simulation Module
 * Modular component for embedding farming simulation in any web application
 */

// ============== FARM TILE CLASS ==============
class FarmTile {
  constructor(x, y, tileType = 'farmland') {
    this.x = x;
    this.y = y;
    this.tileType = tileType; // 'farmland', 'water', 'house', 'path'
    this.soilMoisture = 50; // 0-100
    this.cropHealth = 75; // 0-100
    this.irrigationActive = false;
    this.id = `farm_${x}_${y}`;
  }

  update(deltaTime, weatherState) {
    if (this.tileType !== 'farmland') return;

    const deltaTimeSeconds = deltaTime / 1000;
    const evaporationRate = this.getEvaporationRate(weatherState);
    
    // Moisture loss due to evaporation
    this.soilMoisture -= evaporationRate * deltaTimeSeconds;

    // Natural moisture gain from rain
    if (weatherState === 'rainy') {
      this.soilMoisture += 8 * deltaTimeSeconds;
    }

    // Irrigation effect
    if (this.irrigationActive) {
      this.soilMoisture += 15 * deltaTimeSeconds;
    }

    // Clamp moisture
    this.soilMoisture = Math.max(0, Math.min(100, this.soilMoisture));

    // Auto-activate irrigation if too dry
    if (this.soilMoisture < 35) {
      this.irrigationActive = true;
    }

    // Deactivate irrigation if moisture is good
    if (this.soilMoisture > 70) {
      this.irrigationActive = false;
    }

    // Update crop health based on moisture
    this.updateCropHealth();
  }

  getEvaporationRate(weatherState) {
    switch (weatherState) {
      case 'sunny':
        return 12; // Fast loss
      case 'cloudy':
        return 6; // Balanced
      case 'rainy':
        return 2; // Slow loss
      default:
        return 6;
    }
  }

  updateCropHealth() {
    const optimalMoisture = { min: 40, max: 70 };
    const healthChange = 0.5;

    if (this.soilMoisture >= optimalMoisture.min && this.soilMoisture <= optimalMoisture.max) {
      this.cropHealth = Math.min(100, this.cropHealth + healthChange * 0.1);
    } else if (this.soilMoisture < 20 || this.soilMoisture > 85) {
      this.cropHealth = Math.max(0, this.cropHealth - healthChange * 0.2);
    } else {
      this.cropHealth = Math.max(0, this.cropHealth - healthChange * 0.05);
    }
  }

  getColor() {
    if (this.tileType === 'house') return '#CD853F';
    if (this.tileType === 'water') return '#4A90E2';
    if (this.tileType === 'path') return '#A0826D';

    // Farmland color based on moisture
    if (this.soilMoisture < 30) return '#8B6914'; // Dry brown
    if (this.soilMoisture > 75) return '#1E3A8A'; // Overwatered dark blue
    return '#2D5016'; // Healthy green
  }
}

// ============== WEATHER SYSTEM ==============
class WeatherSystem {
  constructor() {
    this.currentWeather = 'sunny';
    this.weatherChangeTimer = 0;
    this.weatherChangeDuration = 5000; // 5 seconds
    this.weatherCycle = ['sunny', 'cloudy', 'rainy'];
    this.weatherIndex = 0;
  }

  update(deltaTime) {
    this.weatherChangeTimer += deltaTime;

    if (this.weatherChangeTimer > this.weatherChangeDuration) {
      this.changeWeather();
      this.weatherChangeTimer = 0;
    }
  }

  changeWeather() {
    this.weatherIndex = Math.floor(Math.random() * this.weatherCycle.length);
    this.currentWeather = this.weatherCycle[this.weatherIndex];
  }

  getWeatherColor() {
    switch (this.currentWeather) {
      case 'sunny':
        return '#FFD700';
      case 'cloudy':
        return '#A9A9A9';
      case 'rainy':
        return '#4682B4';
      default:
        return '#FFD700';
    }
  }

  getWeatherEmoji() {
    switch (this.currentWeather) {
      case 'sunny':
        return '☀️';
      case 'cloudy':
        return '☁️';
      case 'rainy':
        return '🌧️';
      default:
        return '☀️';
    }
  }
}

// ============== IRRIGATION CONTROLLER ==============
class IrrigationController {
  constructor(farms) {
    this.farms = farms;
  }

  getFarmsNeedingIrrigation() {
    return this.farms.filter(
      (farm) => farm.tileType === 'farmland' && farm.soilMoisture < 35
    ).length;
  }

  getAveragesoilMoisture() {
    const farmlands = this.farms.filter((farm) => farm.tileType === 'farmland');
    if (farmlands.length === 0) return 0;
    const total = farmlands.reduce((sum, farm) => sum + farm.soilMoisture, 0);
    return Math.round(total / farmlands.length);
  }

  getTotalFarms() {
    return this.farms.filter((farm) => farm.tileType === 'farmland').length;
  }
}

// ============== FARMER CONTROLLER ==============
class FarmerController {
  constructor(startX, startY, gridSize) {
    this.x = startX;
    this.y = startY;
    this.gridSize = gridSize;
    this.keys = {};
    this.interactionRange = 1.5; // Tile distance for interaction
    this.animationFrame = 0;
    this.animationSpeed = 0.1;

    this.setupListeners();
  }

  setupListeners() {
    document.addEventListener('keydown', (e) => {
      this.keys[e.key.toLowerCase()] = true;
    });

    document.addEventListener('keyup', (e) => {
      this.keys[e.key.toLowerCase()] = false;
    });
  }

  update(farms, mapWidth, mapHeight) {
    const moveSpeed = 0.1; // Tiles per frame
    let newX = this.x;
    let newY = this.y;

    // WASD and Arrow keys movement
    if (this.keys['w'] || this.keys['arrowup']) newY -= moveSpeed;
    if (this.keys['s'] || this.keys['arrowdown']) newY += moveSpeed;
    if (this.keys['a'] || this.keys['arrowleft']) newX -= moveSpeed;
    if (this.keys['d'] || this.keys['arrowright']) newX += moveSpeed;

    // Boundary checking
    newX = Math.max(0, Math.min(mapWidth - 1, newX));
    newY = Math.max(0, Math.min(mapHeight - 1, newY));

    this.x = newX;
    this.y = newY;

    // Animation
    this.animationFrame += this.animationSpeed;
    if (this.animationFrame > 4) this.animationFrame = 0;
  }

  getNearbyFarm(farms) {
    return farms.find(
      (farm) =>
        Math.abs(farm.x - this.x) <= this.interactionRange &&
        Math.abs(farm.y - this.y) <= this.interactionRange &&
        farm.tileType === 'farmland'
    );
  }

  getAnimationFrame() {
    return Math.floor(this.animationFrame);
  }
}

// ============== GAME RENDERER ==============
class GameRenderer {
  constructor(canvas, tileSize = 32) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.tileSize = tileSize;
    this.particleSystem = new ParticleSystem();
  }

  render(farms, farmer, weather, mapWidth, mapHeight) {
    const canvasWidth = mapWidth * this.tileSize;
    const canvasHeight = mapHeight * this.tileSize;

    this.canvas.width = canvasWidth;
    this.canvas.height = canvasHeight;

    // Draw tiles
    farms.forEach((farm) => {
      this.drawTile(farm);
    });

    // Draw water animation on irrigated farms
    farms.forEach((farm) => {
      if (farm.irrigationActive) {
        this.drawIrrigationAnimation(farm);
      }
    });

    // Draw farmer
    this.drawFarmer(farmer);

    // Update and draw particles
    this.particleSystem.update();
    this.particleSystem.draw(this.ctx, this.tileSize);

    // Draw UI overlay
    this.drawUIOverlay(weather);
  }

  drawTile(farm) {
    const x = farm.x * this.tileSize;
    const y = farm.y * this.tileSize;
    const size = this.tileSize;

    // Draw tile background
    this.ctx.fillStyle = farm.getColor();
    this.ctx.fillRect(x, y, size, size);

    // Draw grid
    this.ctx.strokeStyle = '#666666';
    this.ctx.lineWidth = 1;
    this.ctx.strokeRect(x, y, size, size);

    // Draw crop status icon on farmland
    if (farm.tileType === 'farmland') {
      this.drawCropStatus(farm, x, y);
    } else if (farm.tileType === 'house') {
      this.drawHouse(x, y);
    } else if (farm.tileType === 'water') {
      this.drawWaterTank(x, y);
    }
  }

  drawCropStatus(farm, x, y) {
    const centerX = x + this.tileSize / 2;
    const centerY = y + this.tileSize / 2;
    const radius = this.tileSize / 4;

    // Health indicator circle
    const healthPercent = farm.cropHealth / 100;
    this.ctx.fillStyle = `hsla(${healthPercent * 120}, 100%, 50%, 0.7)`;
    this.ctx.beginPath();
    this.ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
    this.ctx.fill();

    // Moisture bar
    const barWidth = this.tileSize * 0.6;
    const barHeight = 3;
    const moisturePercent = farm.soilMoisture / 100;

    this.ctx.fillStyle = '#444444';
    this.ctx.fillRect(
      x + (this.tileSize - barWidth) / 2,
      y + this.tileSize - 6,
      barWidth,
      barHeight
    );

    this.ctx.fillStyle = `hsl(${moisturePercent * 240}, 100%, 50%)`;
    this.ctx.fillRect(
      x + (this.tileSize - barWidth) / 2,
      y + this.tileSize - 6,
      barWidth * moisturePercent,
      barHeight
    );
  }

  drawHouse(x, y) {
    const roadSize = this.tileSize / 3;
    const roofColor = '#8B4513';
    const wallColor = '#D2691E';

    // Roof (triangle)
    this.ctx.fillStyle = roofColor;
    this.ctx.beginPath();
    this.ctx.moveTo(x + this.tileSize / 2, y + 4);
    this.ctx.lineTo(x + 4, y + this.tileSize / 2);
    this.ctx.lineTo(x + this.tileSize - 4, y + this.tileSize / 2);
    this.ctx.fill();

    // Walls
    this.ctx.fillStyle = wallColor;
    this.ctx.fillRect(x + 4, y + this.tileSize / 2, this.tileSize - 8, this.tileSize / 2 - 4);

    // Door
    this.ctx.fillStyle = '#654321';
    this.ctx.fillRect(
      x + this.tileSize / 2 - 3,
      y + this.tileSize / 2 + 4,
      6,
      this.tileSize / 2 - 8
    );
  }

  drawWaterTank(x, y) {
    const tankSize = this.tileSize * 0.6;
    const startX = x + (this.tileSize - tankSize) / 2;
    const startY = y + (this.tileSize - tankSize) / 2;

    this.ctx.fillStyle = '#1E40AF';
    this.ctx.fillRect(startX, startY, tankSize, tankSize);
    this.ctx.strokeStyle = '#0C4A6E';
    this.ctx.lineWidth = 2;
    this.ctx.strokeRect(startX, startY, tankSize, tankSize);

    // Water wave animation
    this.ctx.fillStyle = '#3B82F6';
    const waveHeight = Math.sin(Date.now() / 500) * 2 + 4;
    this.ctx.fillRect(startX, startY + tankSize - waveHeight, tankSize, waveHeight);
  }

  drawIrrigationAnimation(farm) {
    const x = farm.x * this.tileSize + this.tileSize / 2;
    const y = farm.y * this.tileSize + this.tileSize / 2;

    // Particle emission
    for (let i = 0; i < 2; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = Math.random() * 0.5 + 0.5;
      this.particleSystem.add(
        x,
        y,
        Math.cos(angle) * speed,
        Math.sin(angle) * speed,
        1500,
        '#4A90E2'
      );
    }

    // Draw water droplet icon
    this.ctx.fillStyle = '#4A90E2';
    this.ctx.font = '12px Arial';
    this.ctx.fillText('💧', x - 6, y + 4);
  }

  drawFarmer(farmer) {
    const x = farmer.x * this.tileSize;
    const y = farmer.y * this.tileSize;
    const size = this.tileSize * 0.7;
    const offsetX = (this.tileSize - size) / 2;
    const offsetY = (this.tileSize - size) / 2;

    const animFrame = farmer.getAnimationFrame();

    // Body color
    this.ctx.fillStyle = '#FF6B6B';
    this.ctx.fillRect(x + offsetX + 2, y + offsetY + 8, size - 4, size - 10);

    // Head
    this.ctx.fillStyle = '#FFCB9A';
    this.ctx.beginPath();
    this.ctx.arc(x + this.tileSize / 2, y + offsetY + 4, 3, 0, Math.PI * 2);
    this.ctx.fill();

    // Simple walking animation
    const legOffset = Math.sin(animFrame) * 1;
    this.ctx.fillStyle = '#4A4A4A';
    this.ctx.fillRect(x + offsetX + 3, y + offsetY + 14 + legOffset, 2, 4);
    this.ctx.fillRect(x + size + offsetX - 5, y + offsetY + 14 - legOffset, 2, 4);
  }

  drawUIOverlay(weather) {
    // Simple weather indicator in corner
    this.ctx.fillStyle = '#000000';
    this.ctx.globalAlpha = 0.7;
    this.ctx.fillRect(4, 4, 80, 20);
    this.ctx.globalAlpha = 1;

    this.ctx.fillStyle = '#FFFFFF';
    this.ctx.font = 'bold 12px Arial';
    this.ctx.fillText(weather.getWeatherEmoji() + ' ' + weather.currentWeather, 8, 16);
  }
}

// ============== PARTICLE SYSTEM ==============
class ParticleSystem {
  constructor() {
    this.particles = [];
  }

  add(x, y, vx, vy, lifetime, color) {
    this.particles.push({
      x,
      y,
      vx,
      vy,
      lifetime,
      maxLifetime: lifetime,
      color,
    });
  }

  update() {
    this.particles = this.particles.filter((p) => {
      p.x += p.vx;
      p.y += p.vy;
      p.lifetime -= 16; // Assume ~60fps
      p.vy += 0.1; // Gravity
      return p.lifetime > 0;
    });
  }

  draw(ctx, tileSize) {
    this.particles.forEach((p) => {
      const alpha = p.lifetime / p.maxLifetime;
      ctx.fillStyle = p.color;
      ctx.globalAlpha = alpha;
      ctx.beginPath();
      ctx.arc(p.x + tileSize / 2, p.y + tileSize / 2, 1, 0, Math.PI * 2);
      ctx.fill();
      ctx.globalAlpha = 1;
    });
  }
}

// ============== MAIN FARMING SIMULATION ==============
class FarmingSimulation {
  constructor(containerId, mapWidth, mapHeight, tileSize = 32) {
    this.container = document.getElementById(containerId);
    if (!this.container) throw new Error(`Container with id "${containerId}" not found`);

    this.mapWidth = mapWidth;
    this.mapHeight = mapHeight;
    this.tileSize = tileSize;
    this.farms = [];
    this.farmer = null;
    this.weather = new WeatherSystem();
    this.irrigationController = null;
    this.renderer = null;
    this.running = false;
    this.selectedFarm = null;
    this.lastFrameTime = 0;
    this.onFarmInfoCallback = null;

    this.init();
  }

  init() {
    this.createFarmGrid();
    this.setupCanvas();
    this.farmer = new FarmerController(
      Math.floor(this.mapWidth / 2),
      Math.floor(this.mapHeight / 2),
      this.tileSize
    );
    this.irrigationController = new IrrigationController(this.farms);
    this.renderer = new GameRenderer(this.canvas, this.tileSize);

    // Setup interaction
    document.addEventListener('keydown', (e) => {
      if (e.key.toLowerCase() === 'e') {
        this.interactWithFarm();
      }
    });

    this.start();
  }

  createFarmGrid() {
    this.farms = [];
    const centerX = Math.floor(this.mapWidth / 2);
    const centerY = Math.floor(this.mapHeight / 2);

    for (let x = 0; x < this.mapWidth; x++) {
      for (let y = 0; y < this.mapHeight; y++) {
        let tileType = 'farmland';

        // Place house at center
        if (x === centerX && y === centerY) {
          tileType = 'house';
        }
        // Place water tank
        else if (x === Math.floor(this.mapWidth / 4) && y === Math.floor(this.mapHeight / 4)) {
          tileType = 'water';
        }
        // Place paths
        else if (x === centerX || y === centerY) {
          tileType = 'path';
        }

        const tile = new FarmTile(x, y, tileType);
        this.farms.push(tile);
      }
    }
  }

  setupCanvas() {
    this.canvas = document.createElement('canvas');
    this.canvas.id = 'farm-simulator-canvas';
    this.canvas.style.border = '3px solid #333';
    this.canvas.style.imageRendering = 'pixelated';
    this.canvas.style.imageRendering = 'crisp-edges';
    this.canvas.style.display = 'block';
    this.canvas.style.margin = '10px 0';
    this.container.appendChild(this.canvas);
  }

  start() {
    this.running = true;
    this.lastFrameTime = Date.now();
    this.gameLoop();
  }

  stop() {
    this.running = false;
  }

  gameLoop = () => {
    if (!this.running) return;

    const currentTime = Date.now();
    const deltaTime = currentTime - this.lastFrameTime;
    this.lastFrameTime = currentTime;

    // Update
    this.farmer.update(this.farms, this.mapWidth, this.mapHeight);
    this.weather.update(deltaTime);

    this.farms.forEach((farm) => {
      farm.update(deltaTime, this.weather.currentWeather);
    });

    // Render
    this.renderer.render(this.farms, this.farmer, this.weather, this.mapWidth, this.mapHeight);

    // Update dashboard
    this.updateDashboard();

    requestAnimationFrame(this.gameLoop);
  };

  interactWithFarm() {
    const nearbyFarm = this.farmer.getNearbyFarm(this.farms);
    if (nearbyFarm) {
      this.selectedFarm = nearbyFarm;
      this.showFarmInfo(nearbyFarm);
    }
  }

  showFarmInfo(farm) {
    if (this.onFarmInfoCallback) {
      this.onFarmInfoCallback({
        id: farm.id,
        soilMoisture: Math.round(farm.soilMoisture),
        cropHealth: Math.round(farm.cropHealth),
        irrigationStatus: farm.irrigationActive ? 'Active' : 'Inactive',
      });
    } else {
      console.log('Farm Info:', {
        id: farm.id,
        soilMoisture: Math.round(farm.soilMoisture),
        cropHealth: Math.round(farm.cropHealth),
        irrigationStatus: farm.irrigationActive ? 'Active' : 'Inactive',
      });
    }
  }

  updateDashboard() {
    const dashboard = document.getElementById('farm-dashboard');
    if (!dashboard) return;

    const totalFarms = this.irrigationController.getTotalFarms();
    const farmsNeedingIrrigation = this.irrigationController.getFarmsNeedingIrrigation();
    const avgMoisture = this.irrigationController.getAveragesoilMoisture();

    dashboard.innerHTML = `
      <div class="dashboard-item">
        <span class="label">Weather:</span>
        <span class="value">${this.weather.getWeatherEmoji()} ${this.weather.currentWeather}</span>
      </div>
      <div class="dashboard-item">
        <span class="label">Total Farms:</span>
        <span class="value">${totalFarms}</span>
      </div>
      <div class="dashboard-item">
        <span class="label">Needs Irrigation:</span>
        <span class="value farm-alert">${farmsNeedingIrrigation}</span>
      </div>
      <div class="dashboard-item">
        <span class="label">Avg Moisture:</span>
        <span class="value">${avgMoisture}%</span>
      </div>
    `;
  }

  setFarmInfoCallback(callback) {
    this.onFarmInfoCallback = callback;
  }

  getFarmStats() {
    return {
      totalFarms: this.irrigationController.getTotalFarms(),
      farmsNeedingIrrigation: this.irrigationController.getFarmsNeedingIrrigation(),
      averageMoisture: this.irrigationController.getAveragesoilMoisture(),
      currentWeather: this.weather.currentWeather,
    };
  }
}

// Export for ES6 modules (Vite/Svelte)
export default FarmingSimulation;
