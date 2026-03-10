<template>
  <div class="dashboard-container">
    <!-- 1. CABECERA DE CONTEXTO -->
    <header class="dashboard-header">
      <div class="header-content">
        <h1 class="page-title">Panel de Control</h1>
        <p class="page-subtitle">Monitoreo de reservaciones y configuración operativa en tiempo real.</p>
      </div>
    </header>
    
    <!-- 2. MÉTRICAS RÁPIDAS (KPIs) -->
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

    <!-- 3. GRID OPERATIVO -->
    <div class="admin-grid-layout">
      <section id="config" class="scroll-mt">
        <AdminConfig />
      </section>
      <section id="tables" class="scroll-mt">
        <AdminTables />
      </section>
    </div>

    <!-- 4. CALENDARIO DETALLADO (DATATABLE) -->
    <section id="calendar" class="scroll-mt reservations-section">
      <div class="section-card">
        
        <!-- TOOLBAR CORREGIDA (Sin choques visuales) -->
        <div class="card-toolbar">
          <div class="toolbar-left">
            <h2 class="card-title">Listado de Reservas</h2>
            <div class="search-box">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="search-icon"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
              <input 
                type="text" 
                v-model="searchQuery" 
                placeholder="Buscar cliente, email o mesa..." 
                class="search-input"
              />
            </div>
          </div>
          
          <div class="filters-bar">
            <div class="filter-item">
              <label>Filtrar por Fecha</label>
              <input type="date" v-model="filters.date" @change="handleApiFilterChange" />
            </div>
            <div class="filter-item">
              <label>Estado</label>
              <select v-model="filters.status" @change="handleApiFilterChange">
                <option value="">Todos</option>
                <option value="confirmed">Confirmadas</option>
                <option value="pending">Pendientes</option>
                <option value="cancelled">Canceladas</option>
              </select>
            </div>
            <button @click="resetFilters" class="btn-reset-icon" title="Limpiar todo">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path><path d="M3 3v5h5"></path></svg>
            </button>
          </div>
        </div>

        <!-- TABLA -->
        <div class="table-wrapper">
          <table v-if="paginatedReservations.length > 0" class="data-table">
            <thead>
              <tr>
                <th @click="toggleSort('time')" class="sortable">
                  Horario <span class="sort-indicator" :class="getSortClass('time')"></span>
                </th>
                <th @click="toggleSort('name')" class="sortable">
                  Cliente <span class="sort-indicator" :class="getSortClass('name')"></span>
                </th>
                <th @click="toggleSort('guests')" class="sortable">
                  Pax <span class="sort-indicator" :class="getSortClass('guests')"></span>
                </th>
                <th @click="toggleSort('table_number')" class="sortable">
                  Mesa <span class="sort-indicator" :class="getSortClass('table_number')"></span>
                </th>
                <th @click="toggleSort('status')" class="sortable">
                  Estado <span class="sort-indicator" :class="getSortClass('status')"></span>
                </th>
                <th class="text-right">Gestión</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="res in paginatedReservations" :key="res.id" :class="['row-anim', res.status]">
                <td class="time-col">
                  <strong>{{ formatTime(res.time) }}</strong>
                  <span>{{ res.date }}</span>
                </td>
                <td class="client-col">
                  <div class="name-main">{{ res.name }}</div>
                  <div class="email-sub">{{ res.email }}</div>
                </td>
                <td><span class="guests-pill">{{ res.guests }}</span></td>
                <td><span class="table-pill">Mesa {{ res.table_details?.number || '?' }}</span></td>
                <td><span :class="['status-pill', res.status]">{{ res.status }}</span></td>
                <td class="text-right">
                  <button 
                    v-if="res.status !== 'cancelled'" 
                    @click="cancelReservation(res.id)" 
                    class="btn-action-delete"
                  >
                    Anular
                  </button>
                </td>
              </tr>
            </tbody>
          </table>

          <div v-else class="table-empty-state">
            <div v-if="loading" class="loader-container">
              <div class="spinner"></div>
              <p>Sincronizando datos...</p>
            </div>
            <div v-else class="empty-msg">
              <p>No hay resultados.</p>
            </div>
          </div>
        </div>

        <!-- PAGINACIÓN -->
        <div class="table-footer">
          <div class="footer-summary">
            Mostrando <strong>{{ paginationStart + 1 }} - {{ paginationEnd }}</strong> de <strong>{{ totalFiltered }}</strong>
          </div>
          <div class="footer-controls">
            <div class="rows-select">
              <span>Ver:</span>
              <select v-model="itemsPerPage" @change="currentPage = 1">
                <option :value="5">5</option>
                <option :value="10">10</option>
                <option :value="25">25</option>
              </select>
            </div>
            <div class="pagination-pages">
              <button @click="currentPage--" :disabled="currentPage === 1" class="btn-nav">‹</button>
              <span class="page-info">Pág. {{ currentPage }} de {{ totalPages }}</span>
              <button @click="currentPage++" :disabled="currentPage === totalPages" class="btn-nav">›</button>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useReservationStore } from '../stores/reservationStore';
