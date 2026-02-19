<script>
  import { createEventDispatcher, onMount } from 'svelte'
  import { authStore } from '../stores/authStore'
  import WeatherCard from '../components/WeatherCard.svelte'
  import IrrigationStatus from '../components/IrrigationStatus.svelte'
  import Chart from '../components/Chart.svelte'

  const dispatch = createEventDispatcher()

  let data = null
  let loading = true
  let error = ''

  onMount(async () => {
    await loadDashboardData()
  })

  async function loadDashboardData() {
    try {
      loading = true
      error = ''
      const response = await fetch('/api/dashboard/data')

      if (response.ok) {
        data = await response.json()
      } else {
        error = 'Failed to load dashboard data'
      }
    } catch (err) {
      error = err.message
    } finally {
      loading = false
    }
  }

  function handleRefresh() {
    loadDashboardData()
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
  <!-- Header -->
  <header class="bg-white shadow-md sticky top-0 z-50 md:z-auto">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="text-3xl">🌾</div>
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Dashboard</h1>
            <p class="text-sm text-gray-500">Real-time Irrigation Management</p>
          </div>
        </div>

        <button
          on:click={handleRefresh}
          class="p-2 hover:bg-gray-100 rounded-lg transition"
          title="Refresh data"
        >
          🔄
        </button>
      </div>
    </div>
  </header>

  <!-- Main Content -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    {#if loading}
      <div class="flex items-center justify-center py-12">
        <div class="text-center">
          <div class="mb-4 text-4xl animate-bounce">🌾</div>
          <p class="text-gray-600">Loading dashboard data...</p>
        </div>
      </div>
    {:else if error}
      <div class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
        <p class="text-red-700 font-semibold">Error: {error}</p>
        <button
          on:click={handleRefresh}
          class="mt-2 text-red-600 hover:text-red-700 underline text-sm"
        >
          Try again
        </button>
      </div>
    {:else if data}
      <!-- User Info -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-6 border-l-4 border-green-500">
        <h2 class="text-xl font-bold text-gray-900 mb-4">Welcome, {$authStore.user.name}</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <p class="text-gray-600 text-sm">Farm Size</p>
            <p class="text-2xl font-bold text-green-600">{$authStore.user.farmSize}</p>
          </div>
          <div>
            <p class="text-gray-600 text-sm">Crop Type</p>
            <p class="text-2xl font-bold text-green-600">{data.crop.name}</p>
          </div>
          <div>
            <p class="text-gray-600 text-sm">Location</p>
            <p class="text-lg font-semibold text-gray-900">{$authStore.user.location}</p>
          </div>
          <div>
            <p class="text-gray-600 text-sm">Season</p>
            <p class="text-lg font-semibold text-gray-900">{data.crop.season}</p>
          </div>
        </div>
      </div>

      <!-- Weather & Irrigation Status -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <WeatherCard weather={data.weather} />
        <IrrigationStatus irrigation={data.irrigation} water={data.water} />
      </div>

      <!-- Sensor Data -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6 mb-6">
        <div class="bg-white rounded-lg shadow-md p-6">
          <p class="text-gray-600 text-sm">Soil Moisture</p>
          <p class="text-3xl font-bold text-blue-600 mt-2">{data.sensors.moisture}%</p>
          <div class="mt-2 bg-gray-200 rounded-full h-2">
            <div
              class="bg-blue-500 h-2 rounded-full transition-all duration-300"
              style="width: {data.sensors.moisture}%"
            />
          </div>
        </div>
        <div class="bg-white rounded-lg shadow-md p-6">
          <p class="text-gray-600 text-sm">Temperature</p>
          <p class="text-3xl font-bold text-orange-600 mt-2">{data.sensors.temperature}°C</p>
          <p class="text-xs text-gray-500 mt-2">Feels like {data.weather.feelsLike}°C</p>
        </div>
        <div class="bg-white rounded-lg shadow-md p-6">
          <p class="text-gray-600 text-sm">Humidity</p>
          <p class="text-3xl font-bold text-cyan-600 mt-2">{data.sensors.humidity}%</p>
          <p class="text-xs text-gray-500 mt-2">Pressure: {data.weather.pressure}mb</p>
        </div>
        <div class="bg-white rounded-lg shadow-md p-6">
          <p class="text-gray-600 text-sm">Rainfall</p>
          <p class="text-3xl font-bold text-indigo-600 mt-2">{data.sensors.rainfall}mm</p>
          <p class="text-xs text-gray-500 mt-2">Last hour</p>
        </div>
      </div>

      <!-- Water Requirements -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h3 class="text-lg font-bold text-gray-900 mb-4">💧 Water Management</h3>
        <div class="grid grid-cols-3 gap-4 mb-6">
          <div class="text-center p-4 bg-green-50 rounded-lg">
            <p class="text-gray-600 text-sm">Required</p>
            <p class="text-3xl font-bold text-green-600">{data.water.requirement}</p>
            <p class="text-xs text-gray-500">mm per season</p>
          </div>
          <div class="text-center p-4 bg-blue-50 rounded-lg">
            <p class="text-gray-600 text-sm">Actually Used</p>
            <p class="text-3xl font-bold text-blue-600">{data.water.actual}</p>
            <p class="text-xs text-gray-500">mm (85% efficient)</p>
          </div>
          <div class="text-center p-4 bg-red-50 rounded-lg">
            <p class="text-gray-600 text-sm">Deficit</p>
            <p class="text-3xl font-bold text-red-600">{data.water.deficit}</p>
            <p class="text-xs text-gray-500">mm remaining</p>
          </div>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
          <div
            class="bg-gradient-to-r from-green-400 to-blue-500 h-4 rounded-full transition-all duration-300"
            style="width: {(data.water.actual / data.water.requirement) * 100}%"
          />
        </div>
        <p class="text-xs text-gray-500 mt-2">
          {Math.round((data.water.actual / data.water.requirement) * 100)}% of required water applied
        </p>
      </div>

      <!-- Recommendations -->
      <div class="bg-white rounded-lg shadow-md p-6 mb-6">
        <h3 class="text-lg font-bold text-gray-900 mb-4">📋 Recommendations</h3>
        <div class="space-y-2">
          {#each data.recommendations as rec}
            <div class="flex items-start space-x-3 p-3 bg-blue-50 rounded-lg">
              <span class="text-lg">💡</span>
              <p class="text-gray-700 text-sm">{rec}</p>
            </div>
          {/each}
        </div>
      </div>

      <!-- Charts -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Chart
          title="Weekly Soil Moisture (%)"
          days={data.weekly.days}
          values={data.weekly.moisture}
          color="#3b82f6"
        />
        <Chart
          title="Weekly Temperature (°C)"
          days={data.weekly.days}
          values={data.weekly.temperature}
          color="#f97316"
        />
        <Chart
          title="Weekly Water Usage (mm)"
          days={data.weekly.days}
          values={data.weekly.waterUsage}
          color="#22c55e"
        />
      </div>
    {/if}
  </main>
</div>
