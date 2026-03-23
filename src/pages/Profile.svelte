<script>
  import { createEventDispatcher } from 'svelte'
  import { authStore } from '../stores/authStore'
  import { languageStore, t } from '../stores/i18nStore'
  import { farmStatsStore } from '../stores/farmStatsStore'

  const dispatch = createEventDispatcher()

  let isEditing = false
  let editData = {
    name: $authStore.user.name,
    farmSize: $authStore.user.farmSize,
    crop: $authStore.user.crop,
    location: $authStore.user.location,
  }
  let error = ''
  let success = false
  let loading = false

  const crops = ['Tomato', 'Rice', 'Wheat', 'Corn', 'Sugarcane', 'Cotton', 'Potato', 'Onion']

  async function handleSaveProfile() {
    error = ''
    success = false
    loading = true

    try {
      const response = await fetch('/api/auth/update-profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(editData),
      })

      const result = await response.json()

      if (response.ok) {
        success = true
        isEditing = false
        setTimeout(() => (success = false), 3000)
      } else {
        error = result.error || 'Failed to update profile'
      }
    } catch (err) {
      error = err.message
    } finally {
      loading = false
    }
  }

  function handleCancel() {
    editData = {
      name: $authStore.user.name,
      farmSize: $authStore.user.farmSize,
      crop: $authStore.user.crop,
      location: $authStore.user.location,
    }
    isEditing = false
    error = ''
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 md:p-8 md:pl-72">
  <!-- Header -->
  <header class="bg-white shadow-md md:rounded-lg md:mb-8">
    <div class="px-8 py-6 md:flex md:items-center md:justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">👤 {t('profile.title', $languageStore)}</h1>
        <p class="text-gray-500 mt-1">{t('profile.subtitle', $languageStore)}</p>
      </div>
    </div>
  </header>

  <!-- Profile Content -->
  <main class="max-w-2xl mx-auto px-4 md:px-0">
    {#if success}
      <div class="mb-6 p-4 bg-green-50 border-l-4 border-green-500 rounded-lg">
        <p class="text-green-700 font-semibold">✓ {t('profile.updated', $languageStore)}</p>
      </div>
    {/if}

    {#if error}
      <div class="mb-6 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg">
        <p class="text-red-700 font-semibold">{error}</p>
      </div>
    {/if}

    <div class="bg-white rounded-lg shadow-lg overflow-hidden">
      <!-- Profile Header -->
      <div class="bg-gradient-to-r from-green-500 to-emerald-600 px-8 py-12 text-center text-white">
        <div class="text-6xl mb-4">👤</div>
        <h2 class="text-3xl font-bold mb-2">{$authStore.user.name}</h2>
        <p class="text-green-100">@{$authStore.user.username}</p>
        <p class="text-green-100 text-sm mt-2">Member since 2026</p>
      </div>

      <!-- Profile Info -->
      <div class="px-8 py-8">
        {#if !isEditing}
          <!-- View Mode -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
            <div>
              <h3 class="text-lg font-semibold text-gray-700 mb-4">{t('profile.personalInfo', $languageStore)}</h3>
              <div class="space-y-4">
                <div>
                  <p class="text-gray-600 text-sm">{t('profile.fullName', $languageStore)}</p>
                  <p class="text-xl font-semibold text-gray-900">{$authStore.user.name}</p>
                </div>
                <div>
                  <p class="text-gray-600 text-sm">{t('profile.username', $languageStore)}</p>
                  <p class="text-xl font-semibold text-gray-900">{$authStore.user.username}</p>
                </div>
                <div>
                  <p class="text-gray-600 text-sm">{t('profile.location', $languageStore)}</p>
                  <p class="text-xl font-semibold text-gray-900">{$authStore.user.location || t('profile.notSet', $languageStore)}</p>
                </div>
              </div>
            </div>

            <div>
              <h3 class="text-lg font-semibold text-gray-700 mb-4">{t('profile.farmInfo', $languageStore)}</h3>
              <div class="space-y-4">
                <div>
                  <p class="text-gray-600 text-sm">{t('profile.farmSize', $languageStore)}</p>
                  <p class="text-xl font-semibold text-green-600">{$authStore.user.farmSize}</p>
                </div>
                <div>
                  <p class="text-gray-600 text-sm">{t('profile.primaryCrop', $languageStore)}</p>
                  <p class="text-xl font-semibold text-green-600">{$authStore.user.crop}</p>
                </div>
                <div>
                  <p class="text-gray-600 text-sm">{t('profile.accountStatus', $languageStore)}</p>
                  <p class="text-xl font-semibold text-green-600">✓ {t('profile.active', $languageStore)}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Stats -->
          <div class="pt-8 border-t border-gray-200">
            <h3 class="text-lg font-semibold text-gray-700 mb-4">Account Statistics</h3>
            <div class="grid grid-cols-3 gap-4">
              <div class="bg-blue-50 rounded-lg p-6 text-center">
                <p class="text-gray-600 text-sm">Avg Moisture</p>
                <p class="text-3xl font-bold text-blue-600 mt-2">{$farmStatsStore.avgMoisture}%</p>
              </div>
              <div class="bg-green-50 rounded-lg p-6 text-center">
                <p class="text-gray-600 text-sm">Avg Health</p>
                <p class="text-3xl font-bold text-green-600 mt-2">{$farmStatsStore.avgHealth}%</p>
              </div>
              <div class="bg-purple-50 rounded-lg p-6 text-center">
                <p class="text-gray-600 text-sm">Needs Irrigation</p>
                <p class="text-3xl font-bold text-purple-600 mt-2">{$farmStatsStore.farmsNeedingIrrigation}</p>
              </div>
            </div>
          </div>

          <!-- Edit Button -->
          <div class="mt-8 pt-8 border-t border-gray-200">
            <button
              on:click={() => (isEditing = true)}
              class="px-6 py-3 bg-blue-500 text-white font-bold rounded-lg hover:bg-blue-600 transition"
            >
              ✏️ {t('profile.editProfile', $languageStore)}
            </button>
          </div>
        {:else}
          <!-- Edit Mode -->
          <h3 class="text-lg font-semibold text-gray-700 mb-6">{t('profile.editFarmInfo', $languageStore)}</h3>

          <div class="space-y-6 mb-8">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">{t('profile.fullName', $languageStore)}</label>
              <input
                type="text"
                bind:value={editData.name}
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={loading}
              />
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">{t('profile.farmSize', $languageStore)}</label>
                <input
                  type="text"
                  bind:value={editData.farmSize}
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={loading}
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">{t('profile.primaryCrop', $languageStore)}</label>
                <select
                  bind:value={editData.crop}
                  class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={loading}
                >
                  {#each crops as crop}
                    <option value={crop}>{crop}</option>
                  {/each}
                </select>
              </div>
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">{t('profile.location', $languageStore)}</label>
              <input
                type="text"
                bind:value={editData.location}
                placeholder="City, State"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={loading}
              />
              <p class="text-xs text-gray-500 mt-1">{t('profile.weatherDetection', $languageStore)}</p>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex gap-3">
            <button
              on:click={handleCancel}
              disabled={loading}
              class="flex-1 px-4 py-3 border border-gray-300 text-gray-700 font-bold rounded-lg hover:bg-gray-50 transition"
            >
              {t('common.cancel', $languageStore)}
            </button>
            <button
              on:click={handleSaveProfile}
              disabled={loading}
              class="flex-1 px-4 py-3 bg-blue-500 text-white font-bold rounded-lg hover:bg-blue-600 transition disabled:opacity-50"
            >
              {loading ? t('profile.saving', $languageStore) : t('profile.saveChanges', $languageStore)}
            </button>
          </div>
        {/if}
      </div>
    </div>
  </main>
</div>
