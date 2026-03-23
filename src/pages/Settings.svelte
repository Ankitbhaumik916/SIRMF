<script>
  import { languageStore, SUPPORTED_LANGUAGES, setLanguage, t } from '../stores/i18nStore'

  let saved = false

  function handleLanguageChange(event) {
    setLanguage(event.target.value)
    saved = true
    setTimeout(() => {
      saved = false
    }, 1800)
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 md:p-8 md:pl-72">
  <header class="bg-white shadow-md md:rounded-lg md:mb-8">
    <div class="px-8 py-6">
      <h1 class="text-3xl font-bold text-gray-900">⚙️ {t('settings.title', $languageStore)}</h1>
      <p class="text-gray-500 mt-1">{t('settings.subtitle', $languageStore)}</p>
    </div>
  </header>

  <main class="max-w-3xl mx-auto px-4 md:px-0">
    <div class="bg-white rounded-lg shadow-md p-6 md:p-8 border-l-4 border-emerald-500">
      <h2 class="text-xl font-bold text-gray-900 mb-3">🌐 {t('settings.languageTitle', $languageStore)}</h2>
      <p class="text-gray-600 text-sm mb-5">{t('settings.languageDescription', $languageStore)}</p>

      <label for="languageSelect" class="block text-sm font-semibold text-gray-700 mb-2">
        {t('settings.currentLanguage', $languageStore)}
      </label>
      <select
        id="languageSelect"
        class="w-full md:w-96 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
        value={$languageStore}
        on:change={handleLanguageChange}
      >
        {#each SUPPORTED_LANGUAGES as language}
          <option value={language.code}>{language.name}</option>
        {/each}
      </select>

      {#if saved}
        <p class="mt-4 text-sm font-semibold text-emerald-700">✓ {t('settings.applied', $languageStore)}</p>
      {/if}
    </div>
  </main>
</div>
