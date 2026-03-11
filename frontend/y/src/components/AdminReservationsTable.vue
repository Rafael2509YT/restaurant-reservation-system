<template>
  <section id="calendar" class="scroll-mt">
    <div class="section-card">
      <div class="card-toolbar">
        <div class="toolbar-left">
          <h2 class="card-title">Listado de Reservas</h2>
          <div class="search-box">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="search-icon"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            <input type="text" v-model="searchQuery" placeholder="Buscar cliente, email o mesa..." class="search-input" />
          </div>
        </div>
        
        <div class="filters-bar">
          <div class="filter-item">
            <label>Fecha</label>
            <input type="date" v-model="filters.date" @change="handleFilterChange" />
          </div>
          <div class="filter-item">
            <label>Estado</label>
            <select v-model="filters.status" @change="handleFilterChange">
              <option value="">Todos</option>
              <option value="confirmed">Confirmadas</option>
              <option value="pending">Pendientes</option>
              <option value="cancelled">Canceladas</option>
            </select>
          </div>
          <button @click="resetLocalFilters" class="btn-reset-icon" title="Limpiar">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path><path d="M3 3v5h5"></path></svg>
          </button>
        </div>
      </div>

      <div class="table-wrapper">
        <BaseLoading v-if="loading" type="skeleton-table" :count="5" />
        <table v-else-if="paginatedReservations.length > 0" class="data-table">
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
            <tr v-for="res in paginatedReservations" :key="res.id" :class="res.status">
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
                <button v-if="res.status !== 'cancelled'" @click="cancelRes(res.id)" class="btn-action-delete">Anular</button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-else class="table-empty-state">
           <p v-if="loading">Cargando reservaciones...</p>
           <p v-else>No se encontraron resultados.</p>
        </div>
      </div>

      <div class="table-footer">
        <div class="footer-summary">Mostrando <strong>{{ paginationStart + 1 }}-{{ paginationEnd }}</strong> de <strong>{{ totalFiltered }}</strong></div>
        <div class="footer-controls">
          <select v-model="itemsPerPage" @change="currentPage = 1">
            <option :value="5">5</option>
            <option :value="10">10</option>
            <option :value="25">25</option>
          </select>
          <div class="pagination-pages">
            <button @click="currentPage--" :disabled="currentPage === 1" class="btn-nav">‹</button>
            <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
            <button @click="currentPage++" :disabled="currentPage === totalPages" class="btn-nav">›</button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import BaseLoading from './BaseLoading.vue';

const props = defineProps({
  reservations: Array,
  loading: Boolean
});

const emit = defineEmits(['filter-change', 'cancel-res']);

const filters = ref({ date: '', status: '' });
const searchQuery = ref('');
const currentPage = ref(1);
const itemsPerPage = ref(10);
const sortKey = ref('time'); 
const sortOrder = ref('asc');

const processedReservations = computed(() => {
  let list = [...props.reservations];
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase();
    list = list.filter(res => 
      res.name.toLowerCase().includes(q) || 
      res.email.toLowerCase().includes(q) ||
      res.table_details?.number?.toString().includes(q)
    );
  }
  list.sort((a, b) => {
    let aV, bV;
    if (sortKey.value === 'table_number') { aV = a.table_details?.number || 0; bV = b.table_details?.number || 0; }
    else { aV = a[sortKey.value]; bV = b[sortKey.value]; }
    if (typeof aV === 'number' && typeof bV === 'number') return sortOrder.value === 'asc' ? aV - bV : bV - aV;
    return sortOrder.value === 'asc' ? String(aV).localeCompare(String(bV)) : String(bV).localeCompare(String(aV));
  });
  return list;
});

const totalFiltered = computed(() => processedReservations.value.length);
const totalPages = computed(() => Math.ceil(totalFiltered.value / itemsPerPage.value) || 1);
const paginationStart = computed(() => (currentPage.value - 1) * itemsPerPage.value);
const paginationEnd = computed(() => Math.min(paginationStart.value + itemsPerPage.value, totalFiltered.value));
const paginatedReservations = computed(() => processedReservations.value.slice(paginationStart.value, paginationEnd.value));

