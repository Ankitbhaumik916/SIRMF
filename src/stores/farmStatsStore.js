import { writable } from 'svelte/store'

const baselineStats = {
  avgMoisture: 55,
  avgHealth: 75,
  totalFarms: 0,
  farmsNeedingIrrigation: 0,
  currentWeather: 'sunny',
}

export const farmStatsStore = writable(baselineStats)

export function setFarmStats(stats = {}) {
  farmStatsStore.update((current) => ({
    ...current,
    ...stats,
    avgMoisture: clampPercent(stats.avgMoisture ?? current.avgMoisture),
    avgHealth: clampPercent(stats.avgHealth ?? current.avgHealth),
  }))
}

function clampPercent(value) {
  return Math.max(0, Math.min(100, Number(value) || 0))
}
