<script>
  import { createEventDispatcher } from 'svelte'
  import { login } from '../stores/authStore'
  import { languageStore, t } from '../stores/i18nStore'

  const dispatch = createEventDispatcher()

  let username = 'demo'
  let password = 'demo123'
  let error = ''
  let loading = false
  let showPassword = false

  async function handleLogin() {
    error = ''
    if (!username || !password) {
      error = t('login.errorRequired', $languageStore)
      return
    }

    loading = true
    const result = await login(username, password)

    if (result.success) {
      dispatch('navigate', 'dashboard')
    } else {
      error = result.error || t('login.errorFailed', $languageStore)
    }
    loading = false
  }

  function handleKeyPress(e) {
    if (e.key === 'Enter') handleLogin()
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-green-900 via-green-700 to-emerald-600 flex items-center justify-center p-4">
  <!-- Animated background -->
  <div class="absolute inset-0 overflow-hidden">
    <div class="absolute top-20 left-20 w-72 h-72 bg-green-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
    <div class="absolute top-40 right-20 w-72 h-72 bg-blue-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
  </div>

  <div class="relative z-10 w-full max-w-md">
    <!-- Card -->
    <div class="bg-white rounded-2xl shadow-2xl overflow-hidden animate-slide-in">
      <!-- Header -->
      <div class="bg-gradient-to-r from-green-500 to-emerald-600 px-8 py-8 text-center">
        <div class="text-5xl mb-3">🌾</div>
        <h1 class="text-3xl font-bold text-white mb-2">{t('login.header', $languageStore)}</h1>
        <p class="text-green-50">{t('login.subheader', $languageStore)}</p>
      </div>

      <!-- Form -->
      <div class="px-8 py-8">
        {#if error}
          <div class="mb-6 p-4 bg-red-50 border-l-4 border-red-500 rounded">
            <p class="text-red-700 text-sm font-medium">{error}</p>
          </div>
        {/if}

        <form on:submit|preventDefault={handleLogin}>
        <div class="mb-6">
          <label for="username" class="block text-sm font-semibold text-gray-700 mb-2">
            {t('login.username', $languageStore)}
          </label>
          <input
            id="username"
            type="text"
            bind:value={username}
            on:keypress={handleKeyPress}
            placeholder={t('login.usernamePlaceholder', $languageStore)}
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
            disabled={loading}
          />
        </div>

        <div class="mb-6">
          <label for="password" class="block text-sm font-semibold text-gray-700 mb-2">
            {t('login.password', $languageStore)}
          </label>
          <div class="relative">
            {#if showPassword}
              <input
                id="password"
                type="text"
                bind:value={password}
                on:keypress={handleKeyPress}
                placeholder={t('login.passwordPlaceholder', $languageStore)}
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                disabled={loading}
              />
            {:else}
              <input
                id="password"
                type="password"
                bind:value={password}
                on:keypress={handleKeyPress}
                placeholder={t('login.passwordPlaceholder', $languageStore)}
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                disabled={loading}
              />
            {/if}
            <button
              type="button"
              on:click={() => (showPassword = !showPassword)}
              class="absolute right-3 top-3 text-gray-500 hover:text-gray-700"
            >
              {showPassword ? '👁️' : '👁️‍🗨️'}
            </button>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          class="w-full bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-bold py-3 px-4 rounded-lg transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? t('login.loggingIn', $languageStore) : t('login.button', $languageStore)}
        </button>
        </form>

        <p class="text-center text-gray-600 text-sm mt-4">
          {t('login.demo', $languageStore)}
        </p>
      </div>

      <!-- Footer -->
      <div class="bg-gray-50 px-8 py-4 border-t border-gray-100">
        <p class="text-center text-gray-600 text-sm">
          {t('login.noAccount', $languageStore)}
          <button
            on:click={() => dispatch('navigate', 'signup')}
            class="text-green-600 hover:text-green-700 font-semibold"
          >
            {t('login.signup', $languageStore)}
          </button>
        </p>
      </div>
    </div>

    <!-- Features highlight -->
    <div class="mt-8 grid grid-cols-3 gap-4 text-center text-white text-sm">
      <div class="flex flex-col items-center">
        <div class="text-2xl mb-2">📊</div>
        <p class="font-semibold">Real-time Data</p>
      </div>
      <div class="flex flex-col items-center">
        <div class="text-2xl mb-2">🌧️</div>
        <p class="font-semibold">Weather API</p>
      </div>
      <div class="flex flex-col items-center">
        <div class="text-2xl mb-2">💡</div>
        <p class="font-semibold">Smart Insights</p>
      </div>
    </div>
  </div>
</div>

<style>
  @keyframes blob {
    0%, 100% {
      transform: translate(0, 0) scale(1);
    }
    33% {
      transform: translate(30px, -50px) scale(1.1);
    }
    66% {
      transform: translate(-20px, 20px) scale(0.9);
    }
  }

  :global(.animate-blob) {
    animation: blob 7s infinite;
  }

  :global(.animation-delay-2000) {
    animation-delay: 2s;
  }
</style>