import { storeToRefs } from 'pinia';
import AdminConfig from './AdminConfig.vue';
import AdminTables from './AdminTables.vue';

const store = useReservationStore();
const { adminReservations, loading, error } = storeToRefs(store);

const filters = ref({ date: '', status: '' });
const metrics = ref(null);
const searchQuery = ref('');
const currentPage = ref(1);
const itemsPerPage = ref(10);
const sortKey = ref('time'); 
const sortOrder = ref('asc');

const processedReservations = computed(() => {
  let list = [...adminReservations.value];
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase();
    list = list.filter(res => 
      res.name.toLowerCase().includes(q) || 
      res.email.toLowerCase().includes(q) ||
      res.table_details?.number?.toString().includes(q)
    );
  }
  list.sort((a, b) => {
    let aVal, bVal;
    if (sortKey.value === 'table_number') {
      aVal = a.table_details?.number || 0;
      bVal = b.table_details?.number || 0;
    } else {
      aVal = a[sortKey.value];
      bVal = b[sortKey.value];
    }
    if (typeof aVal === 'number' && typeof bVal === 'number') {
      return sortOrder.value === 'asc' ? aVal - bVal : bVal - aVal;
    }
    const strA = aVal?.toString().toLowerCase() || '';
    const strB = bVal?.toString().toLowerCase() || '';
    return sortOrder.value === 'asc' ? strA.localeCompare(strB) : strB.localeCompare(strA);
  });
  return list;
});

const totalFiltered = computed(() => processedReservations.value.length);
const totalPages = computed(() => Math.ceil(totalFiltered.value / itemsPerPage.value) || 1);
const paginationStart = computed(() => (currentPage.value - 1) * itemsPerPage.value);
const paginationEnd = computed(() => Math.min(paginationStart.value + itemsPerPage.value, totalFiltered.value));
const paginatedReservations = computed(() => processedReservations.value.slice(paginationStart.value, paginationEnd.value));

const fetchData = async () => {
    await store.fetchAdminReservations(filters.value.date, filters.value.status);
    metrics.value = await store.fetchMetrics(filters.value.date || undefined);
};

const handleApiFilterChange = () => { currentPage.value = 1; fetchData(); };
const resetFilters = () => { filters.value = { date: '', status: '' }; searchQuery.value = ''; fetchData(); };
const toggleSort = (key) => {
  if (sortKey.value === key) sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  else { sortKey.value = key; sortOrder.value = 'asc'; }
};
const getSortClass = (key) => {
  if (sortKey.value !== key) return '';
  return sortOrder.value === 'asc' ? 'asc' : 'desc';
};
const cancelReservation = async (id) => {
  if (confirm("¿Anular reservación?")) { await store.adminCancelReservation(id); await fetchData(); }
};
const formatTime = (t) => t ? t.substring(0, 5) : '--:--';
const getOccupancyColor = (val, type) => {
  if (val >= 90) return type === 'bg' ? 'bg-danger' : 'text-danger';
  if (val >= 70) return type === 'bg' ? 'bg-warning' : 'text-warning';
  return type === 'bg' ? 'bg-success' : 'text-success';
};
watch(searchQuery, () => currentPage.value = 1);
onMounted(() => fetchData());
</script>

