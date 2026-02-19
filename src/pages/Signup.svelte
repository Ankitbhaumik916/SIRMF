<script>
  import { createEventDispatcher } from 'svelte'
  import { signup } from '../stores/authStore'

  const dispatch = createEventDispatcher()

  let step = 1 // Step 1: Credentials, Step 2: Farm Details
  
  let formData = {
    username: '',
    password: '',
    confirmPassword: '',
    name: '',
    farmSize: '',
    crop: 'Tomato',
    location: '',
  }

  let error = ''
  let success = false
  let loading = false
  let showPassword = false

  const crops = ['Tomato', 'Rice', 'Wheat', 'Corn', 'Sugarcane', 'Cotton', 'Potato', 'Onion']

  function validateStep1() {
    if (!formData.username || !formData.password || !formData.confirmPassword) {
      error = 'All credential fields are required'
      return false
    }
    if (formData.password !== formData.confirmPassword) {
      error = 'Passwords do not match'
      return false
    }
    if (formData.password.length < 6) {
      error = 'Password must be at least 6 characters'
      return false
    }
    return true
  }

  function validateStep2() {
    if (!formData.name || !formData.farmSize) {
      error = 'Farmer name and farm size are required'
      return false
    }
    return true
  }

  function nextStep() {
    error = ''
    if (validateStep1()) {
      step = 2
    }
  }

  function backStep() {
    error = ''
    step = 1
  }

  async function handleSignup() {
    error = ''
    success = false

    if (!validateStep2()) {
      return
    }

    loading = true
    const result = await signup(formData)

    if (result.success) {
      success = true
      setTimeout(() => {
        dispatch('navigate', 'login')
      }, 2000)
    } else {
      error = result.error || 'Signup failed'
    }

    loading = false
  }

  function handleKeyPress(e) {
    if (e.key === 'Enter' && step === 1) nextStep()
    if (e.key === 'Enter' && step === 2) handleSignup()
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-blue-900 via-blue-700 to-cyan-600 flex items-center justify-center p-4 py-8">
  <div class="relative z-10 w-full max-w-2xl">
    <div class="bg-white rounded-2xl shadow-2xl overflow-hidden animate-slide-in">
      <!-- Header -->
      <div class="bg-gradient-to-r from-blue-500 to-cyan-600 px-8 py-6 text-center">
        <div class="text-4xl mb-2">🚜</div>
        <h1 class="text-2xl font-bold text-white">Create Your Farm Account</h1>
        <p class="text-blue-50 text-sm">Join Smart Farming Community - Step {step} of 2</p>
      </div>

      <!-- Progress Bar -->
      <div class="px-8 pt-6">
        <div class="flex gap-4">
          <div
            class={`flex-1 h-2 rounded-full transition-all ${
              step >= 1 ? 'bg-blue-500' : 'bg-gray-300'
            }`}
          ></div>
          <div
            class={`flex-1 h-2 rounded-full transition-all ${
              step >= 2 ? 'bg-blue-500' : 'bg-gray-300'
            }`}
          ></div>
        </div>
      </div>

      <!-- Form -->
      <div class="px-8 py-6">
        {#if success}
          <div class="mb-4 p-4 bg-green-50 border-l-4 border-green-500 rounded">
            <p class="text-green-700 text-sm font-medium">
              Account created! Redirecting to login...
            </p>
          </div>
        {/if}

        {#if error}
          <div class="mb-4 p-4 bg-red-50 border-l-4 border-red-500 rounded">
            <p class="text-red-700 text-sm font-medium">{error}</p>
          </div>
        {/if}

        <!-- Step 1: Credentials -->
        {#if step === 1}
          <div class="space-y-4 mb-6">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Username</label>
              <input
                type="text"
                bind:value={formData.username}
                placeholder="Choose unique username"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={loading}
              />
              <p class="text-xs text-gray-500 mt-1">Used for login</p>
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Password</label>
              {#if showPassword}
                <input
                  type="text"
                  bind:value={formData.password}
                  placeholder="Min 6 characters"
                  on:keypress={handleKeyPress}
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={loading}
                />
              {:else}
                <input
                  type="password"
                  bind:value={formData.password}
                  placeholder="Min 6 characters"
                  on:keypress={handleKeyPress}
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={loading}
                />
              {/if}
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Confirm Password</label>
              {#if showPassword}
                <input
                  type="text"
                  bind:value={formData.confirmPassword}
                  placeholder="Confirm password"
                  on:keypress={handleKeyPress}
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={loading}
                />
              {:else}
                <input
                  type="password"
                  bind:value={formData.confirmPassword}
                  placeholder="Confirm password"
                  on:keypress={handleKeyPress}
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={loading}
                />
              {/if}
            </div>

            <label class="flex items-center text-sm text-gray-600">
              <input
                type="checkbox"
                bind:checked={showPassword}
                disabled={loading}
                class="rounded"
              />
              <span class="ml-2">Show password</span>
            </label>
          </div>

          <div class="flex gap-3">
            <button
              on:click={() => dispatch('navigate', 'login')}
              class="flex-1 px-4 py-3 border border-gray-300 text-gray-700 font-bold rounded-lg hover:bg-gray-50 transition"
            >
              Back to Login
            </button>
            <button
              on:click={nextStep}
              disabled={loading}
              class="flex-1 bg-gradient-to-r from-blue-500 to-cyan-600 hover:from-blue-600 hover:to-cyan-700 text-white font-bold py-3 rounded-lg transition disabled:opacity-50"
            >
              Next: Farm Details →
            </button>
          </div>
        {/if}

        <!-- Step 2: Farm Details -->
        {#if step === 2}
          <div class="space-y-4 mb-6">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Farmer Name *</label>
              <input
                type="text"
                bind:value={formData.name}
                placeholder="Your full name"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={loading}
              />
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Farm Size *</label>
                <input
                  type="text"
                  bind:value={formData.farmSize}
                  placeholder="e.g., 2 Acres"
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={loading}
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Primary Crop *</label>
                <select
                  bind:value={formData.crop}
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={loading}
                >
                  {#each crops as crop}
                    <option value={crop}>{crop}</option>
                  {/each}
                </select>
              </div>
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Location</label>
              <input
                type="text"
                bind:value={formData.location}
                placeholder="City, State (for weather detection)"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={loading}
              />
              <p class="text-xs text-gray-500 mt-1">Will be used for real-time weather data</p>
            </div>
          </div>

          <div class="flex gap-3">
            <button
              on:click={backStep}
              disabled={loading}
              class="flex-1 px-4 py-3 border border-gray-300 text-gray-700 font-bold rounded-lg hover:bg-gray-50 transition"
            >
              ← Back
            </button>
            <button
              on:click={handleSignup}
              disabled={loading || success}
              class="flex-1 bg-gradient-to-r from-blue-500 to-cyan-600 hover:from-blue-600 hover:to-cyan-700 text-white font-bold py-3 rounded-lg transition disabled:opacity-50"
            >
              {loading ? 'Creating Account...' : 'Create Account'}
            </button>
          </div>
        {/if}
      </div>

      <!-- Footer -->
      <div class="bg-gray-50 px-8 py-4 border-t border-gray-100">
        <p class="text-center text-gray-600 text-sm">
          Already have an account?
          <button
            on:click={() => dispatch('navigate', 'login')}
            class="text-blue-600 hover:text-blue-700 font-semibold"
          >
            Login
          </button>
        </p>
      </div>
    </div>
  </div>
</div>
