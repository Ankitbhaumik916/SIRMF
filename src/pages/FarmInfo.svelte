<div class="farm-info-page">
	<iframe
		class="simulation-frame"
		src="/impl1"
		title="SIRMF ML Farm Intelligence"
		loading="lazy"
		referrerpolicy="same-origin"
	></iframe>
</div>

<style>
	.farm-info-page {
		width: 100%;
		min-height: calc(100vh - 64px);
		background: #08110c;
	}

	.simulation-frame {
		width: 100%;
		min-height: calc(100vh - 64px);
		border: 0;
		display: block;
	}

	@media (max-width: 768px) {
		.farm-info-page {
			min-height: calc(100vh - 56px);
		}

		.simulation-frame {
			min-height: calc(100vh - 56px);
		}
	}
</style>
