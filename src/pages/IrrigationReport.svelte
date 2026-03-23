<script>
  import { onMount } from 'svelte'
  import { get } from 'svelte/store'
  import { authStore } from '../stores/authStore'
  import { farmStatsStore } from '../stores/farmStatsStore'
  import { buildIrrigationReport } from '../utils/irrigationReporting'

  const REPORT_TIMEOUT_MS = 5000

  let report = null
  let loading = false
  let error = ''
  let requestDurationMs = null
  let generatedWithinSla = null

  async function fetchDashboardDataWithTimeout(timeoutMs = REPORT_TIMEOUT_MS) {
    const controller = new AbortController()
    const timer = setTimeout(() => {
      controller.abort()
    }, timeoutMs)

    try {
      const response = await fetch('/api/dashboard/data', {
        credentials: 'include',
        signal: controller.signal,
      })

      if (!response.ok) {
        throw new Error('Failed to fetch irrigation data')
      }

      return await response.json()
    } catch (err) {
      if (err.name === 'AbortError') {
        throw new Error('Report generation exceeded 5 seconds. Please retry.')
      }
      throw err
    } finally {
      clearTimeout(timer)
    }
  }

  async function generateReport() {
    loading = true
    error = ''

    const startedAt = performance.now()
    const liveFarmStatsAtClick = get(farmStatsStore)

    try {
      const dashboardData = await fetchDashboardDataWithTimeout()
      report = buildIrrigationReport(dashboardData, liveFarmStatsAtClick)

      requestDurationMs = performance.now() - startedAt
      generatedWithinSla = requestDurationMs <= REPORT_TIMEOUT_MS
    } catch (err) {
      report = null
      requestDurationMs = performance.now() - startedAt
      generatedWithinSla = false
      error = err.message || 'Could not generate report'
    } finally {
      loading = false
    }
  }

  onMount(() => {
    generateReport()
  })
</script>

<div class="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 md:p-8 md:pl-72">
  <header class="bg-white shadow-md md:rounded-lg md:mb-8">
    <div class="px-8 py-6 md:flex md:items-center md:justify-between gap-3">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">💧 Irrigation Report</h1>
        <p class="text-gray-500 mt-1">Water usage and efficiency report generated on request</p>
      </div>
      <button
        on:click={generateReport}
        disabled={loading}
        class="px-5 py-2.5 bg-emerald-600 text-white rounded-lg font-semibold hover:bg-emerald-700 disabled:opacity-50"
      >
        {loading ? 'Generating...' : 'Generate Report'}
      </button>
    </div>
  </header>

  <main class="max-w-6xl mx-auto px-4 md:px-0 space-y-6">
    <div class="bg-white rounded-lg shadow-md p-5 border-l-4 border-emerald-500">
      <p class="text-sm text-gray-700">
        Farmer: <span class="font-semibold">{$authStore.user?.name || 'User'}</span>
        <span class="mx-2">•</span>
        Crop: <span class="font-semibold">{$authStore.user?.crop || '-'}</span>
        <span class="mx-2">•</span>
        Farm Size: <span class="font-semibold">{$authStore.user?.farmSize || '-'}</span>
      </p>
      {#if requestDurationMs !== null}
        <p class="text-sm mt-2 font-medium {generatedWithinSla ? 'text-emerald-700' : 'text-red-700'}">
          {generatedWithinSla ? '✓ SLA met' : '⚠ SLA missed'} — generated in {(requestDurationMs / 1000).toFixed(2)}s
        </p>
      {/if}
    </div>

    {#if loading}
      <div class="bg-white rounded-lg shadow-md p-8 text-center">
        <p class="text-gray-600">Generating irrigation performance report...</p>
      </div>
    {/if}

    {#if error}
      <div class="bg-red-50 border border-red-200 rounded-lg p-4">
        <p class="text-red-700 font-semibold">{error}</p>
      </div>
    {/if}

    {#if report}
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div class="bg-white rounded-lg shadow-md p-5">
          <p class="text-xs uppercase tracking-wide text-gray-500">Required Water</p>
          <p class="text-2xl font-bold text-gray-900 mt-2">{report.metrics.requirement} mm</p>
        </div>
        <div class="bg-white rounded-lg shadow-md p-5">
          <p class="text-xs uppercase tracking-wide text-gray-500">Actual Usage</p>
          <p class="text-2xl font-bold text-blue-700 mt-2">{report.metrics.actual} mm</p>
        </div>
        <div class="bg-white rounded-lg shadow-md p-5">
          <p class="text-xs uppercase tracking-wide text-gray-500">Efficiency</p>
          <p class="text-2xl font-bold text-emerald-700 mt-2">{report.metrics.efficiency}%</p>
        </div>
        <div class="bg-white rounded-lg shadow-md p-5">
          <p class="text-xs uppercase tracking-wide text-gray-500">Performance Score</p>
          <p class="text-2xl font-bold text-indigo-700 mt-2">{report.metrics.performanceScore}</p>
          <p class="text-xs text-gray-500 mt-1">{report.metrics.performanceBand}</p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-lg font-bold text-gray-900 mb-4">📊 Farm Stats & Water Usage</h2>
          <div class="space-y-3 text-sm">
            <p><span class="font-semibold">Avg Moisture:</span> {report.metrics.avgMoisture}%</p>
            <p><span class="font-semibold">Avg Health:</span> {report.metrics.avgHealth}%</p>
            <p><span class="font-semibold">Water Usage:</span> {report.metrics.waterUsagePercent}% of required</p>
            <p><span class="font-semibold">Deficit:</span> {report.metrics.deficit} mm</p>
            <p><span class="font-semibold">Estimated Savings:</span> {report.metrics.estimatedSavings} mm</p>
            <p><span class="font-semibold">Current Zone:</span> {report.irrigation.currentZone || '-'}</p>
            <p><span class="font-semibold">Next Schedule:</span> {report.irrigation.nextSchedule || '-'}</p>
            <p><span class="font-semibold">Generated At:</span> {report.generatedAt}</p>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-lg font-bold text-gray-900 mb-4">💡 Report Recommendations</h2>
          <div class="space-y-3">
            {#each report.recommendations as rec}
              <div class="p-3 rounded-lg bg-emerald-50 border border-emerald-100 text-sm text-emerald-900">
                {rec}
              </div>
            {/each}
          </div>
        </div>
      </div>
    {/if}
  </main>
</div>
