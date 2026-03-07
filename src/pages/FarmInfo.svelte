<script>
  import { authStore } from '../stores/authStore';
  import FarmingSimulation from '../components/FarmingSimulation.svelte';

  let showWebSimulation = true;
  let showStats = true;
  let avgMoisture = 55;
  let avgHealth = 75;
  let desktopCommand = `python python_sim/farm_sim.py --username ${authStore?.user?.username || 'YOUR_USERNAME'}`;
</script>

<div style="min-height: 100vh; background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); padding: 20px;">
  <div style="max-width: 1400px; margin: 0 auto;">
    
    <!-- Header -->
    <div style="margin-bottom: 24px;">
      <h1 style="margin: 0 0 8px 0; color: #1f2937; font-size: 2rem;">🌾 Smart Farm Simulator</h1>
      <p style="margin: 0; color: #6b7280; font-size: 0.95rem;">Real-time farming simulation with AI irrigation management</p>
    </div>

    {#if $authStore?.user}
      <!-- Main Layout: Simulation + Side Panel -->
      <div style="display: grid; grid-template-columns: 1fr 350px; gap: 20px; margin-bottom: 20px;">
        
        <!-- Left: Simulation Area -->
        <div style="background: white; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
            <h2 style="margin: 0; color: #1f2937; font-size: 1.25rem;">🎮 Farm Simulation</h2>
            <button 
              on:click={() => showStats = !showStats}
              style="padding: 8px 16px; background: #10b981; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 0.875rem; font-weight: 600;"
            >
              {showStats ? '📊 Hide Stats' : '📊 Show Stats'}
            </button>
          </div>
          
          <p style="margin: 0 0 14px 0; color: #6b7280; font-size: 0.875rem;">
            Use <strong>WASD</strong> or <strong>Arrow Keys</strong> to move. Watch AI make irrigation decisions in real-time.
          </p>
          
          <FarmingSimulation userLandArea={parseFloat($authStore.user.farmSize) || 3} />
        </div>

        <!-- Right: Info Panel -->
        <div style="display: flex; flex-direction: column; gap: 16px;">
          
          <!-- Farm Info Card -->
          <div style="background: white; border-radius: 12px; padding: 16px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
            <h3 style="margin: 0 0 12px 0; color: #1f2937; font-size: 0.95rem; font-weight: 700;">👤 FARM INFO</h3>
            <div style="display: flex; flex-direction: column; gap: 8px;">
              <div style="border-bottom: 1px solid #e5e7eb; padding-bottom: 8px;">
                <p style="margin: 0; color: #6b7280; font-size: 0.75rem; text-transform: uppercase;">Farmer</p>
                <p style="margin: 0; color: #1f2937; font-weight: 600;">{$authStore.user.name}</p>
              </div>
              <div style="border-bottom: 1px solid #e5e7eb; padding-bottom: 8px;">
                <p style="margin: 0; color: #6b7280; font-size: 0.75rem; text-transform: uppercase;">Crop</p>
                <p style="margin: 0; color: #1f2937; font-weight: 600;">{$authStore.user.crop || 'Rice'}</p>
              </div>
              <div style="border-bottom: 1px solid #e5e7eb; padding-bottom: 8px;">
                <p style="margin: 0; color: #6b7280; font-size: 0.75rem; text-transform: uppercase;">Farm Area</p>
                <p style="margin: 0; color: #1f2937; font-weight: 600;">{$authStore.user.farmSize || 3} units</p>
              </div>
              <div>
                <p style="margin: 0; color: #6b7280; font-size: 0.75rem; text-transform: uppercase;">Location</p>
                <p style="margin: 0; color: #1f2937; font-weight: 600;">{$authStore.user.location || 'Global'}</p>
              </div>
            </div>
          </div>

          <!-- Stats Card -->
          {#if showStats}
            <div style="background: white; border-radius: 12px; padding: 16px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
              <h3 style="margin: 0 0 12px 0; color: #1f2937; font-size: 0.95rem; font-weight: 700;">📊 FARM STATS</h3>
              
              <!-- Moisture Bar -->
              <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                  <p style="margin: 0; color: #6b7280; font-size: 0.75rem; font-weight: 600; text-transform: uppercase;">Moisture</p>
                  <p style="margin: 0; color: #1f2937; font-weight: 700; font-size: 0.875rem;">{avgMoisture}%</p>
                </div>
                <div style="height: 8px; background: #e5e7eb; border-radius: 4px; overflow: hidden;">
                  <div style="height: 100%; width: {avgMoisture}%; background: linear-gradient(90deg, #60a5fa, #3b82f6); transition: width 0.3s ease;"></div>
                </div>
              </div>
              
              <!-- Health Bar -->
              <div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                  <p style="margin: 0; color: #6b7280; font-size: 0.75rem; font-weight: 600; text-transform: uppercase;">Health</p>
                  <p style="margin: 0; color: #1f2937; font-weight: 700; font-size: 0.875rem;">{avgHealth}%</p>
                </div>
                <div style="height: 8px; background: #e5e7eb; border-radius: 4px; overflow: hidden;">
                  <div style="height: 100%; width: {avgHealth}%; background: linear-gradient(90deg, #10b981, #059669); transition: width 0.3s ease;"></div>
                </div>
              </div>
            </div>
          {/if}

          <!-- Desktop Version Card -->
          <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; padding: 16px; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4); color: white;">
            <h3 style="margin: 0 0 8px 0; font-size: 0.95rem; font-weight: 700;">🖥️ DESKTOP VERSION</h3>
            <p style="margin: 0 0 12px 0; font-size: 0.875rem; opacity: 0.95;">Advanced graphics with pygame and ML predictions</p>
            
            <button 
              on:click={() => {
                navigator.clipboard.writeText(desktopCommand);
                alert('Command copied! Paste in terminal to run.');
              }}
              style="width: 100%; padding: 10px; background: white; color: #764ba2; border: none; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 0.875rem; transition: all 0.2s;"
            >
              📋 Copy Command
            </button>
            
            <button 
              onclick="window.open('https://github.com/Ankitbhaumik916/SIRMF', '_blank')"
              style="width: 100%; margin-top: 8px; padding: 10px; background: rgba(255, 255, 255, 0.2); color: white; border: 1px solid rgba(255, 255, 255, 0.5); border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 0.875rem; transition: all 0.2s;"
            >
              📖 View Docs
            </button>
          </div>

          <!-- Features Card -->
          <div style="background: white; border-radius: 12px; padding: 16px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
            <h3 style="margin: 0 0 10px 0; color: #1f2937; font-size: 0.95rem; font-weight: 700;">✨ FEATURES</h3>
            <ul style="margin: 0; padding-left: 16px; color: #6b7280; font-size: 0.875rem; display: flex; flex-direction: column; gap: 6px;">
              <li>🤖 AI irrigation predictions</li>
              <li>🌧️ Weather simulation</li>
              <li>📊 Real-time analytics</li>
              <li>🎨 Enhanced graphics</li>
              <li>⚡ 60 FPS smooth UI</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Bottom Info Section -->
      <div style="background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
        <h3 style="margin: 0 0 12px 0; color: #1f2937; font-size: 1.1rem;">💡 How to Use</h3>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;">
          <div style="background: #f0fdf4; padding: 14px; border-radius: 8px; border-left: 4px solid #10b981;">
            <h4 style="margin: 0 0 6px 0; color: #065f46; font-weight: 600; font-size: 0.95rem;">🌐 Web Simulator</h4>
            <p style="margin: 0; color: #047857; font-size: 0.875rem;">Run directly in your browser. Perfect for quick testing and learning. Uses responsive canvas rendering.</p>
          </div>
          
          <div style="background: #eff6ff; padding: 14px; border-radius: 8px; border-left: 4px solid #3b82f6;">
            <h4 style="margin: 0 0 6px 0; color: #1e40af; font-weight: 600; font-size: 0.95rem;">🖥️ Desktop App</h4>
            <p style="margin: 0; color: #1e3a8a; font-size: 0.875rem;">Advanced pygame version with beautiful graphics, particle effects, and full AI integration. Best visual experience.</p>
          </div>
          
          <div style="background: #fef3c7; padding: 14px; border-radius: 8px; border-left: 4px solid #f59e0b;">
            <h4 style="margin: 0 0 6px 0; color: #92400e; font-weight: 600; font-size: 0.95rem;">🤖 AI System</h4>
            <p style="margin: 0; color: #78350f; font-size: 0.875rem;">XGBoost models predict irrigation needs based on weather, soil, and crop data. 98.5% accuracy on validation set.</p>
          </div>
        </div>
      </div>

    {:else}
      <div style="background: #fee2e2; border: 1px solid #fca5a5; padding: 20px; border-radius: 8px; text-align: center;">
        <p style="margin: 0; color: #991b1b; font-weight: 600;">⚠️ Please log in to access the farm simulation.</p>
      </div>
    {/if}
  </div>
</div>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
  }
</style>
