<template>
  <div class="config-section-container">
    <!-- TÍTULO DE SECCIÓN (Sustituye al header pesado) -->
    <div class="section-top-bar">
      <div class="section-title-group">
        <h3 class="section-title">Parámetros de Operación</h3>
        <p class="section-subtitle">Horarios y lógica de reservación</p>
      </div>
      
      <!-- ÉXITO EN LINEA -->
      <transition name="fade-slide">
        <div v-if="successMsg" class="toast-success">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg>
          {{ successMsg }}
        </div>
      </transition>
    </div>

    <!-- ERROR BANNER -->
    <transition name="shake">
      <div v-if="error" class="error-strip">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
        {{ error }}
      </div>
    </transition>

    <!-- CARGANDO SKELETON -->
    <BaseLoading v-if="!form" type="skeleton-form" />

    <!-- FORMULARIO -->
    <form @submit.prevent="saveConfig" v-else class="config-inner-grid">
      
      <!-- CARD 1: TIEMPOS -->
      <div class="setting-card">
        <div class="card-header-icon blue">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
          <span>Horario Comercial</span>
        </div>
        
        <div class="form-grid-row">
          <div class="input-block">
            <label>Apertura</label>
            <input type="time" v-model="form.opening_time" required class="premium-input" />
          </div>
          <div class="input-block">
            <label>Cierre</label>
            <input type="time" v-model="form.closing_time" required class="premium-input" />
          </div>
        </div>
      </div>

      <!-- CARD 2: REGLAS -->
      <div class="setting-card">
        <div class="card-header-icon amber">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path></svg>
          <span>Reglas de Mesa</span>
        </div>

        <div class="input-block mb-4">
          <label>Frecuencia de Slots</label>
          <div class="input-group-addon">
            <input type="number" v-model="form.reservation_interval_minutes" required min="15" step="15" />
            <span class="unit">min</span>
          </div>
        </div>

        <div class="input-block">
          <label>Tiempo de Estancia</label>
          <div class="input-group-addon">
            <input type="number" v-model="form.reservation_duration_minutes" required min="30" step="15" />
            <span class="unit">min</span>
          </div>
        </div>
      </div>

      <!-- ACCIONES -->
      <div class="config-footer">
        <button type="submit" :disabled="loading" class="btn-save-settings">
          <span v-if="!loading" class="flex-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="mr-2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline><polyline points="7 3 7 8 15 8"></polyline></svg>
            Guardar cambios
          </span>
          <span v-else class="loader-dots"></span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useReservationStore } from '../stores/reservationStore';
import { storeToRefs } from 'pinia';
import BaseLoading from './BaseLoading.vue';

const store = useReservationStore();
const { loading, error } = storeToRefs(store);
const successMsg = ref('');
const form = ref(null);

onMounted(async () => {
    await store.fetchConfig();
    if (store.config) {
        form.value = { ...store.config };
    }
});

const saveConfig = async () => {
    successMsg.value = '';
    try {
        await store.updateConfig(form.value);
        successMsg.value = "Configuración actualizada";
        setTimeout(() => successMsg.value = '', 4000);
    } catch (e) {
    }
};
</script>

<style scoped>
.config-section-container {
  width: 100%;
  background: white;
  border-radius: 1rem;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  margin-bottom: 2rem;
}

/* Header Compacto */
.section-top-bar {
  padding: 1.25rem 1.5rem;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: space-between;
  align-items: center;
}

.section-title { font-size: 0.95rem; font-weight: 800; color: #0f172a; margin: 0; }
.section-subtitle { font-size: 0.75rem; color: #64748b; margin: 0; }

.toast-success {
  background: #10b981;
  color: white;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.4rem 0.8rem;
  border-radius: 2rem;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

/* Grid Interno */
.config-inner-grid {
  padding: 1.5rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.25rem;
}

.setting-card {
  background: #fdfdfd;
  padding: 1.25rem;
  border-radius: 12px;
  border: 1px solid #f1f5f9;
  display: flex;
  flex-direction: column;
}

.card-header-icon {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.85rem;
  font-weight: 700;
  margin-bottom: 1.25rem;
}
.card-header-icon.blue { color: #3b82f6; }
.card-header-icon.amber { color: #f59e0b; }

/* Inputs Estilizados */
.form-grid-row { 
  display: flex; 
  gap: 1rem; 
  flex-wrap: wrap;
}

.input-block { 
  display: flex; 
  flex-direction: column; 
  gap: 0.4rem; 
  flex: 1;
  min-width: 140px;
}

.input-block label { font-size: 0.75rem; font-weight: 700; color: #475569; }

.premium-input, .input-group-addon input {
  width: 100%;
  padding: 0.6rem 0.75rem;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 0.9rem;
  background: white;
  color: #1e293b;
  transition: all 0.2s;
}

.premium-input:focus, .input-group-addon input:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
  outline: none;
}

.input-group-addon {
  position: relative;
  display: flex;
  align-items: center;
}

.input-group-addon .unit {
  position: absolute;
  right: 12px;
  font-size: 0.7rem;
  font-weight: 700;
  color: #94a3b8;
  text-transform: uppercase;
}

/* Footer y Botón */
.config-footer {
  display: flex;
  justify-content: flex-end;
  padding: 0 1.5rem 1.5rem;
}

.btn-save-settings {
  background: #0f172a;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 10px;
  font-weight: 700;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
  width: auto;
}

@media (max-width: 640px) {
  .config-inner-grid {
    padding: 1rem;
    grid-template-columns: 1fr;
  }
  .section-top-bar {
    padding: 1rem;
  }
  .config-footer {
    padding: 0 1rem 1rem;
  }
  .btn-save-settings {
    width: 100%;
  }
}

.flex-center { display: flex; align-items: center; }
.mr-2 { margin-right: 0.5rem; }

/* Otros */
.error-strip {
  margin: 1rem 1.5rem 0;
  padding: 0.75rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
  border-radius: 8px;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.mb-4 { margin-bottom: 1rem; }

/* Animaciones */
.fade-slide-enter-active { transition: all 0.3s ease-out; }
.fade-slide-enter-from { opacity: 0; transform: translateX(10px); }
</style>