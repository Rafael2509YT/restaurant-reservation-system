<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <div class="header-content">
        <h1 class="page-title">Panel de Control</h1>
        <p class="page-subtitle">Monitoreo de reservaciones y configuración operativa.</p>
      </div>
    </header>
    
    <!-- NUEVO COMPONENTE DE MÉTRICAS -->
    <AdminMetrics :metrics="metrics" />

    <div class="admin-grid-layout">
      <section id="config" class="scroll-mt">
        <AdminConfig />
      </section>
      <section id="tables" class="scroll-mt">
        <AdminTables />
      </section>
    </div>

    <!-- NUEVO COMPONENTE DE TABLA DE RESERVAS -->
    <AdminReservationsTable 
      :reservations="adminReservations" 
      :loading="loading"
      @filter-change="handleExternalFilter"
      @cancel-res="handleCancelReservation"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useReservationStore } from '../stores/reservationStore';
import { storeToRefs } from 'pinia';

// Importación de componentes 
import AdminConfig from './AdminConfig.vue';
import AdminTables from './AdminTables.vue';
import AdminMetrics from './AdminMetrics.vue';
import AdminReservationsTable from './AdminReservationsTable.vue';

const store = useReservationStore();
const { adminReservations, loading } = storeToRefs(store);
const metrics = ref(null);

const fetchData = async (filters = { date: '', status: '' }) => {
    await store.fetchAdminReservations(filters.date, filters.status);
    metrics.value = await store.fetchMetrics(filters.date || undefined);
};

const handleExternalFilter = (newFilters) => {
    fetchData(newFilters);
};

const handleCancelReservation = async (id) => {
    if (confirm("¿Confirmas la anulación de esta reservación?")) {
        await store.adminCancelReservation(id);
        await fetchData();
    }
};

onMounted(() => fetchData());
</script>

<style scoped>
.dashboard-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1rem 3rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.dashboard-header { margin-top: 1rem; }
.page-title { font-size: 2rem; font-weight: 800; color: #0f172a; margin: 0; }
.page-subtitle { color: #64748b; font-size: 1rem; }
.admin-grid-layout {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  align-items: start;
}
.scroll-mt { scroll-margin-top: 100px; }
</style>