<script>
  import { createEventDispatcher } from 'svelte'
  import { authStore } from '../stores/authStore'

  const dispatch = createEventDispatcher()

  let isOpen = false
  let currentPage = 'dashboard'

  $: if ($authStore.isAuthenticated) {
    // Keep sidebar in sync with current page
  }

  function navigate(page) {
    currentPage = page
    dispatch('navigate', page)
    isOpen = false
  }

  function handleLogout() {
    dispatch('navigate', 'logout')
    isOpen = false
  }

  const menuItems = [
    { id: 'dashboard', icon: '📊', label: 'Dashboard', color: 'blue' },
    { id: 'weather', icon: '🌤️', label: 'Weather', color: 'cyan' },
    { id: 'irrigation', icon: '💧', label: 'Irrigation', color: 'green' },
    { id: 'farm', icon: '🌾', label: 'Farm Info', color: 'amber' },
    { id: 'profile', icon: '👤', label: 'Profile', color: 'purple' },
    { id: 'settings', icon: '⚙️', label: 'Settings', color: 'gray' },
  ]
</script>

<div class="flex h-screen bg-gray-50">
  <!-- Mobile menu button -->
  <button
    on:click={() => (isOpen = !isOpen)}
    class="fixed top-4 left-4 z-50 md:hidden p-2 bg-green-600 text-white rounded-lg"
  >
    ☰
  </button>

  <!-- Sidebar -->
  <aside
    class={`fixed md:static w-64 h-screen bg-gradient-to-b from-green-800 to-green-900 text-white shadow-lg transform transition-transform duration-300 z-40 ${
      isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
    }`}
  >
    <!-- Logo -->
    <div class="p-6 border-b border-green-700">
      <div class="flex items-center gap-3 mb-2">
        <div class="text-3xl">🌾</div>
        <div>
          <h1 class="text-xl font-bold">Smart Farming</h1>
          <p class="text-xs text-green-100">v2.0</p>
        </div>
      </div>
    </div>

    <!-- User Info -->
    <div class="p-4 border-b border-green-700 mx-3 mt-3 rounded-lg bg-green-700/50">
      <p class="text-xs text-green-100">Logged in as</p>
      <p class="font-semibold truncate">{$authStore.user.name}</p>
      <p class="text-xs text-green-200">{$authStore.user.farmSize} • {$authStore.user.crop}</p>
    </div>

    <!-- Navigation Menu -->
    <nav class="flex-1 overflow-y-auto py-4">
      <div class="px-2 space-y-1">
        {#each menuItems as item}
          <button
            on:click={() => navigate(item.id)}
            class={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
              currentPage === item.id
                ? 'bg-white text-green-800 shadow-md'
                : 'text-green-100 hover:bg-green-700/50'
            }`}
          >
            <span class="text-xl">{item.icon}</span>
            <span class="font-medium">{item.label}</span>
            {#if currentPage === item.id}
              <span class="ml-auto text-lg">→</span>
            {/if}
          </button>
        {/each}
      </div>
    </nav>

    <!-- Footer -->
    <div class="p-4 border-t border-green-700 space-y-2">
      <button
        on:click={() => navigate('profile')}
        class="w-full flex items-center gap-2 px-4 py-2 text-green-100 hover:bg-green-700/50 rounded-lg transition"
      >
        <span>👤</span>
        <span>View Profile</span>
      </button>
      <button
        on:click={handleLogout}
        class="w-full flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition font-medium"
      >
        <span>🚪</span>
        <span>Logout</span>
      </button>
    </div>
  </aside>

  <!-- Overlay for mobile -->
  {#if isOpen}
    <div
      class="fixed inset-0 bg-black/50 z-30 md:hidden"
      on:click={() => (isOpen = false)}
    ></div>
  {/if}
</div>

<style>
  aside {
    max-height: 100vh;
  }
</style>
