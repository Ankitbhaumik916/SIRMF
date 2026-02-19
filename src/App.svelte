<script>
  import { onMount } from 'svelte'
  import { authStore, checkAuth, logout } from './stores/authStore'
  import Login from './pages/Login.svelte'
  import Signup from './pages/Signup.svelte'
  import Dashboard from './pages/Dashboard.svelte'
  import Profile from './pages/Profile.svelte'
  import Sidebar from './components/Sidebar.svelte'

  let currentPage = 'loading'

  onMount(async () => {
    const isAuthenticated = await checkAuth()
    currentPage = isAuthenticated ? 'dashboard' : 'login'
  })

  function handleNavigation(event) {
    const page = event.detail
    if (page === 'logout') {
      logout()
      currentPage = 'login'
    } else {
      currentPage = page
    }
  }

  $: if ($authStore.loading) {
    currentPage = 'loading'
  }
</script>

<svelte:window />

{#if $authStore.loading}
  <div class="flex items-center justify-center min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
    <div class="text-center">
      <div class="mb-4 text-5xl animate-bounce">🌾</div>
      <h2 class="text-2xl font-bold text-gray-700 mb-2">Smart Farming System</h2>
      <p class="text-gray-500">Loading...</p>
    </div>
  </div>
{:else if !$authStore.isAuthenticated}
  {#if currentPage === 'login'}
    <Login on:navigate={handleNavigation} />
  {:else if currentPage === 'signup'}
    <Signup on:navigate={handleNavigation} />
  {/if}
{:else}
  <div class="flex">
    <Sidebar on:navigate={handleNavigation} />
    <main class="flex-1 overflow-auto">
      {#if currentPage === 'dashboard'}
        <Dashboard on:navigate={handleNavigation} />
      {:else if currentPage === 'profile'}
        <Profile on:navigate={handleNavigation} />
      {:else if currentPage === 'weather'}
        <div class="p-8">
          <h1 class="text-3xl font-bold mb-4">🌤️ Weather Dashboard</h1>
          <p class="text-gray-600">Weather page coming soon...</p>
        </div>
      {:else if currentPage === 'irrigation'}
        <div class="p-8">
          <h1 class="text-3xl font-bold mb-4">💧 Irrigation Management</h1>
          <p class="text-gray-600">Irrigation management page coming soon...</p>
        </div>
      {:else if currentPage === 'farm'}
        <div class="p-8">
          <h1 class="text-3xl font-bold mb-4">🌾 Farm Information</h1>
          <p class="text-gray-600">Farm information page coming soon...</p>
        </div>
      {:else if currentPage === 'settings'}
        <div class="p-8">
          <h1 class="text-3xl font-bold mb-4">⚙️ Settings</h1>
          <p class="text-gray-600">Settings page coming soon...</p>
        </div>
      {/if}
    </main>
  </div>
{/if}

<style global>
  :global(body) {
    margin: 0;
    padding: 0;
  }
</style>
