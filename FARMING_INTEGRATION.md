# Farming Simulation Integration Guide

## Overview

The Pixel-Art Precision Farming Simulation is a modular, self-contained component that simulates a pixel-art style farm with dynamic crop management, weather effects, and irrigation systems.

## Files Created

1. **src/utils/farmingSimulation.js** - Core simulation engine (non-framework dependent)
2. **src/components/FarmingSimulation.svelte** - Svelte wrapper component
3. **FARMING_INTEGRATION.md** - This integration guide

## Quick Start

### Option 1: Use the Svelte Component (Recommended for this project)

In any of your Svelte pages, import and use the component:

```svelte
<script>
  import FarmingSimulation from '../components/FarmingSimulation.svelte';
  import { authStore } from '../stores/authStore';

  let selectedFarmInfo = null;

  function handleFarmSelect(farmInfo) {
    selectedFarmInfo = farmInfo;
    console.log('Farm selected:', farmInfo);
    // You can save this data to your store or send it to the backend
  }
</script>

<div class="farm-info-page">
  <h1>Farm Information & Management</h1>
  
  <!-- Get user land area from auth store -->
  <FarmingSimulation 
    userLandArea={$authStore.user.farmSize || 100}
    onFarmSelect={handleFarmSelect}
  />
  
  {#if selectedFarmInfo}
    <div class="selected-farm-display">
      <p>Currently viewing farm: {selectedFarmInfo.id}</p>
    </div>
  {/if}
</div>

<style>
  .farm-info-page {
    padding: 20px;
  }
</style>
```

### Option 2: Add to Existing Profile Page

Modify `src/pages/Profile.svelte`:

```svelte
<script>
  // ... existing imports ...
  import FarmingSimulation from '../components/FarmingSimulation.svelte';

  // ... existing code ...
</script>

<div class="profile-container">
  {#if !isEditing}
    <!-- Existing profile display code -->
    
    {#if activeTab === 'farm-simulation'}
      <div class="tab-content">
        <h3>Farm Simulation</h3>
        <FarmingSimulation 
          userLandArea={$authStore.user.farmSize || 100}
          onFarmSelect={(info) => console.log(info)}
        />
      </div>
    {/if}
  {/if}
</div>
```

### Option 3: Add to Dashboard Page

Modify `src/pages/Dashboard.svelte`:

```svelte
<script>
  import FarmingSimulation from '../components/FarmingSimulation.svelte';
  // ... other imports ...
</script>

<section class="farming-section">
  <h2>Precision Farming Simulation</h2>
  <FarmingSimulation 
    userLandArea={userFarmSize}
    onFarmSelect={handleFarmSelect}
  />
</section>
```

## Component Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `userLandArea` | number | 100 | Farm size in square units. Automatically scales the simulation grid (each tile ≈ 10 sq units) |
| `onFarmSelect` | function | null | Callback function when user interacts with a farm tile (press E when near a farm) |

## How It Works

### User Interaction

- **Movement**: Use `W/A/S/D` or Arrow keys to move the farmer
- **Interaction**: Press `E` when near a farmland tile to view farm details
- **Details Popup**: Shows soil moisture, crop health, and irrigation status

### Simulation Features

#### Each Farm Tile Has:
- **Soil Moisture** (0-100%): Decreases via evaporation, increases via irrigation/rain
- **Crop Health** (0-100%): Based on soil moisture levels (optimal: 40-70%)
- **Irrigation Status**: Auto-activates when moisture < 35%, auto-deactivates when > 70%

#### Weather System:
- **Sunny** ☀️: Fast moisture loss (12 units/sec)
- **Cloudy** ☁️: Balanced loss (6 units/sec)
- **Rainy** 🌧️: Slow loss (2 units/sec) + natural moisture gain (8 units/sec)
- Weather changes randomly every 5 seconds

#### Dashboard Displays:
- Current weather condition
- Total number of farmland tiles
- Number of farms currently needing irrigation
- Average soil moisture across all farms

### Land Area Scaling

The simulation automatically calculates grid size based on `userLandArea`:

```
Grid PER SIDE = Math.ceil(√(userLandArea / 10))
```

**Examples:**
- 100 sq units → 10×10 grid = 100 tiles
- 400 sq units → 20×20 grid = 400 tiles
- 50 sq units → 7×7 grid = 49 tiles

**Each tile represents approximately 10 square units.**

## Color Indicators

