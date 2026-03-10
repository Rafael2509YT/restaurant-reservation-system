<template>
  <div class="availability-wrapper">
    <!-- Header Decorativo con Tipografía Refinada -->
    <header class="checker-header">
      <div class="header-content">
        <span class="badge-premium">Experiencia Gastronómica</span>
        <h2 class="main-title">Encuentra tu Mesa</h2>
        <p class="description">Selecciona el momento perfecto para tu visita</p>
      </div>
    </header>

    <!-- Barra de Búsqueda Estilo Consola Pro -->
    <section class="search-container-pro">
      <form @submit.prevent="checkAvailability" class="checker-form-refined">
        
        <div class="search-main-grid">
          <!-- Bloque de Fecha: Calendar Card -->
          <div class="input-card date-selection">
            <div class="input-card-header">
              <div class="icon-circle blue">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
              </div>
              <div class="header-text">
                <label>Fecha de Visita</label>
                <span class="selected-value-hint">{{ date || 'Selecciona un día' }}</span>
              </div>
            </div>
            
            <div class="calendar-integration">
              <BaseCalendar v-model="date" />
            </div>
          </div>

          <!-- Bloque de Invitados: Stepper Card -->
          <div class="input-card guests-selection">
            <div class="input-card-header">
              <div class="icon-circle amber">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle></svg>
              </div>
              <div class="header-text">
                <label>Comensales</label>
                <span class="selected-value-hint">Tamaño del grupo</span>
              </div>
            </div>

            <div class="stepper-horizontal">
              <button type="button" @click="adjustPartySize(-1)" class="btn-step" :disabled="partySize <= 1">−</button>
              <div class="stepper-display">
                <span class="count">{{ partySize }}</span>
                <span class="unit">{{ partySize === 1 ? 'Persona' : 'Personas' }}</span>
              </div>
              <button type="button" @click="adjustPartySize(1)" class="btn-step" :disabled="partySize >= 20">+</button>
            </div>
            <p class="limit-note">Máximo permitido: 20 invitados</p>
          </div>
        </div>

        <!-- Botón de Acción Principal -->
        <div class="search-footer">
          <button type="submit" :disabled="loading" class="btn-search-hero">
            <div v-if="loading" class="btn-loader"></div>
            <span v-else class="btn-content">
              Confirmar Disponibilidad
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
            </span>
          </button>
        </div>
      </form>
    </section>

    <!-- Section: Carga (Skeletons) -->
    <div v-if="loading" class="loading-state">
      <div class="loading-header">
        <div class="spinner-main"></div>
        <h3>Analizando disponibilidad...</h3>
      </div>
      <BaseLoading type="skeleton-card" :count="3" />
    </div>

    <!-- RESULTADOS Y ESTADOS VACÍOS (Lógica original mantenida) -->
    <div v-else-if="availability && availability.length > 0" class="results-section">
      <!-- ... Resto del código de resultados mantenido ... -->
      <div class="results-header">
        <h3>Mesas para el <span>{{ date }}</span></h3>
        <p class="results-count">{{ availability.length }} disponibles</p>
      </div>
      <div class="tables-grid">
        <div v-for="table in availability" :key="table.table_id" class="table-card">
          <!-- Visualización de mesa... -->
          <div class="table-visual">
            <div class="table-shape" :class="table.table_capacity > 4 ? 'large' : 'medium'">
              <span class="table-number">{{ table.table_number }}</span>
              <div v-for="n in parseInt(table.table_capacity)" :key="n" class="chair" :style="getChairStyle(n, table.table_capacity)"></div>
            </div>
          </div>
          <div class="table-info">
            <div class="info-top">
              <h4>Mesa {{ table.table_number }}</h4>
              <span class="capacity-tag">{{ table.table_capacity }} Pers.</span>
            </div>
            <div class="time-slots">
              <div class="times-pill-container">
                <span v-for="(time, index) in table.available_times" :key="index" class="time-pill">{{ time }}</span>
              </div>
            </div>
            <button @click="$emit('select-table', table.table_id)" class="btn-reserve">Reservar esta mesa</button>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else-if="hasChecked && !loading" class="empty-state-container">
      <!-- Estados vacíos... -->
      <div v-if="noCapacity" class="empty-card">
        <div class="empty-icon">🍽️</div>
        <h4>Capacidad no disponible</h4>
        <p>No hay mesas para {{ partySize }} personas.</p>
      </div>
      <div v-else-if="noDate" class="empty-card">
        <div class="empty-icon">📅</div>
        <h4>Sin disponibilidad</h4>
        <p>No hay horarios para el {{ date }}.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useReservationStore } from '../stores/reservationStore';
import { storeToRefs } from 'pinia';
import BaseLoading from './BaseLoading.vue';
import BaseCalendar from './BaseCalendar.vue';

const store = useReservationStore();
const { availability, loading, noCapacity, noDate } = storeToRefs(store);

const date = ref('');
const partySize = ref(2);
const hasChecked = ref(false);

const adjustPartySize = (delta) => {
  const newVal = partySize.value + delta;
  if (newVal >= 1 && newVal <= 20) partySize.value = newVal;
};

const checkAvailability = async () => {
  hasChecked.value = false;
  await store.fetchAvailability(date.value, partySize.value);
  hasChecked.value = true;
};

const getChairStyle = (index, total) => {
  const angle = (index / total) * 360;
  return { transform: `rotate(${angle}deg) translateY(-35px)` };
};

