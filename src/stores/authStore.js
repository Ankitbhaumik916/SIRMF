import { writable } from 'svelte/store'

// Auth store
export const authStore = writable({
  user: null,
  isAuthenticated: false,
  loading: true,
})

// Check if user is logged in on app load
export async function checkAuth() {
  try {
    const response = await fetch('/api/auth/user')
    if (response.ok) {
      const user = await response.json()
      authStore.set({
        user,
        isAuthenticated: true,
        loading: false,
      })
      return true
    } else {
      authStore.set({
        user: null,
        isAuthenticated: false,
        loading: false,
      })
      return false
    }
  } catch (error) {
    console.error('Auth check failed:', error)
    authStore.set({
      user: null,
      isAuthenticated: false,
      loading: false,
    })
    return false
  }
}

export async function login(username, password) {
  try {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    })

    const data = await response.json()

    if (response.ok) {
      authStore.set({
        user: data.user,
        isAuthenticated: true,
        loading: false,
      })
      return { success: true, user: data.user }
    } else {
      return { success: false, error: data.error }
    }
  } catch (error) {
    return { success: false, error: error.message }
  }
}

export async function signup(userData) {
  try {
    const response = await fetch('/api/auth/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData),
    })

    const data = await response.json()
    return response.ok ? { success: true } : { success: false, error: data.error }
  } catch (error) {
    return { success: false, error: error.message }
  }
}

export async function logout() {
  try {
    await fetch('/api/auth/logout', { method: 'POST' })
    authStore.set({
      user: null,
      isAuthenticated: false,
      loading: false,
    })
    return true
  } catch (error) {
    console.error('Logout failed:', error)
    return false
  }
}