### Soil Moisture (Visual on farm tiles):
- **Brown** (#8B6914): Dry soil (< 30%)
- **Green** (#2D5016): Healthy soil (30-75%)
- **Dark Blue** (#1E3A8A): Overwatered (> 75%)

### Farm Elements:
- **Brown/Tan**: Farmer house (center)
- **Blue**: Water tank/irrigation source
- **Brown tan**: Dirt paths
- **Variable colors**: Farm plots (based on moisture)

## Advanced: Directly Using JavaScript

If you need to use the simulation outside of Svelte, you can use the raw JavaScript class:

```javascript
// Import the class
import FarmingSimulation from './src/utils/farmingSimulation.js';

// Initialize with a container div
const sim = new FarmingSimulation(
  'container-id',  // HTML element ID
  12,              // Map width in tiles
  12,              // Map height in tiles
  32               // Pixel size per tile
);

// Set farm info callback
sim.setFarmInfoCallback((farmInfo) => {
  console.log(farmInfo);
  // {
  //   id: "farm_3_5",
  //   soilMoisture: 65,
  //   cropHealth: 82,
  //   irrigationStatus: "Inactive"
  // }
});

// Get current stats
const stats = sim.getFarmStats();
console.log(stats);
// {
//   totalFarms: 132,
//   farmsNeedingIrrigation: 8,
//   averageMoisture: 58,
//   currentWeather: "rainy"
// }

// Stop simulation
sim.stop();
```

## Performance Considerations

- **FPS**: Runs at ~60 FPS using requestAnimationFrame
- **Memory**: ~10-50MB depending on grid size
- **CPU Usage**: Minimal (particle system and weather updates)

Tested grids:
- 10×10 tiles (100 farms) - negligible impact
- 20×20 tiles (400 farms) - smooth performance
- 30×30 tiles (900 farms) - still smooth

## Customization

### Change Grid Size Manually:
```svelte
<FarmingSimulation userLandArea={250} />
<!-- Results in ~16×16 grid (250 farms) -->
```

### Adjust Tile Size:
Edit `FarmingSimulation.svelte`, line with `tileSize` parameter:
```javascript
simulation = new FarmingSimulation(
  containerElement.id,
  tilesPerSide,
  tilesPerSide,
  48  // Change this for larger/smaller tiles (default: 32)
);
```

### Modify Simulation Parameters:

Edit `src/utils/farmingSimulation.js`:

1. **Evaporation rates** (lines ~35-45):
   ```javascript
   getEvaporationRate(weatherState) {
     switch (weatherState) {
       case 'sunny':
         return 12;  // Increase for faster drying
       // ...
     }
   }
   ```

2. **Auto-irrigation thresholds** (lines ~52-54):
   ```javascript
   if (this.soilMoisture < 35) this.irrigationActive = true;
   if (this.soilMoisture > 70) this.irrigationActive = false;
   ```

3. **Weather change duration** (line ~138):
   ```javascript
   this.weatherChangeDuration = 5000; // 5 seconds, adjust as needed
   ```

4. **Farmer movement speed** (line ~180):
   ```javascript
   const moveSpeed = 0.1; // Tiles per frame
   ```

## Responsive Design

The component is fully responsive:
- On desktop: Canvas and dashboard side-by-side
- On tablets: Stacked vertically
- On mobile: Full-width with scrollable content

## Browser Compatibility

- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support
- Requires: HTML5 Canvas, ES6 JavaScript, CSS Grid

## Troubleshooting

### Canvas Not Rendering
- Ensure container div exists before component mounts
- Check browser console for errors
- Verify JavaScript is not minified in a way that breaks the code

### Simulation Running Slowly
- Reduce grid size (lower `userLandArea`)
- Check browser DevTools Performance tab
- Close other CPU-intensive applications

### Interactions Not Working
- Ensure canvas has focus (click on it first)
- Check console for keyboard event listeners
- Verify ESC key not prevented by other code

## Data Persistence

Currently, the simulation runs in-memory and resets on page reload. To persist data:

```svelte
<script>
  let simulation;
  
  function saveFarmData() {
    const stats = simulation.getFarmStats();
    // Save to localStorage or backend
    localStorage.setItem('farmData', JSON.stringify(stats));
  }

  function loadFarmData() {
    const saved = localStorage.getItem('farmData');
    if (saved) {
      // Restore state (would require modifying simulation.js)
      const data = JSON.parse(saved);
    }
  }
</script>
```

## Future Enhancements

Possible additions:
- Save/load simulation state
- Fertilizer and pest management
- Seasonal changes
- Underground water table system
- Market prices for crops
- Multiplayer local simulation
- Sound effects and music

## Support & Questions

For issues, check:
1. Browser console for errors
2. Canvas dimensions (should match grid × tileSize)
3. Container element ID matches initialization
4. No conflicting CSS transforms on parent elements
