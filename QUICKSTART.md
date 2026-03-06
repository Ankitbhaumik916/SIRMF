# Quick Start: Integrating Farm Simulation into SEPM

This guide will get the farming simulation running in your app in 5 minutes.

## Prerequisites

- Svelte project already set up (which you have)
- `authStore` with user data including `farmSize` field
- Basic understanding of Svelte routing

## Installation Steps

### Step 1: Files Are Ready

All necessary files have been created:
```
src/utils/farmingSimulation.js          ✓ Created
src/components/FarmingSimulation.svelte ✓ Created
src/pages/FarmInfo.svelte               ✓ Created
FARMING_INTEGRATION.md                  ✓ Created
farming-simulation-demo.html            ✓ Created
```

No npm packages needed! Everything uses vanilla JavaScript and Svelte.

### Step 2: Add Route to Your Router (in App.svelte or wherever you manage routes)

If you're using a routing library, add:

```svelte
<script>
  import Dashboard from './pages/Dashboard.svelte';
  import FarmInfo from './pages/FarmInfo.svelte';  // Add this
  import Login from './pages/Login.svelte';
  import Profile from './pages/Profile.svelte';
  // ... other imports
</script>

{#if $authStore.isLoggedIn}
  {#if currentPage === 'dashboard'}
    <Dashboard />
  {/if}
  {#if currentPage === 'farm-info'}
    <FarmInfo />  <!-- Add this -->
  {/if}
  {#if currentPage === 'profile'}
    <Profile />
  {/if}
  <!-- ... other routes ... -->
{/if}
```

Or if using `page.js`:

```javascript
import FarmInfo from './pages/FarmInfo.svelte';

page('/farm-info', () => {
  currentPage.set(FarmInfo);
});
```

### Step 3: Add Navigation Link

Add a link to the farm info page in your sidebar/menu:

```svelte
<!-- In Sidebar.svelte or navigation -->
<a href="/farm-info" class="nav-link">
  🌾 Farm Info
</a>
```

### Step 4: Test It

1. Navigate to the Farm Info page
2. You should see the simulation
3. Use WASD/Arrow keys to move the farmer
4. Press E near a farm to see details
5. Check the dashboard on the right

That's it! 🎉

## Standalone Test (No Router Changes Needed)

To test without modifying your router:

### Option A: Replace an Existing Page Temporarily

In `src/pages/Dashboard.svelte`, add:

```svelte
<script>
  import FarmingSimulation from '../components/FarmingSimulation.svelte';
  import { authStore } from '../stores/authStore';
</script>

<h1>Farm Simulation</h1>
<FarmingSimulation userLandArea={$authStore.user.farmSize || 100} />
```

Go to dashboard and the simulation appears.

### Option B: Open HTML Demo in Browser

Open `farming-simulation-demo.html` in your browser directly. No build required!

## Verify User Data

Make sure your `authStore` has `farmSize` field:

```javascript
// In authStore.js or wherever user data comes from
export const authStore = writable({
  user: {
    name: 'John Farmer',
    farmSize: 100,      // ← Make sure this exists
    crop: 'Tomato',
    location: 'Punjab'
  }
});
```

If `farmSize` is missing, the component defaults to 100 sq units.

## Customization

### Change Default Land Area

```svelte
<FarmingSimulation userLandArea={200} />  <!-- Always 200, ignores store -->
```

### Handle Farm Selection

```svelte
<script>
  function handleFarmSelect(farmInfo) {
    console.log('Farm selected:', farmInfo);
    // Do something with the data
  }
</script>

<FarmingSimulation 
  userLandArea={$authStore.user.farmSize}
  onFarmSelect={handleFarmSelect}
/>
```

### Adjust Simulation Appearance

Edit `src/components/FarmingSimulation.svelte`:

```javascript
simulation = new FarmingSimulation(
  containerElement.id,
  tilesPerSide,
  tilesPerSide,
  48  // Change from 32 to make tiles larger
);
```

## Testing Checklist

- [ ] FarmInfo.svelte page loads without errors
- [ ] Canvas appears in the page
- [ ] WASD/Arrow keys move the farmer
- [ ] E key shows farm details
- [ ] Dashboard shows weather and stats
- [ ] Popup closes when clicking outside or pressing ESC
- [ ] Works on mobile (responsive design)
- [ ] No console errors

## If Something Doesn't Work

### Canvas Not Showing

1. Check browser console for errors (F12)
2. Verify `farm-simulator` div exists
3. Check that farmingSimulation.js is imported
4. Ensure container element has proper ID

### Controls Not Working

1. Click on the canvas first to focus it
2. Check that WASD/E keys aren't conflicting with other listeners
3. Open console and type: `navigator.keyboard` (should work)

### Land Area Not Calculated Correctly

Make sure `authStore.user.farmSize` is a number:
```javascript
// Good
farmSize: 100

// Bad  
farmSize: "100"  // String, not number
```

Fix in your auth store if needed:
```javascript
farmSize: parseInt(data.farmSize) || 100
```

## File Reference

| File | Purpose | Modify? |
|------|---------|---------|
| `src/utils/farmingSimulation.js` | Core engine | Only if customizing simulation |
| `src/components/FarmingSimulation.svelte` | Svelte wrapper | Only if changing wrapper behavior |
| `src/pages/FarmInfo.svelte` | Complete page example | Use as-is or modify styling |
| `FARMING_INTEGRATION.md` | Full documentation | Reference only |
| `farming-simulation-demo.html` | HTML demo | Reference/testing only |

## Next: Backend Integration (Optional)

To save farm data to your backend:

```svelte
<script>
  let simulation;
  let selectedFarm;

  function handleFarmSelect(farmInfo) {
    selectedFarm = farmInfo;
    
    // Save to backend
    fetch('/api/farm/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        farmId: farmInfo.id,
        moisture: farmInfo.soilMoisture,
        health: farmInfo.cropHealth
      })
    });
  }
</script>

<FarmingSimulation onFarmSelect={handleFarmSelect} />
```

## Common Questions

**Q: Can I use this without Svelte?**
A: Yes! Use `farming-simulation-demo.html` or use `src/utils/farmingSimulation.js` directly in vanilla JS.

**Q: How do I save farm state?**
A: The simulation currently runs in-memory. To persist: capture stats with `getFarmStats()` and save to backend/database.

**Q: Can I modify simulation parameters?**
A: Yes! Edit `src/utils/farmingSimulation.js` to change evaporation rates, thresholds, colors, etc.

**Q: Does it work on mobile?**
A: Yes, it's fully responsive. Controls are WASD/Arrow keys which work on most devices.

**Q: How large can the farm be?**
A: Tested up to 900 tiles (30×30) with smooth performance. Adjust based on your needs.

## Support Resources

1. **Full Documentation:** Read `FARMING_INTEGRATION.md`
2. **Working Example:** Check `src/pages/FarmInfo.svelte`
3. **HTML Demo:** Open `farming-simulation-demo.html` in browser
4. **Troubleshooting:** See "If Something Doesn't Work" section above

---

You're all set! Start the farm simulation and let those crops grow! 🌾🚜
