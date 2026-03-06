# Integration Checklist & Data Requirements

## Before You Start

Ensure your user data schema includes these fields for the farming simulation:

### Required User Fields

```javascript
{
  name: String,           // ✓ You have this
  farmSize: Number,       // ← Make sure this exists!
  crop: String,           // ✓ You have this  
  location: String        // ✓ You have this
}
```

### Verify in Your Backend

Your user profile API should return:
```javascript
GET /api/auth/user
{
  "name": "Farmer John",
  "farmSize": 100,        // ← In square units
  "crop": "Tomato",
  "location": "Punjab"
}
```

## Checklist Before Integration

### 1. Verify authStore User Data

**In your authStore.js or wherever user data is set:**

```javascript
// After user login/signup, ensure farmSize is included
const user = {
  name: 'Farmer Name',
  farmSize: parseInt(farmData.farmSize) || 100,  // ← Must be a number!
  crop: 'Crop Type',
  location: 'Location'
};

authStore.set({
  user,
  isAuthenticated: true
});
```

**Test in browser console:**
```javascript
// Open DevTools Console (F12) and type:
let storeValue;
authStore.subscribe(value => storeValue = value);
console.log(storeValue.user.farmSize);  // Should print a number
```

### 2. Check Your Signup Form

**Make sure farmSize is captured in signup:**

In `src/pages/Signup.svelte`, ensure you're collecting farmSize:

```svelte
<script>
  let formData = {
    name: '',
    username: '',
    password: '',
    farmSize: '',        // ← Add this
    crop: 'Tomato',
    location: ''
  };

  async function handleSignup() {
    // Make sure farmSize is sent to backend
    await fetch('/api/auth/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: formData.name,
        username: formData.username,
        password: formData.password,
        farmSize: parseInt(formData.farmSize),  // Convert to number
        crop: formData.crop,
        location: formData.location
      })
    });
  }
</script>

<input type="number" placeholder="Farm Size (sq units)" bind:value={formData.farmSize} />
```

### 3. Check Your Profile Edit

**In `src/pages/Profile.svelte`, ensure farmSize can be edited:**

```svelte
<script>
  let editData = {
    name: $authStore.user.name,
    farmSize: $authStore.user.farmSize,  // ← Include this
    crop: $authStore.user.crop,
    location: $authStore.user.location
  };
</script>

<input 
  type="number" 
  placeholder="Farm Size" 
  bind:value={editData.farmSize}
  min="50"
  max="500"
/>
```

### 4. Backend API Check

Your backend should support:

**Signup endpoint:**
```
POST /api/auth/signup
Request body:
{
  "name": "String",
  "username": "String",
  "password": "String",
  "farmSize": Number,      // ← Include this field
  "crop": "String",
  "location": "String"
}

Response:
{
  "user": {
    "name": "...",
    "farmSize": 100,       // ← Return this
    "crop": "...",
    "location": "..."
  }
}
```

**Profile update endpoint:**
```
POST /api/auth/update-profile
Request body:
{
  "name": "String",
  "farmSize": Number,      // ← Include this field
  "crop": "String",
  "location": "String"
}

Response:
{
  "user": {...}
}
```

**Check in your server.js (backend):**

```javascript
app.post('/api/auth/signup', async (req, res) => {
  const { name, username, password, farmSize, crop, location } = req.body;
  
  // Validate farmSize
  if (!farmSize || typeof farmSize !== 'number') {
    return res.status(400).json({ error: 'farmSize must be a number' });
  }
  
  // Save to database
  // ... your code ...
  
  res.json({
    user: {
      name,
      farmSize,           // ← Return it
      crop,
      location
    }
  });
});
```

### 5. Database Schema Check

If using a database, ensure user table has:

```sql
-- Example MySQL schema
CREATE TABLE users (
  id INT PRIMARY KEY,
  name VARCHAR(200),
  username VARCHAR(100) UNIQUE,
  password VARCHAR(255),
  farmSize INT DEFAULT 100,      -- ← Include this column!
  crop VARCHAR(100),
  location VARCHAR(200),
  created_at TIMESTAMP
);
```

Or if using JSON file storage (like users.json):

