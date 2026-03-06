import { writable } from 'svelte/store'

export const weatherStore = writable({
  data: null,
  loading: false,
  error: '',
  lastUpdated: null,
  location: null,
})

export async function fetchWeatherData(location) {
  if (!location) {
    weatherStore.update(state => ({
      ...state,
      error: 'Location is required',
    }))
    return null
  }

  weatherStore.update(state => ({
    ...state,
    loading: true,
    error: '',
  }))

  try {
    const response = await fetch(`/api/weather/${encodeURIComponent(location)}`)
    
    if (!response.ok) {
      throw new Error('Failed to fetch weather data')
    }

    const data = await response.json()
    const now = new Date()

    weatherStore.update(state => ({
      ...state,
      data: data.weather,
      location: data.location || location,
      lastUpdated: now.toLocaleString('en-IN'),
      loading: false,
      error: '',
    }))

    return data.weather
  } catch (error) {
    console.error('Weather fetch error:', error)
    weatherStore.update(state => ({
      ...state,
      error: error.message,
      loading: false,
    }))
    return null
  }
}
