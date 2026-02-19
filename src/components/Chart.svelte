<script>
  export let title = ''
  export let days = []
  export let values = []
  export let color = '#22c55e'

  const maxValue = Math.max(...values, 1)
  const chartHeight = 150
</script>

<div class="bg-white rounded-lg shadow-md p-6">
  <h3 class="text-lg font-bold text-gray-900 mb-4">{title}</h3>

  <div class="relative" style="height: {chartHeight}px;">
    <svg class="w-full h-full" viewBox="0 0 400 200" style="overflow: visible;">
      <!-- Grid lines -->
      <line x1="0" y1="50" x2="400" y2="50" stroke="#e5e7eb" stroke-width="1" stroke-dasharray="5,5" />
      <line x1="0" y1="100" x2="400" y2="100" stroke="#e5e7eb" stroke-width="1" stroke-dasharray="5,5" />
      <line x1="0" y1="150" x2="400" y2="150" stroke="#e5e7eb" stroke-width="1" stroke-dasharray="5,5" />

      <!-- Bars -->
      {#each values as value, i}
        <g>
          {#if i < days.length}
            <rect
              x={i * 55 + 10}
              y={150 - (value / maxValue) * 140}
              width="40"
              height={(value / maxValue) * 140}
              fill={color}
              opacity="0.8"
              rx="4"
              class="transition-all duration-300 hover:opacity-100"
            />
          {/if}
        </g>
      {/each}
    </svg>
  </div>

  <!-- Legend -->
  <div class="flex gap-2 justify-center mt-4 flex-wrap">
    {#each days as day, i}
      {#if i < values.length}
        <div class="flex items-center gap-2 text-xs">
          <div class="w-3 h-3 rounded" style="background-color: {color};"></div>
          <span class="text-gray-600">{day}:</span>
          <span class="font-semibold text-gray-900">{values[i]}</span>
        </div>
      {/if}
    {/each}
  </div>
</div>