```json
{
  "username": "farmer1",
  "password": "hashed_password",
  "name": "John Farmer",
  "farmSize": 100,              // ← Include this
  "crop": "Tomato",
  "location": "Punjab"
}
```

## Post-Integration Checklist

Once you've set everything up:

- [ ] farmSize field exists in user data
- [ ] Signup form collects farmSize
- [ ] Profile edit form allows changing farmSize
- [ ] Backend API returns farmSize in user object
- [ ] Database/storage includes farmSize column
- [ ] authStore.user.farmSize returns a number (not string)
- [ ] FarmingSimulation component receives farmSize prop

## Testing

### Test 1: Verify Store Has Data

```javascript
// In browser console
authStore.subscribe(v => console.log(v.user.farmSize));
```

Should output: `100` (or whatever the farm size is)

### Test 2: Simple Integration Test

Create a test file `src/pages/FarmTest.svelte`:

```svelte
<script>
  import FarmingSimulation from '../components/FarmingSimulation.svelte';
  import { authStore } from '../stores/authStore';
</script>

<div>
  <p>Farm Size from Store: {$authStore.user?.farmSize || 'NOT SET'}</p>
  {#if $authStore.user?.farmSize}
    <FarmingSimulation userLandArea={$authStore.user.farmSize} />
  {/if}
</div>
```

Navigate to this page. If you see the simulation, data is flowing correctly!

### Test 3: Check Different Farm Sizes

```javascript
// Manually set different farm sizes and watch grid change
// In browser console:
authStore.set({
  user: { ...currentUser, farmSize: 50 }   // 7x7 grid
});
```

Refresh page, simulation should show smaller grid.

```javascript
authStore.set({
  user: { ...currentUser, farmSize: 400 }  // 20x20 grid  
});
```

Simulation should show larger grid.

## Troubleshooting Data Issues

| Problem | Solution |
|---------|----------|
| `undefined` land area | farmSize not in user object, set default or add field |
| Grid too small | farmSize is too low, increase value or multiply by 10 |
| Grid too large | farmSize is too high, check if in wrong unit |
| "Not a number" error | farmSize is string, convert to parseInt() |
| farmSize always 100 | Check if fallback is being used, verify data is saved |

## Example Complete Flow

### 1. User Signs Up

```
Form: 
  Name: John Farmer
  Username: farmer1
  Password: ***
  Farm Size: 150 sq units
  Crop: Wheat
  Location: Haryana

POST /api/auth/signup
{
  "name": "John Farmer",
  "username": "farmer1", 
  "password": "hashed",
  "farmSize": 150,         // ← Sent as number
  "crop": "Wheat",
  "location": "Haryana"
}
```

### 2. Backend Saves to DB

```javascript
// server.js
const user = {
  name: "John Farmer",
  username: "farmer1",
  farmSize: 150,           // ← Stored as number
  crop: "Wheat",
  location: "Haryana"
};
saveToDatabase(user);
```

### 3. User Logs In

```
GET /api/auth/user
Response:
{
  "name": "John Farmer",
  "farmSize": 150,         // ← Retrieved from DB
  "crop": "Wheat",
  "location": "Haryana"
}
```

### 4. authStore Updates

```javascript
authStore.set({
  user: {
    name: "John Farmer",
    farmSize: 150,         // ← In store now
    crop: "Wheat",
    location: "Haryana"
  },
  isAuthenticated: true
});
```

### 5. Farm Simulation Uses It

```svelte
<FarmingSimulation userLandArea={150} />
<!-- Grid calculates: Math.ceil(√(150 / 10)) = 4 → Actually 12×12 grid -->
<!-- More accurately: 12×12 = 144 ≈ 150 sq units -->
```

## Questions?

- **Can I skip farmSize?** No, but component has default of 100 if missing
- **What units for farmSize?** Square units (sq meters, acres converted, etc.)
- **Can it be decimal?** Preference for integers, decimals will be rounded
- **Min/Max values?** Works with 50-500+ sq units, larger values = more tiles

---

**You're ready!** Once these fields are in place, the farming simulation will automatically adapt to each user's land area. 🌾
