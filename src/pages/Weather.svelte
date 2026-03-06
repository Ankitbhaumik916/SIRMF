<script>
  import { onMount } from 'svelte'
  import { authStore } from '../stores/authStore'
  import { weatherStore, fetchWeatherData } from '../stores/weatherStore'

  let location = $authStore.user?.location || ''
  let tempLocation = location

  onMount(async () => {
    if (location) {
      await fetchWeatherData(location)
    }
  })

  async function handleSearchWeather() {
    if (tempLocation.trim()) {
      location = tempLocation
      await fetchWeatherData(location)
    }
  }

  function getWeatherEmoji(icon) {
    const iconMap = {
      'Clouds': '☁️',
      'Clear': '☀️',
      'Rain': '🌧️',
      'Drizzle': '🌦️',
      'Thunderstorm': '⛈️',
      'Snow': '❄️',
      'Mist': '🌫️',
      'Smoke': '💨',
      'Wind': '💨',
    }
    return iconMap[icon] || '🌤️'
  }

  function handleKeyPress(e) {
    if (e.key === 'Enter') {
      handleSearchWeather()
    }
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-blue-50 to-cyan-50">
  <!-- Header -->
  <header class="bg-white shadow-md sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
      <h1 class="text-3xl font-bold text-gray-900">🌤️ Weather Dashboard</h1>
      <p class="text-sm text-gray-500 mt-1">Real-time weather information for your location</p>
    </div>
  </header>

  <!-- Main Content -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Search Section -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-3">Enter Location</label>
      <div class="flex gap-3">
        <input
          type="text"
          bind:value={tempLocation}
          on:keypress={handleKeyPress}
          placeholder="e.g., Malda, Raiganj, Delhi..."
          class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          on:click={handleSearchWeather}
          disabled={$weatherStore.loading}
          class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400 transition font-semibold"
        >
          {$weatherStore.loading ? '🔄 Searching...' : 'Search'}
        </button>
      </div>
      {#if $weatherStore.lastUpdated}
        <p class="text-xs text-gray-500 mt-2">
          Last updated: {$weatherStore.lastUpdated}
        </p>
      {/if}
    </div>

    <!-- Error Message -->
    {#if $weatherStore.error}
      <div class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
        <p class="text-red-700 font-semibold">⚠️ Error: {$weatherStore.error}</p>
      </div>
    {/if}

    <!-- Loading State -->
    {#if $weatherStore.loading}
      <div class="flex items-center justify-center py-12">
        <div class="text-center">
          <div class="mb-4 text-5xl animate-bounce">🌤️</div>
          <p class="text-gray-600">Fetching weather data...</p>
        </div>
      </div>
    {:else if $weatherStore.data}
      <!-- Main Weather Info Card -->
      <div class="bg-gradient-to-br from-blue-400 to-cyan-500 rounded-lg shadow-lg p-8 text-white mb-6">
        <div class="flex items-start justify-between mb-8">
          <div>
            <h2 class="text-4xl font-bold mb-2">{$weatherStore.location}</h2>
            <p class="text-blue-100 capitalize text-lg">{$weatherStore.data.description}</p>
          </div>
          <div class="text-7xl">{getWeatherEmoji($weatherStore.data.icon)}</div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <!-- Temperature Section -->
          <div class="bg-white bg-opacity-20 rounded-lg p-6 backdrop-blur">
            <p class="text-blue-100 text-sm mb-2">Temperature</p>
            <p class="text-6xl font-bold mb-2">{$weatherStore.data.temp}°C</p>
            <p class="text-blue-100">Feels like {$weatherStore.data.feelsLike}°C</p>
          </div>

          <!-- Condition Summary -->
          <div class="bg-white bg-opacity-20 rounded-lg p-6 backdrop-blur">
            <p class="text-blue-100 text-sm mb-4">Weather Condition</p>
            <div class="space-y-3">
              <div class="flex justify-between items-center">
                <span class="text-blue-100">Humidity</span>
                <span class="text-2xl font-bold">{$weatherStore.data.humidity}%</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-blue-100">Wind Speed</span>
                <span class="text-2xl font-bold">{$weatherStore.data.windSpeed} km/h</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Detailed Information Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <!-- Pressure Card -->
        <div class="bg-white rounded-lg shadow p-6">
          <div class="text-3xl mb-3">🔻</div>
          <p class="text-gray-600 text-sm mb-1">Pressure</p>
          <p class="text-3xl font-bold text-gray-900">{$weatherStore.data.pressure}</p>
          <p class="text-gray-500 text-xs">millibars</p>
        </div>

        <!-- Cloud Cover Card -->
        <div class="bg-white rounded-lg shadow p-6">
          <div class="text-3xl mb-3">☁️</div>
          <p class="text-gray-600 text-sm mb-1">Cloud Cover</p>
          <p class="text-3xl font-bold text-gray-900">{$weatherStore.data.cloudiness}%</p>
          <div class="mt-2 bg-gray-200 rounded-full h-2">
            <div
              class="bg-blue-500 h-2 rounded-full transition-all duration-300"
              style="width: {$weatherStore.data.cloudiness}%"
            />
          </div>
        </div>

        <!-- Rainfall Card -->
        <div class="bg-white rounded-lg shadow p-6">
          <div class="text-3xl mb-3">🌧️</div>
          <p class="text-gray-600 text-sm mb-1">Rainfall</p>
          <p class="text-3xl font-bold text-gray-900">{$weatherStore.data.rainfall}</p>
          <p class="text-gray-500 text-xs">mm/hour</p>
        </div>

        <!-- Temperature Card -->
        <div class="bg-white rounded-lg shadow p-6">
          <div class="text-3xl mb-3">🌡️</div>
          <p class="text-gray-600 text-sm mb-1">Temperature</p>
          <p class="text-3xl font-bold text-gray-900">{$weatherStore.data.temp}°</p>
          <p class="text-gray-500 text-xs">Celsius</p>
        </div>
      </div>

      <!-- Irrigation Recommendations -->
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-bold text-gray-900 mb-4">📋 Irrigation Recommendations</h3>
        <div class="space-y-3">
          {#if $weatherStore.data.humidity < 40}
            <div class="flex items-start gap-3 p-3 bg-yellow-50 rounded-lg border border-yellow-200">
              <span class="text-lg">⚠️</span>
              <p class="text-yellow-800 text-sm">
                <strong>Low Humidity:</strong> Humidity is {$weatherStore.data.humidity}% - irrigation may be needed soon to prevent water loss.
              </p>
            </div>
          {/if}

          {#if $weatherStore.data.rainfall > 0}
            <div class="flex items-start gap-3 p-3 bg-blue-50 rounded-lg border border-blue-200">
              <span class="text-lg">💧</span>
              <p class="text-blue-800 text-sm">
                <strong>Rainfall Detected:</strong> {$weatherStore.data.rainfall}mm rainfall expected - consider reducing irrigation schedule.
              </p>
            </div>
          {/if}

          {#if $weatherStore.data.temp > 35}
            <div class="flex items-start gap-3 p-3 bg-orange-50 rounded-lg border border-orange-200">
              <span class="text-lg">🌡️</span>
              <p class="text-orange-800 text-sm">
                <strong>High Temperature:</strong> At {$weatherStore.data.temp}°C, increase irrigation frequency to prevent crop stress.
              </p>
            </div>
          {/if}

          {#if $weatherStore.data.cloudiness > 60}
            <div class="flex items-start gap-3 p-3 bg-cyan-50 rounded-lg border border-cyan-200">
              <span class="text-lg">☁️</span>
              <p class="text-cyan-800 text-sm">
                <strong>Cloudy Weather:</strong> {$weatherStore.data.cloudiness}% cloud cover reduces evaporation - reduce irrigation slightly.
              </p>
            </div>
          {/if}

          {#if $weatherStore.data.humidity >= 40 && $weatherStore.data.rainfall === 0 && $weatherStore.data.temp <= 35 && $weatherStore.data.cloudiness <= 60}
            <div class="flex items-start gap-3 p-3 bg-green-50 rounded-lg border border-green-200">
              <span class="text-lg">✅</span>
              <p class="text-green-800 text-sm">
                <strong>Optimal Conditions:</strong> Current weather conditions are ideal for irrigation and crop growth.
              </p>
            </div>
          {/if}
        </div>
      </div>
    {:else}
      <div class="text-center py-12 bg-white rounded-lg shadow">
        <p class="text-gray-600 text-lg">Enter a location to view weather information</p>
      </div>
    {/if}
  </main>
</div>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
  }
</style>
