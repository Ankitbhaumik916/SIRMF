<script>
  export let weather = {}

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
</script>

<div class="bg-gradient-to-br from-blue-400 to-cyan-500 rounded-lg shadow-lg p-8 text-white">
  <h3 class="text-lg font-bold mb-6">🌤️ Current Weather</h3>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
    <!-- Main Weather Info -->
    <div class="flex items-center justify-center">
      <div class="text-center">
        <div class="text-6xl mb-4">{getWeatherEmoji(weather.icon)}</div>
        <p class="text-4xl font-bold">{weather.temp}°C</p>
        <p class="text-blue-100 capitalize mt-2">{weather.description}</p>
        <p class="text-blue-100 text-sm">Feels like {weather.feelsLike}°C</p>
      </div>
    </div>

    <!-- Weather Details -->
    <div class="space-y-4">
      <div class="bg-white	 bg-opacity-20 rounded-lg p-4 backdrop-blur">
        <div class="flex items-center justify-between">
          <p class="text-blue-100">Humidity</p>
          <p class="text-2xl font-bold">{weather.humidity}%</p>
        </div>
      </div>

      <div class="bg-white bg-opacity-20 rounded-lg p-4 backdrop-blur">
        <div class="flex items-center justify-between">
          <p class="text-blue-100">Wind Speed</p>
          <p class="text-2xl font-bold">{weather.windSpeed} km/h</p>
        </div>
      </div>

      <div class="bg-white bg-opacity-20 rounded-lg p-4 backdrop-blur">
        <div class="flex items-center justify-between">
          <p class="text-blue-100">Pressure</p>
          <p class="text-2xl font-bold">{weather.pressure} mb</p>
        </div>
      </div>

      <div class="bg-white bg-opacity-20 rounded-lg p-4 backdrop-blur">
        <div class="flex items-center justify-between">
          <p class="text-blue-100">Cloud Cover</p>
          <p class="text-2xl font-bold">{weather.cloudiness}%</p>
        </div>
      </div>
    </div>
  </div>
</div>