const handleFilterChange = () => { currentPage.value = 1; emit('filter-change', filters.value); };
const resetLocalFilters = () => { filters.value = { date: '', status: '' }; searchQuery.value = ''; handleFilterChange(); };
const toggleSort = (key) => { if (sortKey.value === key) sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'; else { sortKey.value = key; sortOrder.value = 'asc'; }};
const getSortClass = (k) => sortKey.value === k ? sortOrder.value : '';
const formatTime = (t) => t ? t.substring(0, 5) : '--:--';
const cancelRes = (id) => emit('cancel-res', id);

watch(searchQuery, () => currentPage.value = 1);
</script>

<style scoped>
/* Reutilizamos los estilos de la tabla anterior */
.table-wrapper { overflow-x: auto; -webkit-overflow-scrolling: touch; }
.data-table { width: 100%; border-collapse: collapse; text-align: left; min-width: 800px; }
.section-card { background: white; border-radius: 1.5rem; border: 1px solid #e2e8f0; overflow: hidden; }
.card-toolbar { padding: 1.25rem 1.5rem; background: #f8fafc; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1.25rem; }
.toolbar-left { display: flex; align-items: center; gap: 1rem; flex: 1; min-width: 250px; }
.search-box { position: relative; max-width: 350px; width: 100%; }
.search-icon { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #94a3b8; }
.search-input { width: 100%; padding: 0.5rem 1rem 0.5rem 2.5rem; border-radius: 0.75rem; border: 1px solid #cbd5e1; font-size: 0.85rem; }
.filters-bar { display: flex; align-items: center; gap: 1rem; }
.filter-item { display: flex; flex-direction: column; gap: 0.25rem; }
.filter-item label { font-size: 0.65rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; }
.filter-item input, .filter-item select { padding: 0.4rem 0.6rem; border-radius: 0.5rem; border: 1px solid #cbd5e1; font-size: 0.85rem; }
.data-table { width: 100%; border-collapse: collapse; text-align: left; }
.data-table th { padding: 1rem 1.5rem; font-size: 0.75rem; color: #64748b; text-transform: uppercase; background: #fafafa; border-bottom: 1px solid #f1f5f9; cursor: pointer; }
.sort-indicator { display: inline-block; width: 8px; height: 8px; margin-left: 5px; opacity: 0.3; border: 4px solid transparent; position: relative; }
.sort-indicator.asc { border-bottom-color: #6366f1; opacity: 1; top: -4px; }
.sort-indicator.desc { border-top-color: #6366f1; opacity: 1; top: 4px; }
.data-table td { padding: 1rem 1.25rem; border-bottom: 1px solid #f1f5f9; font-size: 0.85rem; }
.status-pill { padding: 0.3rem 0.7rem; border-radius: 2rem; font-size: 0.75rem; font-weight: 700; text-transform: capitalize; }
.status-pill.confirmed { background: #dcfce7; color: #166534; }
.status-pill.pending { background: #fef3c7; color: #92400e; }
.status-pill.cancelled { background: #fee2e2; color: #991b1b; }
.btn-action-delete { padding: 0.4rem 0.8rem; background: #fff1f2; border: 1px solid #fecaca; color: #dc2626; border-radius: 8px; font-weight: 600; cursor: pointer; }
.table-footer { padding: 1.25rem 1.5rem; background: #f8fafc; display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #e2e8f0; flex-wrap: wrap; gap: 1rem; }
.pagination-pages { display: flex; align-items: center; gap: 1rem; }
.btn-nav { width: 32px; height: 32px; border: 1px solid #cbd5e1; border-radius: 8px; background: white; cursor: pointer; }
.table-empty-state { padding: 3rem; text-align: center; color: #94a3b8; }

@media (max-width: 768px) {
  .card-toolbar { padding: 1rem; flex-direction: column; align-items: stretch; }
  .toolbar-left { min-width: auto; flex-direction: column; align-items: stretch; }
  .filters-bar { flex-wrap: wrap; justify-content: space-between; }
  .filter-item { flex: 1; min-width: 120px; }
  .search-box { max-width: 100%; }
  .table-footer { flex-direction: column; gap: 1.25rem; padding: 1.5rem 1rem; }
  .footer-controls { width: 100%; justify-content: space-between; }
}
</style>