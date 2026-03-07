<script>
  import { authStore } from '../stores/authStore';
  import FarmingSimulation from '../components/FarmingSimulation.svelte';

  let showWebSimulation = true;
  let showPythonInstructions = false;
</script>

<div style="padding: 30px; background: white; min-height: 100vh; color: #1f2937;">
  <h1 style="margin: 0 0 12px 0;">🌾 Farm Simulation</h1>
  <p style="margin: 0 0 20px 0; color: #4b5563;">Interactive farming simulation with real-time irrigation management</p>

  {#if $authStore?.user}
    <!-- Tab Navigation -->
    <div style="display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 2px solid #e5e7eb;">
      <button 
        on:click={() => { showWebSimulation = true; showPythonInstructions = false; }}
        style="padding: 10px 20px; border: none; background: {showWebSimulation ? '#10b981' : 'transparent'}; color: {showWebSimulation ? 'white' : '#6b7280'}; cursor: pointer; border-radius: 6px 6px 0 0; font-weight: 600; transition: all 0.2s;"
      >
        🌐 Web Simulation
      </button>
      <button 
        on:click={() => { showWebSimulation = false; showPythonInstructions = true; }}
        style="padding: 10px 20px; border: none; background: {showPythonInstructions ? '#10b981' : 'transparent'}; color: {showPythonInstructions ? 'white' : '#6b7280'}; cursor: pointer; border-radius: 6px 6px 0 0; font-weight: 600; transition: all 0.2s;"
      >
        🖥️ Desktop Simulation
      </button>
    </div>

    <!-- Farmer Profile -->
    <div style="background: #e8f5e9; padding: 18px; border-radius: 8px; margin-bottom: 20px;">
      <h2 style="margin: 0 0 8px 0;">👤 Farmer Profile</h2>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px;">
        <div>
          <p style="margin: 0; color: #6b7280; font-size: 0.875rem;">Name</p>
          <p style="margin: 0; font-weight: 600; color: #1f2937;">{$authStore.user.name}</p>
        </div>
        <div>
          <p style="margin: 0; color: #6b7280; font-size: 0.875rem;">Farm Size</p>
          <p style="margin: 0; font-weight: 600; color: #1f2937;">{$authStore.user.farmSize || 100} hectares</p>
        </div>
        <div>
          <p style="margin: 0; color: #6b7280; font-size: 0.875rem;">Crop</p>
          <p style="margin: 0; font-weight: 600; color: #1f2937;">{$authStore.user.crop || 'Rice'}</p>
        </div>
        <div>
          <p style="margin: 0; color: #6b7280; font-size: 0.875rem;">Location</p>
          <p style="margin: 0; font-weight: 600; color: #1f2937;">{$authStore.user.location || 'Not specified'}</p>
        </div>
      </div>
    </div>

    <!-- Web Simulation -->
    {#if showWebSimulation}
      <div style="background: white; border: 2px solid #e5e7eb; border-radius: 8px; padding: 20px; margin-bottom: 20px;">
        <h3 style="margin: 0 0 12px 0; color: #1f2937;">🎮 Interactive Web Simulation</h3>
        <p style="margin: 0 0 16px 0; color: #6b7280; font-size: 0.875rem;">
          Use <strong>WASD</strong> or <strong>Arrow Keys</strong> to move around your farm. Click on tiles to view details.
        </p>
        
        <FarmingSimulation userLandArea={parseFloat($authStore.user.farmSize) || 3} />
        
        <div style="margin-top: 16px; padding: 12px; background: #f0fdf4; border-radius: 6px; border-left: 4px solid #10b981;">
          <p style="margin: 0; color: #065f46; font-size: 0.875rem;">
            💡 <strong>Tips:</strong> Monitor soil moisture levels and crop health. Irrigation activates automatically when moisture drops below 35%.
          </p>
        </div>
      </div>
    {/if}

    <!-- Python Instructions -->
    {#if showPythonInstructions}
      <div style="background: #f9fafb; border: 2px solid #e5e7eb; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
        <h3 style="margin: 0 0 12px 0; color: #1f2937;">🖥️ Python Desktop Simulation</h3>
        <p style="margin: 0 0 12px 0; color: #6b7280;">
          Run the pygame-powered desktop simulation with enhanced graphics and features.
        </p>
        
        <div style="background: #111827; color: #e5e7eb; padding: 14px; border-radius: 6px; margin-bottom: 12px; overflow-x: auto;">
          <pre style="margin: 0; font-family: 'Courier New', monospace;">python python_sim/farm_sim.py --username {$authStore.user.username || 'Ankit22'}</pre>
        </div>
        
        <div style="background: #eff6ff; padding: 12px; border-radius: 6px; border-left: 4px solid #3b82f6;">
          <p style="margin: 0; color: #1e40af; font-size: 0.875rem;">
            ℹ️ The simulation automatically loads your farm data (size, crop, location) from the database.
          </p>
        </div>

        <div style="margin-top: 16px;">
          <h4 style="margin: 0 0 8px 0; color: #1f2937; font-size: 1rem;">Controls:</h4>
          <ul style="margin: 0; padding-left: 20px; color: #4b5563;">
            <li>Use <strong>WASD</strong> or <strong>Arrow Keys</strong> to navigate</li>
            <li>Click on farm tiles to inspect details</li>
            <li>Press <strong>ESC</strong> or <strong>Q</strong> to quit</li>
            <li>Toggle irrigation with <strong>I</strong> key (auto-managed by default)</li>
          </ul>
        </div>

        <div style="margin-top: 16px;">
          <h4 style="margin: 0 0 8px 0; color: #1f2937; font-size: 1rem;">Features:</h4>
          <ul style="margin: 0; padding-left: 20px; color: #4b5563;">
            <li>Real-time weather simulation (sunny, cloudy, rainy)</li>
            <li>Dynamic soil moisture and crop health tracking</li>
            <li>Automatic irrigation system</li>
            <li>Weather API integration (connects to project backend)</li>
            <li>Pixel-art graphics and smooth animations</li>
          </ul>
        </div>
      </div>
    {/if}

  {:else}
    <div style="background: #fef2f2; border: 1px solid #fecaca; padding: 18px; border-radius: 8px;">
      <p style="margin: 0; color: #991b1b;">⚠️ Please log in to access the farm simulation.</p>
    </div>
  {/if}
</div>
