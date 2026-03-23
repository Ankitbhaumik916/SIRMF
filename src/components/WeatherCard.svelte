<script>
  import { createEventDispatcher } from 'svelte'
  import { languageStore, t } from '../stores/i18nStore'
  
  export let weather = {}
  export let location = 'User Location'
  
  const dispatch = createEventDispatcher()

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

  function handleViewFull() {
    dispatch('navigate', 'weather')
  }
</script>

<div class="bg-gradient-to-br from-blue-400 to-cyan-500 rounded-lg shadow-lg p-6 text-white">
  <div class="flex items-start justify-between mb-4">
    <div>
      <h3 class="text-lg font-bold">🌤️ {t('weatherCard.currentWeather', $languageStore)}</h3>
      <p class="text-blue-100 text-sm">{location}</p>
    </div>
    <button
      on:click={handleViewFull}
      class="px-3 py-1 bg-white bg-opacity-20 hover:bg-opacity-30 rounded text-sm font-semibold transition"
    >
      {t('weatherCard.viewFull', $languageStore)}
    </button>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <!-- Main Weather Info -->
    <div class="flex items-center justify-center">
      <div class="text-center">
        <div class="text-5xl mb-2">{getWeatherEmoji(weather.icon)}</div>
        <p class="text-3xl font-bold">{weather.temp}°C</p>
        <p class="text-blue-100 capitalize text-sm mt-1">{weather.description}</p>
      </div>
    </div>

    <!-- Weather Details -->
    <div class="space-y-2">
      <div class="bg-white bg-opacity-20 rounded p-3 backdrop-blur">
        <div class="flex justify-between items-center">
          <p class="text-blue-100 text-sm">{t('weatherCard.humidity', $languageStore)}</p>
          <p class="font-bold">{weather.humidity}%</p>
        </div>
      </div>

      <div class="bg-white bg-opacity-20 rounded p-3 backdrop-blur">
        <div class="flex justify-between items-center">
          <p class="text-blue-100 text-sm">{t('weatherCard.windSpeed', $languageStore)}</p>
          <p class="font-bold">{weather.windSpeed} km/h</p>
        </div>
      </div>

      <div class="bg-white bg-opacity-20 rounded p-3 backdrop-blur">
        <div class="flex justify-between items-center">
          <p class="text-blue-100 text-sm">{t('weatherCard.pressure', $languageStore)}</p>
          <p class="font-bold">{weather.pressure} mb</p>
        </div>
      </div>

      <div class="bg-white bg-opacity-20 rounded p-3 backdrop-blur">
        <div class="flex justify-between items-center">
          <p class="text-blue-100 text-sm">{t('weatherCard.clouds', $languageStore)}</p>
          <p class="font-bold">{weather.cloudiness}%</p>
        </div>
      </div>
    </div>
  </div>

  <p class="text-xs text-blue-100 mt-4 text-right">
    Last updated: {new Date().toLocaleTimeString('en-IN')}
  </p>
</div>
