<script>
  export let irrigation = {}
  export let water = {}
</script>

<div class="bg-gradient-to-br from-green-400 to-emerald-500 rounded-lg shadow-lg p-8 text-white">
  <h3 class="text-lg font-bold mb-6">💧 Irrigation Status</h3>

  <div class="space-y-6">
    <!-- Main Status -->
    <div class="bg-white bg-opacity-20 rounded-lg p-6 backdrop-blur text-center">
      <p class="text-green-100 text-sm mb-2">System Status</p>
      <p class="text-3xl font-bold flex items-center justify-center">
        <span class="inline-block w-4 h-4 bg-green-300 rounded-full mr-3 animate-pulse"></span>
        {irrigation.status}
      </p>
    </div>

    <!-- Zone and Time Info -->
    <div class="grid grid-cols-2 gap-4">
      <div class="bg-white bg-opacity-20 rounded-lg p-4 backdrop-blur">
        <p class="text-green-100 text-xs">Current Zone</p>
        <p class="text-2xl font-bold mt-2">{irrigation.currentZone}</p>
      </div>

      <div class="bg-white bg-opacity-20 rounded-lg p-4 backdrop-blur">
        <p class="text-green-100 text-xs">Time Remaining</p>
        <p class="text-2xl font-bold mt-2">{irrigation.timeRemaining}</p>
      </div>
    </div>

    <!-- Schedule -->
    <div class="bg-white bg-opacity-20 rounded-lg p-4 backdrop-blur">
      <p class="text-green-100 text-sm">Next Schedule</p>
      <p class="text-lg font-semibold mt-2">📅 {irrigation.nextSchedule}</p>
    </div>

    <!-- Efficiency -->
    <div class="bg-white bg-opacity-20 rounded-lg p-4 backdrop-blur">
      <p class="text-green-100 text-sm">System Efficiency</p>
      <p class="text-3xl font-bold mt-2 text-green-200">{water.efficiency}%</p>
      <div class="mt-3 bg-white bg-opacity-20 rounded-full h-2 overflow-hidden">
        <div
          class="bg-green-300 h-2 rounded-full transition-all duration-300"
          style="width: {water.efficiency}%"
        ></div>
      </div>
    </div>
  </div>
</div>
