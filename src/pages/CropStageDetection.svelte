<script>
  import { authStore } from '../stores/authStore'
  import { languageStore, t } from '../stores/i18nStore'

  const stageDescriptions = {
    germination: 'Seed sprouting and initial root/shoot emergence.',
    vegetative: 'Rapid leaf and stem development stage.',
    flowering: 'Flower initiation and bloom period.',
    maturity: 'Final stage before or at harvest readiness.',
  }

  let selectedFile = null
  let previewUrl = ''
  let loading = false
  let error = ''
  let prediction = null

  function onFileSelect(event) {
    error = ''
    prediction = null

    const file = event.target.files?.[0]
    if (!file) return

    if (!file.type.startsWith('image/')) {
      error = 'Please upload a valid image file.'
      return
    }

    if (file.size > 8 * 1024 * 1024) {
      error = 'Image size should be under 8 MB.'
      return
    }

    selectedFile = file
    previewUrl = URL.createObjectURL(file)
  }

  function fileToBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.onload = () => {
        const dataUrl = reader.result
        const base64 = dataUrl.split(',')[1]
        resolve(base64)
      }
      reader.onerror = () => reject(new Error('Failed to read image file.'))
      reader.readAsDataURL(file)
    })
  }

  async function runPrediction() {
    if (!selectedFile) {
      error = 'Please select an image first.'
      return
    }

    loading = true
    error = ''
    prediction = null

    try {
      const imageBase64 = await fileToBase64(selectedFile)

      const response = await fetch('/api/crop-stage/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ imageBase64 }),
      })

      const contentType = response.headers.get('content-type') || ''
      if (!contentType.includes('application/json')) {
        const rawText = await response.text()
        const shortBody = rawText.slice(0, 120).replace(/\s+/g, ' ').trim()
        throw new Error(
          `Server returned non-JSON response (status ${response.status}). Ensure backend is running. Response starts with: ${shortBody}`
        )
      }

      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.error || `Prediction failed with status ${response.status}`)
      }

      prediction = data
    } catch (err) {
      error = err.message
    } finally {
      loading = false
    }
  }

  function clearSelection() {
    selectedFile = null
    prediction = null
    error = ''
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl)
      previewUrl = ''
    }
  }
</script>

<div class="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 md:p-8 md:pl-72">
  <header class="bg-white shadow-md md:rounded-lg md:mb-8">
    <div class="px-8 py-6">
      <h1 class="text-3xl font-bold text-gray-900">🌱 {t('cropStage.title', $languageStore)}</h1>
      <p class="text-gray-500 mt-1">{t('cropStage.subtitle', $languageStore)}</p>
    </div>
  </header>

  <main class="max-w-4xl mx-auto px-4 md:px-0">
    <div class="bg-white rounded-lg shadow-lg p-6 md:p-8">
      <div class="mb-4 p-4 rounded-lg bg-emerald-50 border border-emerald-100">
        <p class="text-sm text-emerald-800">
          {t('cropStage.profileCrop', $languageStore)} <span class="font-semibold">{$authStore.user?.crop || t('profile.notSet', $languageStore)}</span>
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label for="cropImageFile" class="block text-sm font-semibold text-gray-700 mb-2">{t('cropStage.cropImage', $languageStore)}</label>
          <input
            id="cropImageFile"
            type="file"
            accept="image/*"
            on:change={onFileSelect}
            class="w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:border-0 file:rounded-md file:bg-emerald-600 file:text-white hover:file:bg-emerald-700"
          />

          <div class="mt-4 flex gap-3">
            <button
              on:click={runPrediction}
              disabled={loading || !selectedFile}
              class="px-5 py-2.5 bg-emerald-600 text-white rounded-lg font-semibold hover:bg-emerald-700 disabled:opacity-50"
            >
              {loading ? t('cropStage.analyzing', $languageStore) : t('cropStage.detect', $languageStore)}
            </button>
            <button
              on:click={clearSelection}
              disabled={loading}
              class="px-5 py-2.5 border border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 disabled:opacity-50"
            >
              {t('common.clear', $languageStore)}
            </button>
          </div>

          {#if error}
            <p class="mt-4 text-sm text-red-600 font-medium">{error}</p>
          {/if}
        </div>

        <div class="bg-gray-50 border border-gray-200 rounded-lg p-4 min-h-[240px] flex items-center justify-center">
          {#if previewUrl}
            <img src={previewUrl} alt="Selected crop" class="max-h-60 rounded-md object-contain" />
          {:else}
            <p class="text-gray-500 text-sm">{t('cropStage.preview', $languageStore)}</p>
          {/if}
        </div>
      </div>

      {#if prediction}
        <div class="mt-8 p-5 rounded-lg border border-blue-100 bg-blue-50">
          <h2 class="text-lg font-bold text-gray-900 mb-3">{t('cropStage.result', $languageStore)}</h2>

          {#if prediction.note}
            <div class="mb-3 rounded-md border border-amber-300 bg-amber-50 px-3 py-2 text-sm text-amber-800">
              {prediction.note}
            </div>
          {/if}

          {#if prediction.error}
            <div class="mb-3 rounded-md border border-red-300 bg-red-50 px-3 py-2 text-sm text-red-700">
              {prediction.error}
            </div>
          {/if}

          <div class="space-y-2 text-sm">
            <p><span class="font-semibold">{t('cropStage.crop', $languageStore)}</span> {prediction.cropType}</p>
            <p><span class="font-semibold">{t('cropStage.stage', $languageStore)}</span> {prediction.stage}</p>
            <p><span class="font-semibold">{t('cropStage.confidence', $languageStore)}</span> {(prediction.confidence * 100).toFixed(2)}%</p>
            <p><span class="font-semibold">{t('cropStage.model', $languageStore)}</span> {prediction.model}</p>
          </div>

          {#if stageDescriptions[prediction.stage]}
            <p class="mt-3 text-sm text-gray-700">{stageDescriptions[prediction.stage]}</p>
          {/if}

          {#if prediction.topPredictions?.length}
            <div class="mt-4">
              <h3 class="font-semibold text-gray-800 mb-2">{t('cropStage.topPredictions', $languageStore)}</h3>
              <ul class="space-y-1 text-sm text-gray-700">
                {#each prediction.topPredictions as item}
                  <li>{item.stage}: {(item.confidence * 100).toFixed(2)}%</li>
                {/each}
              </ul>
            </div>
          {/if}
        </div>
      {/if}
    </div>
  </main>
</div>
