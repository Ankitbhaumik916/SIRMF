export const FARM_STATS_BASELINE = {
  avgMoisture: 55,
  avgHealth: 75,
}

function clamp(value, min = 0, max = 100) {
  return Math.max(min, Math.min(max, value))
}

function computeMoistureScore(avgMoisture) {
  const ideal = 60
  const diff = Math.abs(avgMoisture - ideal)
  return clamp(100 - diff * 3)
}

export function buildIrrigationReport(dashboardData, farmStats = FARM_STATS_BASELINE) {
  const requirement = dashboardData?.water?.requirement || 0
  const actual = dashboardData?.water?.actual || 0
  const deficit = dashboardData?.water?.deficit || Math.max(0, requirement - actual)
  const efficiency = dashboardData?.water?.efficiency || 0

  const waterUsagePercent = requirement > 0 ? (actual / requirement) * 100 : 0
  const savings = Math.max(0, requirement - actual)

  const moistureScore = computeMoistureScore(farmStats.avgMoisture)
  const healthScore = clamp(farmStats.avgHealth)

  const performanceScore = clamp(
    efficiency * 0.5 + moistureScore * 0.3 + healthScore * 0.2
  )

  let performanceBand = 'Critical'
  if (performanceScore >= 80) performanceBand = 'Excellent'
  else if (performanceScore >= 65) performanceBand = 'Good'
  else if (performanceScore >= 50) performanceBand = 'Needs Attention'

  const recommendations = []

  if (efficiency < 75) {
    recommendations.push('Check sprinkler/drip distribution uniformity to improve system efficiency.')
  }
  if (farmStats.avgMoisture < 45) {
    recommendations.push('Soil moisture is low; increase irrigation cycle frequency for the next schedule.')
  }
  if (deficit > requirement * 0.2) {
    recommendations.push('High deficit detected; prioritize irrigation in the current active zone first.')
  }
  if (recommendations.length === 0) {
    recommendations.push('Current irrigation performance is stable. Continue existing schedule with routine monitoring.')
  }

  return {
    generatedAt: new Date().toLocaleString('en-IN'),
    metrics: {
      requirement,
      actual,
      deficit,
      efficiency,
      waterUsagePercent: Number(waterUsagePercent.toFixed(2)),
      estimatedSavings: Number(savings.toFixed(2)),
      avgMoisture: farmStats.avgMoisture,
      avgHealth: farmStats.avgHealth,
      performanceScore: Number(performanceScore.toFixed(2)),
      performanceBand,
    },
    irrigation: dashboardData?.irrigation || {},
    recommendations,
  }
}