<style scoped>
/* ESTRUCTURA BASE */
.dashboard-container { max-width: 1400px; margin: 0 auto; padding: 0 2rem 4rem; display: flex; flex-direction: column; gap: 2.5rem; }
.dashboard-header { margin-top: 1rem; }
.page-title { font-size: 2rem; font-weight: 800; color: #0f172a; margin: 0; }
.page-subtitle { color: #64748b; font-size: 1rem; }

/* HUD METRICS */
.metrics-hud { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.5rem; }
.metric-card { background: white; padding: 1.5rem; border-radius: 1.25rem; border: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; }
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

/* GRID OPERATIVO */
.admin-grid-layout { display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 2rem; }
.scroll-mt { scroll-margin-top: 100px; }

/* NAVBAR DE LA TABLA (CORRECCIÓN AQUÍ) */
.section-card { background: white; border-radius: 1.5rem; border: 1px solid #e2e8f0; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.04); overflow: hidden; }

.card-toolbar {
  padding: 1.5rem 2rem;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap; /* Importante para responsivo */
  gap: 2rem;
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex: 1; /* Permite crecer pero limitaremos el search-box */
  min-width: 300px;
}

.search-box {
  position: relative;
  max-width: 350px; /* EVITA QUE CHOQUE CON LOS FILTROS */
  width: 100%;
}

.search-icon { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #94a3b8; }
.search-input {
  width: 100%;
  padding: 0.6rem 1rem 0.6rem 2.5rem;
  border-radius: 0.75rem;
  border: 1px solid #cbd5e1;
  font-size: 0.9rem;
  transition: border-color 0.2s;
}
.search-input:focus { border-color: #6366f1; outline: none; box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1); }

.filters-bar {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  flex-shrink: 0; /* IMPIDE QUE LOS FILTROS SE ACHIQUEN */
}

.filter-item { display: flex; flex-direction: column; gap: 0.25rem; }
.filter-item label { font-size: 0.65rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; }
.filter-item input, .filter-item select { padding: 0.4rem 0.6rem; border-radius: 0.5rem; border: 1px solid #cbd5e1; font-size: 0.85rem; background: white; }

.btn-reset-icon { background: white; border: 1px solid #e2e8f0; padding: 0.6rem; border-radius: 0.5rem; color: #64748b; cursor: pointer; }

/* DATA TABLE */
.table-wrapper { overflow-x: auto; }
.data-table { width: 100%; border-collapse: collapse; text-align: left; min-width: 900px; }
.data-table th { padding: 1rem 1.5rem; font-size: 0.75rem; font-weight: 700; color: #64748b; text-transform: uppercase; background: #fafafa; border-bottom: 1px solid #f1f5f9; }
.sortable { cursor: pointer; }
.sort-indicator { display: inline-block; width: 8px; height: 8px; margin-left: 5px; opacity: 0.3; border: 4px solid transparent; position: relative; }
.sort-indicator.asc { border-bottom-color: #6366f1; opacity: 1; top: -4px; }
.sort-indicator.desc { border-top-color: #6366f1; opacity: 1; top: 4px; }

.data-table td { padding: 1.25rem 1.5rem; border-bottom: 1px solid #f1f5f9; font-size: 0.9rem; }
.client-col .name-main { font-weight: 700; color: #0f172a; }
.client-col .email-sub { font-size: 0.75rem; color: #64748b; }
.status-pill { padding: 0.3rem 0.7rem; border-radius: 2rem; font-size: 0.75rem; font-weight: 700; text-transform: capitalize; }
.status-pill.confirmed { background: #dcfce7; color: #166534; }
.status-pill.pending { background: #fef3c7; color: #92400e; }
.status-pill.cancelled { background: #fee2e2; color: #991b1b; }

/* FOOTER PAGINACIÓN */
.table-footer { padding: 1.25rem 2rem; background: #f8fafc; display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #e2e8f0; }
.footer-summary { font-size: 0.85rem; color: #64748b; }
.footer-controls { display: flex; align-items: center; gap: 2rem; }
.rows-select select { padding: 0.2rem; border-radius: 4px; border: 1px solid #cbd5e1; }
.pagination-pages { display: flex; align-items: center; gap: 1rem; }
.btn-nav { width: 32px; height: 32px; border: 1px solid #cbd5e1; border-radius: 8px; background: white; cursor: pointer; }
.btn-nav:disabled { opacity: 0.3; cursor: not-allowed; }

.table-empty-state { padding: 5rem; text-align: center; }
.spinner { width: 32px; height: 32px; border: 3px solid #e2e8f0; border-top-color: #6366f1; border-radius: 50%; animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 1024px) {
  .card-toolbar { gap: 1.5rem; }
  .toolbar-left { min-width: 100%; }
  .search-box { max-width: 100%; }
  .filters-bar { width: 100%; justify-content: flex-start; }
}
</style>