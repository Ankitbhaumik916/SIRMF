<script>
  import { onMount, onDestroy } from 'svelte';
  import FarmingSimulation from '../utils/farmingSimulation.js';

  export let userLandArea = 100; // Land area in square units
  export let onFarmSelect = null;
  export let onStatsUpdate = null;

  let simulation = null;
  let containerElement;
  let farmInfoPopup = null;

  onMount(() => {
    // Wait for next tick to ensure DOM is ready
    setTimeout(() => {
      if (!containerElement) {
        console.error('Container element not found');
        return;
      }

      try {
        // Calculate map dimensions based on user's land area
        // Assuming each tile represents ~10 sq units
        const tilesPerSide = Math.max(6, Math.ceil(Math.sqrt(userLandArea / 10)));
        
        console.log('Initializing simulation with:', {
          landArea: userLandArea,
          tilesPerSide,
          containerId: containerElement.id
        });
        
        // Initialize simulation
        simulation = new FarmingSimulation(
          containerElement.id,
          tilesPerSide,
          tilesPerSide,
          32 // tileSize in pixels
        );

        // Set callback for farm selection
        simulation.setFarmInfoCallback((farmInfo) => {
          farmInfoPopup = farmInfo;
          if (onFarmSelect) {
            onFarmSelect(farmInfo);
          }
        });

        simulation.setFarmStatsCallback((stats) => {
          if (onStatsUpdate) {
            onStatsUpdate(stats);
          }
        });
      } catch (error) {
        console.error('Error initializing simulation:', error);
      }
    }, 100);

    return () => {
      if (simulation) {
        simulation.stop();
      }
    };
  });

  onDestroy(() => {
    if (simulation) {
      simulation.stop();
    }
  });

  function closeFarmInfo() {
    farmInfoPopup = null;
  }

  function handleKeyDown(event) {
    if (event.key === 'Escape') {
      closeFarmInfo();
    }
  }
</script>

<div class="farming-simulation-container">
  <div class="simulation-wrapper">
    <div bind:this={containerElement} id="farm-simulator" class="canvas-container" />
    <div id="farm-dashboard" class="dashboard" />
  </div>

  {#if farmInfoPopup}
    <div 
      class="farm-info-popup" 
      on:click={closeFarmInfo}
      on:keydown={handleKeyDown}
      role="presentation"
    >
      <div class="popup-content" role="dialog" aria-modal="true">
        <button class="close-btn" on:click={closeFarmInfo}>×</button>
        <h3>Farm Details</h3>
        <div class="info-row">
          <span class="label">Farm ID:</span>
          <span class="value">{farmInfoPopup.id}</span>
        </div>
        <div class="info-row">
          <span class="label">Soil Moisture:</span>
          <span class="value">{farmInfoPopup.soilMoisture}%</span>
          <div class="progress-bar">
            <div
              class="progress-fill"
              style="width: {farmInfoPopup.soilMoisture}%; background-color: hsl({farmInfoPopup.soilMoisture *
                240 /
                100}, 100%, 50%);"
            />
          </div>
        </div>
        <div class="info-row">
          <span class="label">Crop Health:</span>
          <span class="value">{farmInfoPopup.cropHealth}%</span>
          <div class="progress-bar">
            <div
              class="progress-fill"
              style="width: {farmInfoPopup.cropHealth}%; background-color: hsl({farmInfoPopup.cropHealth *
                120 /
                100}, 100%, 50%);"
            />
          </div>
        </div>
        <div class="info-row">
          <span class="label">Irrigation Status:</span>
          <span class="value status-{farmInfoPopup.irrigationStatus.toLowerCase()}">
            {farmInfoPopup.irrigationStatus}
          </span>
        </div>
        <p class="hint">Click outside or press ESC to close</p>
      </div>
    </div>
  {/if}
</div>

<style>
  .farming-simulation-container {
    width: 100%;
    padding: 20px;
    background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
    border-radius: 8px;
  }

  .simulation-wrapper {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
  }

  .canvas-container {
    flex: 1;
    min-width: 300px;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #fff;
    border-radius: 8px;
    padding: 10px;
  }

  :global(#farm-simulator-canvas) {
    border: 3px solid #333 !important;
    image-rendering: pixelated;
    image-rendering: crisp-edges;
    display: block;
    margin: auto;
  }

  .dashboard {
    min-width: 250px;
    background: white;
    border: 2px solid #333;
    border-radius: 8px;
    padding: 15px;
    display: flex;
    flex-direction: column;
    gap: 15px;
  }

  :global(.dashboard-item) {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    background: #f9f9f9;
    border-radius: 4px;
    border-left: 3px solid #4A90E2;
  }

  :global(.dashboard-item .label) {
    font-weight: bold;
    color: #333;
  }

  :global(.dashboard-item .value) {
    font-size: 1.2em;
    color: #0066cc;
    font-weight: bold;
  }

  :global(.dashboard-item .farm-alert) {
    color: #ff6b6b;
    background: #ffe6e6;
    padding: 2px 8px;
    border-radius: 4px;
  }

  .farm-info-popup {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.6);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .popup-content {
    background: white;
    border: 3px solid #333;
    border-radius: 8px;
    padding: 20px;
    max-width: 400px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    position: relative;
    animation: popupSlide 0.3s ease-out;
  }

  @keyframes popupSlide {
    from {
      opacity: 0;
      transform: scale(0.8);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }

  .close-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    background: #ff6b6b;
    color: white;
    border: none;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    cursor: pointer;
    font-size: 1.5em;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .close-btn:hover {
    background: #ff5252;
  }

  .popup-content h3 {
    margin-top: 0;
    margin-bottom: 15px;
    color: #333;
    font-size: 1.3em;
    border-bottom: 2px solid #eee;
    padding-bottom: 10px;
  }

  .info-row {
    margin-bottom: 15px;
    display: flex;
    flex-direction: column;
    gap: 5px;
  }

  .info-row .label {
    font-weight: bold;
    color: #555;
    font-size: 0.9em;
  }

  .info-row .value {
    font-size: 1.1em;
    color: #0066cc;
    font-weight: bold;
  }

  .progress-bar {
    width: 100%;
    height: 20px;
    background: #e0e0e0;
    border-radius: 4px;
    overflow: hidden;
    border: 1px solid #999;
  }

  .progress-fill {
    height: 100%;
    transition: width 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 0.8em;
    font-weight: bold;
  }

  .status-active {
    color: #22c55e;
    background: #f0fdf4;
    padding: 4px 8px;
    border-radius: 4px;
    display: inline-block;
  }

  .status-inactive {
    color: #ef4444;
    background: #fef2f2;
    padding: 4px 8px;
    border-radius: 4px;
    display: inline-block;
  }

  .hint {
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px solid #eee;
    font-size: 0.85em;
    color: #999;
    text-align: center;
  }

  @media (max-width: 768px) {
    .simulation-wrapper {
      flex-direction: column;
    }

    .dashboard {
      min-width: 100%;
    }

    .popup-content {
      max-width: 90vw;
      max-height: 90vh;
      overflow-y: auto;
    }
  }
</style>
