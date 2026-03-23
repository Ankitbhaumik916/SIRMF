<script>
  import { onMount } from 'svelte'
  import { authStore, checkAuth, logout } from './stores/authStore'
  import Login from './pages/Login.svelte'
  import Signup from './pages/Signup.svelte'
  import Dashboard from './pages/Dashboard.svelte'
  import IrrigationReport from './pages/IrrigationReport.svelte'
  import Profile from './pages/Profile.svelte'
  import Weather from './pages/Weather.svelte'
  import FarmInfo from './pages/FarmInfo.svelte'
  import CropStageDetection from './pages/CropStageDetection.svelte'
  import SoilCheck from './pages/SoilCheck.svelte'
  import Settings from './pages/Settings.svelte'
  import Sidebar from './components/Sidebar.svelte'
  import { languageStore, t } from './stores/i18nStore'

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
      <h2 class="text-2xl font-bold text-gray-700 mb-2">{t('app.title', $languageStore)}</h2>
      <p class="text-gray-500">{t('app.loading', $languageStore)}</p>
    </div>
  </div>
{:else if !$authStore.isAuthenticated}
  {#if currentPage === 'login'}
    <Login on:navigate={handleNavigation} />
  {:else if currentPage === 'signup'}
    <Signup on:navigate={handleNavigation} />
  {/if}
{:else}
  <div class="flex h-screen bg-white">
    <Sidebar on:navigate={handleNavigation} />
    <main class="flex-1 overflow-auto bg-white">
      {#if currentPage === 'dashboard'}
        <Dashboard on:navigate={handleNavigation} />
      {:else if currentPage === 'profile'}
        <Profile on:navigate={handleNavigation} />
      {:else if currentPage === 'weather'}
        <Weather on:navigate={handleNavigation} />
      {:else if currentPage === 'irrigation'}
        <IrrigationReport />
      {:else if currentPage === 'crop-stage'}
        <CropStageDetection />
      {:else if currentPage === 'soil-check'}
        <SoilCheck />
      {:else if currentPage === 'farm'}
        <FarmInfo />
      {:else if currentPage === 'settings'}
        <Settings />
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
