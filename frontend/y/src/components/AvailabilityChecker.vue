<template>
  <div class="availability-wrapper">
    <!-- Header Decorativo -->
    <header class="checker-header">
      <div class="header-content">
        <span class="subtitle">Reserva tu experiencia culinaria</span>
        <h2 class="title">Verificar Disponibilidad</h2>
      </div>
    </header>

    <!-- Barra de Búsqueda Estilo Premium -->
    <section class="search-container">
      <form @submit.prevent="checkAvailability" class="checker-form">
        <div class="input-group">
          <label for="date">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
            Fecha
          </label>
          <input type="date" id="date" v-model="date" required :min="today" class="custom-input" />
        </div>

        <div class="input-group">
          <label for="partySize">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="icon"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
            Comensales
          </label>
          <input type="number" id="partySize" v-model="partySize" min="1" max="20" placeholder="¿Cuántas personas?" class="custom-input" />
        </div>

        <button type="submit" :disabled="loading" class="btn-search">
          <span v-if="!loading">Buscar Mesas</span>
          <span v-else class="loader-inline"></span>
        </button>
      </form>
    </section>

    <!-- Errores -->
    <div v-if="error" class="error-toast">
      {{ error }}
    </div>

    <!-- RESULTADOS: Grid de Mesas -->
    <div v-if="availability && availability.length > 0" class="results-section">
      <div class="results-header">
        <h3>Mesas disponibles para el <span>{{ date }}</span></h3>
        <p class="results-count">{{ availability.length }} opciones encontradas</p>
      </div>

      <div class="tables-grid">
        <div v-for="table in availability" :key="table.table_id" class="table-card" :class="{ 'disabled': !table.available_times?.length }">
          
          <!-- Representación Gráfica de la Mesa -->
          <div class="table-visual">
            <div class="table-shape" :class="table.table_capacity > 4 ? 'large' : 'medium'">
              <span class="table-number">{{ table.table_number }}</span>
              <!-- Generar sillas visualmente según capacidad -->
              <div v-for="n in parseInt(table.table_capacity)" :key="n" class="chair" :style="getChairStyle(n, table.table_capacity)"></div>
            </div>
          </div>

          <div class="table-info">
            <div class="info-top">
              <h4>Mesa {{ table.table_number }}</h4>
              <span class="capacity-tag">Capacidad: {{ table.table_capacity }}</span>
            </div>
            
            <div v-if="table.available_times?.length > 0" class="time-slots">
              <p class="slots-title">Horarios libres:</p>
              <div class="times-pill-container">
                <span v-for="(time, index) in table.available_times" :key="index" class="time-pill">
                  {{ time }}
                </span>
              </div>
            </div>
            <div v-else class="no-times-status">
              Sin horarios disponibles
            </div>

            <button 
              @click="$emit('select-table', table.table_id)" 
              class="btn-reserve" 
              :disabled="!table.available_times?.length"
            >
              Reservar ahora
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ESTADOS VACÍOS -->
    <div v-else-if="hasChecked && !loading" class="empty-state-container">
      <div v-if="noCapacity" class="empty-card capacity">
        <div class="empty-icon">🍽️</div>
        <h4>No hay mesas para {{ partySize }} personas</h4>
        <p>Intenta reducir el número de invitados o cambiar la fecha.</p>
      </div>
      <div v-else-if="noDate" class="empty-card date">
        <div class="empty-icon">📅</div>
        <h4>Día Completo</h4>
        <p>No tenemos disponibilidad para el {{ date }}. ¡Prueba otro día!</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useReservationStore } from '../stores/reservationStore';
import { storeToRefs } from 'pinia';

const store = useReservationStore();
const { availability, loading, error, noCapacity, noDate } = storeToRefs(store);

const date = ref('');
const partySize = ref('');
const hasChecked = ref(false);

const today = computed(() => {
  const d = new Date();
  return d.toISOString().split('T')[0];
});

const checkAvailability = async () => {
  hasChecked.value = false;
  await store.fetchAvailability(date.value, partySize.value);
  hasChecked.value = true;
};

// Lógica visual para posicionar sillas alrededor de la mesa circular/ovalada
const getChairStyle = (index, total) => {
  const angle = (index / total) * 360;
  return {
    transform: `rotate(${angle}deg) translateY(-35px)`
  };
};
</script>