onMounted(() => {
  date.value = new Date().toISOString().split('T')[0];
});
</script>

<style scoped>
/* Contenedor Principal */
.availability-wrapper {
  max-width: 1000px;
  margin: 0 auto;
  padding: 3rem 1rem;
  font-family: 'Inter', system-ui, sans-serif;
}

/* Header Estilizado */
.checker-header { text-align: center; margin-bottom: 3rem; }
.badge-premium {
  background: #eef2ff;
  color: #4f46e5;
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.main-title { font-size: 2.5rem; font-weight: 900; color: #0f172a; margin: 1rem 0 0.5rem; letter-spacing: -0.02em; }
.description { color: #64748b; font-size: 1.1rem; }

/* Contenedor de Búsqueda Pro */
.search-container-pro {
  background: #ffffff;
  padding: 2.5rem;
  border-radius: 2rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.08);
  border: 1px solid #f1f5f9;
  max-width: 850px;
  margin: 0 auto 4rem;
}

.search-main-grid {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 2rem;
}

/* Tarjetas de Entrada */
.input-card {
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 1.5rem;
  border: 1px solid #e2e8f0;
}

.input-card-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.icon-circle {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.icon-circle.blue { background: #dbeafe; color: #2563eb; }
.icon-circle.amber { background: #fef3c7; color: #d97706; }

.header-text label { display: block; font-weight: 800; font-size: 0.85rem; color: #1e293b; text-transform: uppercase; }
.selected-value-hint { font-size: 0.75rem; color: #64748b; }

/* Calendar Wrapper */
.calendar-integration { background: white; border-radius: 1rem; padding: 0.5rem; border: 1px solid #e2e8f0; }

/* Stepper Modernizado */
.stepper-horizontal {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  padding: 0.5rem;
  border-radius: 1.25rem;
  border: 1px solid #e2e8f0;
}

.btn-step {
  width: 48px;
  height: 48px;
  border: none;
  background: #f1f5f9;
  color: #0f172a;
  border-radius: 1rem;
  font-size: 1.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-step:hover:not(:disabled) { background: #e2e8f0; transform: scale(1.05); }
.btn-step:active:not(:disabled) { transform: scale(0.95); }
.btn-step:disabled { opacity: 0.3; cursor: not-allowed; }

.stepper-display { text-align: center; }
.stepper-display .count { display: block; font-size: 1.75rem; font-weight: 900; color: #0f172a; line-height: 1; }
.stepper-display .unit { font-size: 0.75rem; font-weight: 700; color: #64748b; text-transform: uppercase; }

.limit-note { text-align: center; margin-top: 1rem; font-size: 0.75rem; font-weight: 600; color: #94a3b8; }

/* Botón Hero */
.search-footer { margin-top: 2rem; padding-top: 2rem; border-top: 1px solid #f1f5f9; display: flex; justify-content: center; }

.btn-search-hero {
  width: 100%;
  max-width: 350px;
  background: #0f172a;
  color: white;
  padding: 1.25rem;
  border-radius: 1.25rem;
  border: none;
  font-size: 1rem;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 10px 20px rgba(15, 23, 42, 0.2);
}

.btn-search-hero:hover:not(:disabled) {
  background: #1e293b;
  transform: translateY(-3px);
  box-shadow: 0 15px 30px rgba(15, 23, 42, 0.3);
}

.btn-content { display: flex; align-items: center; justify-content: center; gap: 0.75rem; }

/* Loading States */
.loading-state { text-align: center; padding: 2rem; }
.loading-header { margin-bottom: 2rem; }
.spinner-main {
  width: 40px; height: 40px;
  border: 4px solid #f1f5f9; border-top-color: #6366f1;
  border-radius: 50%; animation: spin 0.8s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* Grid de Mesas Mejorado */
.tables-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.table-card {
  background: white; border-radius: 1.5rem; border: 1px solid #e2e8f0;
  transition: all 0.3s ease; overflow: hidden;
}
.table-card:hover { transform: translateY(-8px); box-shadow: 0 20px 30px rgba(0,0,0,0.05); }

.table-visual { height: 120px; background: #f8fafc; display: flex; align-items: center; justify-content: center; }
.table-shape { width: 60px; height: 60px; border: 4px solid #94a3b8; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; background: white; position: relative; }
.table-shape.large { width: 80px; height: 60px; border-radius: 30px; }
.chair { position: absolute; width: 12px; height: 8px; background: #cbd5e1; border-radius: 3px; }

.table-info { padding: 1.5rem; }
.info-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.info-top h4 { margin: 0; font-weight: 800; }
.capacity-tag { font-size: 0.7rem; font-weight: 800; background: #f1f5f9; padding: 0.3rem 0.6rem; border-radius: 2rem; }

.time-pill { background: #eef2ff; color: #4338ca; padding: 0.4rem 0.8rem; border-radius: 0.75rem; font-size: 0.8rem; font-weight: 700; }

.btn-reserve {
  width: 100%; padding: 0.8rem; margin-top: 1rem; border-radius: 1rem; border: none;
  background: #6366f1; color: white; font-weight: 700; cursor: pointer; transition: 0.2s;
}
.btn-reserve:hover { background: #4f46e5; }

/* Responsive */
@media (max-width: 768px) {
  .search-main-grid { grid-template-columns: 1fr; }
  .search-container-pro { padding: 1.5rem; }
  .main-title { font-size: 1.8rem; }
}
</style>