<template>
  <section v-if="metrics" class="metrics-hud">
    <div class="metric-card">
      <div class="m-info">
        <span class="m-label">Capacidad Total</span>
        <span class="m-value">{{ metrics.total_capacity }}</span>
      </div>
      <div class="m-icon">🪑</div>
    </div>
    
    <div class="metric-card">
      <div class="m-info">
        <span class="m-label">Invitados Hoy</span>
        <span class="m-value">{{ metrics.reserved_guests }}</span>
      </div>
      <div class="m-icon">👥</div>
    </div>

    <div class="metric-card occupancy-card">
      <div class="occ-info">
        <span class="m-label">Ocupación Actual</span>
        <span class="m-percent" :class="getOccupancyColor(metrics.occupancy_percentage, 'text')">
          {{ metrics.occupancy_percentage }}%
        </span>
      </div>
      <div class="occ-bar-track">
        <div 
          class="occ-bar-fill" 
          :style="{ width: `${metrics.occupancy_percentage}%` }"
          :class="getOccupancyColor(metrics.occupancy_percentage, 'bg')"
        ></div>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  metrics: {
    type: Object,
    required: true
  }
});

const getOccupancyColor = (val, type) => {
  const isBg = type === 'bg';
  if (val >= 90) return isBg ? 'bg-danger' : 'text-danger';
  if (val >= 70) return isBg ? 'bg-warning' : 'text-warning';
  return isBg ? 'bg-success' : 'text-success';
};
</script>

<style scoped>
.metrics-hud {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
}
.metric-card {
  background: white;
  padding: 1.25rem 1.1rem;
  border-radius: 1.25rem;
  border: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.m-label { font-size: 0.75rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; }
.m-value { font-size: 1.75rem; font-weight: 800; color: #0f172a; display: block; }
.m-icon { font-size: 1.5rem; opacity: 0.1; }
.occupancy-card { flex-direction: column; align-items: stretch; gap: 0.5rem; }
.occ-info { display: flex; justify-content: space-between; align-items: center; }
.m-percent { font-size: 1.25rem; font-weight: 800; }
.occ-bar-track { height: 8px; background: #f1f5f9; border-radius: 10px; overflow: hidden; }
.occ-bar-fill { height: 100%; transition: width 0.6s ease; }
.bg-success { background: #22c55e; } .bg-warning { background: #f59e0b; } .bg-danger { background: #ef4444; }
.text-success { color: #22c55e; } .text-warning { color: #f59e0b; } .text-danger { color: #ef4444; }
</style>