<style scoped>
.availability-wrapper {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem 1rem;
  font-family: 'Inter', sans-serif;
  color: #1e293b;
}

/* Header */
.checker-header {
  text-align: center;
  margin-bottom: 2.5rem;
}
.subtitle {
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-size: 0.8rem;
  font-weight: 600;
  color: #6366f1;
}
.title {
  font-size: 2.25rem;
  font-weight: 800;
  color: #0f172a;
  margin-top: 0.5rem;
}

/* Search Bar */
.search-container {
  background: white;
  padding: 1.5rem;
  border-radius: 1.25rem;
  box-shadow: 0 10px 30px -10px rgba(0,0,0,0.1);
  border: 1px solid #e2e8f0;
  margin-bottom: 3rem;
}

.checker-form {
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  gap: 1.5rem;
  align-items: flex-end;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #64748b;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.custom-input {
  padding: 0.75rem 1rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.75rem;
  font-size: 1rem;
  transition: all 0.2s;
}

.custom-input:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
}

.btn-search {
  background: #0f172a;
  color: white;
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 0.75rem;
  font-weight: 600;
  height: 48px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-search:hover:not(:disabled) {
  background: #1e293b;
  transform: translateY(-1px);
}

/* Grid de Mesas */
.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.results-header h3 span { color: #6366f1; }
.results-count { font-size: 0.9rem; color: #64748b; font-weight: 500; }

.tables-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.table-card {
  background: white;
  border-radius: 1.25rem;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.table-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 25px -5px rgba(0,0,0,0.05);
  border-color: #cbd5e1;
}

/* Visualización de la Mesa */
.table-visual {
  height: 140px;
  background: #f8fafc;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.table-shape {
  width: 70px;
  height: 70px;
  background: #fff;
  border: 4px solid #94a3b8;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  color: #475569;
  position: relative;
  z-index: 2;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
}

.table-shape.large { width: 90px; height: 70px; border-radius: 40px; }

.chair {
  position: absolute;
  width: 14px;
  height: 10px;
  background: #cbd5e1;
  border-radius: 4px 4px 2px 2px;
  top: 50%;
  left: 50%;
  margin-left: -7px;
  margin-top: -5px;
  z-index: 1;
}

/* Info de la Mesa */
.table-info {
  padding: 1.5rem;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.info-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.info-top h4 { margin: 0; font-size: 1.15rem; font-weight: 700; }

.capacity-tag {
  background: #f1f5f9;
  padding: 0.25rem 0.6rem;
  border-radius: 2rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: #475569;
}

.time-slots { margin-bottom: 1.5rem; }
.slots-title { font-size: 0.8rem; color: #94a3b8; font-weight: 600; text-transform: uppercase; margin-bottom: 0.5rem; }

.times-pill-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.time-pill {
  background: #eef2ff;
  color: #4338ca;
  font-size: 0.85rem;
  font-weight: 600;
  padding: 0.35rem 0.75rem;
  border-radius: 0.5rem;
}

.btn-reserve {
  width: 100%;
  padding: 0.75rem;
  border-radius: 0.75rem;
  border: none;
  background: #6366f1;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  margin-top: auto;
}

.btn-reserve:hover:not(:disabled) { background: #4f46e5; }
.btn-reserve:disabled { background: #e2e8f0; color: #94a3b8; cursor: not-allowed; }

/* Estados Vacíos */
.empty-state-container {
  padding: 2rem 0;
}

.empty-card {
  text-align: center;
  background: #f8fafc;
  border: 2px dashed #e2e8f0;
  padding: 3rem;
  border-radius: 1.5rem;
}

.empty-icon { font-size: 3rem; margin-bottom: 1rem; }
.empty-card h4 { font-size: 1.25rem; margin-bottom: 0.5rem; }
.empty-card p { color: #64748b; }

/* Loader */
.loader-inline {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255,255,255,0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 0.8s linear infinite;
  display: inline-block;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* Responsivo */
@media (max-width: 768px) {
  .checker-form {
    grid-template-columns: 1fr;
  }
  .title { font-size: 1.75rem; }
}
</style>