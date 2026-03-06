<script>
  import { authStore } from '../stores/authStore';
</script>

<div style="padding: 30px; background: white; min-height: 100vh; color: #1f2937;">
  <h1 style="margin: 0 0 12px 0;">🌾 Farm Management</h1>
  <p style="margin: 0 0 20px 0; color: #4b5563;">Desktop simulation is now powered by Python + pygame.</p>

  {#if $authStore?.user}
    <div style="background: #e8f5e9; padding: 18px; border-radius: 8px; margin-bottom: 16px;">
      <h2 style="margin: 0 0 8px 0;">Farmer Profile</h2>
      <p style="margin: 4px 0;"><strong>Name:</strong> {$authStore.user.name}</p>
      <p style="margin: 4px 0;"><strong>Farm Size:</strong> {$authStore.user.farmSize || 100}</p>
      <p style="margin: 4px 0;"><strong>Crop:</strong> {$authStore.user.crop || 'Not specified'}</p>
      <p style="margin: 4px 0;"><strong>Username Key:</strong> {$authStore.user.username || 'Use username from data/users.json'}</p>
    </div>

    <div style="background: #f9fafb; border: 1px solid #e5e7eb; padding: 18px; border-radius: 8px;">
      <p style="margin: 0 0 10px 0;"><strong>Run the pygame simulator:</strong></p>
      <pre style="margin: 0; background: #111827; color: #e5e7eb; padding: 12px; border-radius: 6px; overflow: auto;">python python_sim/farm_sim.py --username {$authStore.user.username || 'Ankit22'}</pre>
      <p style="margin: 12px 0 0 0; color: #6b7280;">It automatically uses this farmer's land area and crop from <code>data/users.json</code>.</p>
    </div>
  {:else}
    <p>Please log in to see your farmer profile and run command.</p>
  {/if}
</div>
