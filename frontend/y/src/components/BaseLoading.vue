<template>
  <div :class="['loading-container', type, { 'absolute': absolute }]">
    <!-- SPINNER TYPE -->
    <div v-if="type === 'spinner'" class="spinner-box">
      <div class="spinner"></div>
      <slot><span class="loader-text">Cargando...</span></slot>
    </div>

    <!-- SKELETON CARD (For Table Availability) -->
    <div v-else-if="type === 'skeleton-card'" class="skeleton-grid">
      <div v-for="n in count" :key="n" class="sk-card">
        <div class="sk-visual pulse"></div>
        <div class="sk-content">
          <div class="sk-line title pulse"></div>
          <div class="sk-line sub pulse"></div>
          <div class="sk-btn pulse"></div>
        </div>
      </div>
    </div>

    <!-- SKELETON TABLE (For Admin Lists) -->
    <div v-else-if="type === 'skeleton-table'" class="sk-table">
      <div class="sk-table-header pulse"></div>
      <div v-for="n in count" :key="n" class="sk-table-row pulse"></div>
    </div>

    <!-- SKELETON FORM (For Config/Details) -->
    <div v-else-if="type === 'skeleton-form'" class="sk-form">
      <div class="sk-form-header pulse"></div>
      <div class="sk-form-grid">
        <div v-for="n in 4" :key="n" class="sk-form-item pulse"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  type: {
    type: String,
    default: 'spinner' // spinner, skeleton-card, skeleton-table, skeleton-form
  },
  count: {
    type: Number,
    default: 3
  },
  absolute: {
    type: Boolean,
    default: false
  }
});
</script>

<style scoped>
.loading-container {
  width: 100%;
}
.loading-container.absolute {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(255, 255, 255, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  backdrop-filter: blur(2px);
}

/* Base Pulse Animation */
@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 0.3; }
  100% { opacity: 0.6; }
}
.pulse {
  animation: pulse 1.5s ease-in-out infinite;
  background: #e2e8f0;
  border-radius: 8px;
}

/* Spinner Styles */
.spinner-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f1f5f9;
  border-top-color: #6366f1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.loader-text {
  font-size: 0.875rem;
  font-weight: 600;
  color: #64748b;
}

/* Skeleton Card Styles */
.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}
.sk-card {
  background: white;
  border-radius: 1.25rem;
  border: 1px solid #e2e8f0;
  overflow: hidden;
}
.sk-visual { height: 140px; width: 100%; }
.sk-content { padding: 1.5rem; display: flex; flex-direction: column; gap: 1rem; }
.sk-line { height: 1.2rem; width: 60%; }
.sk-line.sub { width: 40%; height: 0.8rem; }
.sk-btn { height: 40px; width: 100%; margin-top: 1rem; }

/* Skeleton Table Styles */
.sk-table { width: 100%; display: flex; flex-direction: column; gap: 1rem; }
.sk-table-header { height: 50px; width: 100%; margin-bottom: 0.5rem; }
.sk-table-row { height: 60px; width: 100%; }

/* Skeleton Form Styles */
.sk-form { width: 100%; padding: 2rem; background: #f8fafc; border-radius: 1rem; }
.sk-form-header { height: 30px; width: 40%; margin-bottom: 2rem; }
.sk-form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
.sk-form-item { height: 60px; width: 100%; }

@media (max-width: 768px) {
  .sk-form-grid { grid-template-columns: 1fr; }
}
</style>
