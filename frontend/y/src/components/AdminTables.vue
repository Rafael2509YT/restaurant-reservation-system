<template>
  <div class="admin-tables-container">
    <header class="section-header">
      <div class="header-content">
        <h2 class="section-title">Gestión de Mesas</h2>
        <span class="table-count" v-if="tables.length">{{ tables.length }} Mesas en total</span>
      </div>
    </header>

    <!-- Error Banner -->
    <transition name="fade">
      <div v-if="error" class="error-alert">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
        {{ error }}
      </div>
    </transition>

    <div class="tables-scroll-area">
      <BaseLoading v-if="loading" type="skeleton-table" :count="5" />
      <table v-else class="modern-admin-table">
        <thead>
          <tr>
            <th>Número</th>
            <th>Capacidad</th>
            <th>Estado</th>
            <th class="text-right">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="table in tables" :key="table.id" :class="{ 'row-inactive': !table.is_active }">
            <td class="table-number-cell">
              <span class="table-icon">🪑</span>
              <strong>Mesa {{ table.number }}</strong>
            </td>
            <td>
              <div class="capacity-editor">
                <select 
                  v-model="pendingCapacities[table.id]" 
                  class="select-minimal">
                  <option v-for="opt in capacityOptions" :key="opt" :value="opt">{{ opt }} pers.</option>
                </select>
                <transition name="scale">
                  <button 
                    v-if="pendingCapacities[table.id] !== table.capacity"
                    @click="commitCapacity(table)" 
                    class="btn-save-mini"
                    title="Guardar cambios">
                    ✓
                  </button>
                </transition>
              </div>
            </td>
            <td>
              <span :class="['status-pill', table.is_active ? 'active' : 'inactive']">
                <span class="dot"></span>
                {{ table.is_active ? 'Activa' : 'Desactivada' }}
              </span>
            </td>
            <td class="actions-cell">
              <div class="actions-group">
                <button 
                  @click="store.toggleTableStatus(table)" 
                  :class="['btn-icon-text', table.is_active ? 'btn-warn' : 'btn-success']"
                  :title="table.is_active ? 'Desactivar mesa' : 'Activar mesa'">
                  <svg v-if="table.is_active" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="9" y1="9" x2="15" y2="15"></line><line x1="15" y1="9" x2="9" y2="15"></line></svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>
                  {{ table.is_active ? 'Pausar' : 'Activar' }}
                </button>
                <button @click="deleteTable(table.id)" class="btn-icon-text btn-danger" title="Eliminar mesa">
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                  Eliminar
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Sección Agregar Mesa -->
    <div class="add-table-section">
      <div class="add-header">
        <h3 class="add-title">Nueva Mesa</h3>
        <p class="add-subtitle">Añade más capacidad a tu restaurante</p>
      </div>
      
      <form @submit.prevent="createTable" class="modern-inline-form">
        <div class="input-group">
          <input type="text" v-model="form.number" placeholder="Ej: 15" required />
          <span class="input-label">Número</span>
        </div>
        
        <div class="input-group">
          <select v-model="form.capacity" required>
            <option v-for="opt in capacityOptions" :key="opt" :value="opt">{{ opt }} personas</option>
          </select>
          <span class="input-label">Capacidad</span>
        </div>

        <div class="checkbox-group">
          <label class="toggle-switch">
            <input type="checkbox" v-model="form.is_active" />
            <span class="slider"></span>
          </label>
          <span class="toggle-label">Activa</span>
        </div>

        <button type="submit" :disabled="loading" class="btn-primary">
          <span v-if="!loading">Agregar Mesa</span>
          <span v-else class="loader-sml"></span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useReservationStore } from '../stores/reservationStore';
import { storeToRefs } from 'pinia';
import BaseLoading from './BaseLoading.vue';

const store = useReservationStore();
const { tables, loading, error } = storeToRefs(store);

const form = ref({
    number: '',
    capacity: 2,
    is_active: true
});

const capacityOptions = [2, 4, 5, 6, 8, 10];
const pendingCapacities = ref({});

onMounted(async () => {
    await store.fetchTables();
    syncPendingCapacities();
});

const syncPendingCapacities = () => {
    tables.value.forEach(t => {
        if (!(t.id in pendingCapacities.value)) {
            pendingCapacities.value[t.id] = t.capacity;
        }
    });
};

watch(tables, () => {
    syncPendingCapacities();
}, { deep: true });

const commitCapacity = async (table) => {
    const newCapacity = pendingCapacities.value[table.id];
    try {
        await store.updateTable(table.id, { capacity: newCapacity });
    } catch(e) {
        alert(store.error);
        pendingCapacities.value[table.id] = table.capacity;
    }
};

const createTable = async () => {
    try {
        await store.createTable(form.value);
        form.value = { number: '', capacity: 2, is_active: true };
    } catch(e) {}
};

const deleteTable = async (id) => {
    if(confirm("¿Estás seguro de que quieres eliminar esta mesa? Esta acción no se puede deshacer.")) {
        try {
            await store.deleteTable(id);
        } catch(e) {
            alert(store.error);
        }
    }
};
</script>

<style scoped>
.admin-tables-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px -5px rgba(0,0,0,0.05);
  border: 1px solid #e2e8f0;
  overflow: hidden;
  font-family: 'Inter', system-ui, sans-serif;
}

.section-header {
  padding: 1.5rem;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0;
}

.table-count {
  font-size: 0.8rem;
  color: #64748b;
  font-weight: 500;
}

/* Tabla Moderna */
.tables-scroll-area {
  overflow-x: auto;
}

.modern-admin-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.modern-admin-table th {
  text-align: left;
  padding: 1rem;
  background: #fff;
  color: #64748b;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  border-bottom: 1px solid #e2e8f0;
}

.modern-admin-table td {
  padding: 1rem;
  border-bottom: 1px solid #f1f5f9;
  color: #334155;
}

.modern-admin-table tr:hover { background-color: #fbfcfe; }
.modern-admin-table tr.row-inactive td { opacity: 0.7; }

.table-number-cell {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.table-icon { font-size: 1.2rem; }

/* Capacidad Editor */
.capacity-editor {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.select-minimal {
  padding: 0.4rem 0.6rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background: #f8fafc;
  font-size: 0.85rem;
  cursor: pointer;
  outline: none;
}

.btn-save-mini {
  background: #22c55e;
  color: white;
  border: none;
  border-radius: 4px;
  width: 24px;
  height: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

/* Status Pills */
.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.25rem 0.75rem;
  border-radius: 2rem;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-pill.active { background: #dcfce7; color: #166534; }
.status-pill.inactive { background: #f1f5f9; color: #64748b; }

.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}
.active .dot { background: #22c55e; box-shadow: 0 0 6px #22c55e; }
.inactive .dot { background: #94a3b8; }

/* Acciones */
.actions-cell { text-align: right; }
.actions-group {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

.btn-icon-text {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 0.8rem;
  border: none;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 90px;
}

.btn-success { background: #f0fdf4; color: #166534; }
.btn-success:hover { background: #dcfce7; }
.btn-warn { background: #fffbeb; color: #92400e; }
.btn-warn:hover { background: #fef3c7; }
.btn-danger { background: #fff1f2; color: #991b1b; }
.btn-danger:hover { background: #fee2e2; }

/* Sección Agregar Mesa */
.add-table-section {
  padding: 2rem;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
}

.add-header { margin-bottom: 1.5rem; }
.add-title { font-size: 1.1rem; font-weight: 700; color: #1e293b; margin: 0; }
.add-subtitle { font-size: 0.85rem; color: #64748b; margin: 0.2rem 0 0 0; }

.modern-inline-form {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  align-items: center;
}

.input-group {
  position: relative;
  flex: 1;
  min-width: 140px;
}

.input-group input, .input-group select {
  width: 100%;
  padding: 0.75rem 0.875rem;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  background: white;
  font-size: 0.9rem;
  outline: none;
}

.input-label {
  position: absolute;
  top: -8px;
  left: 10px;
  background: #f8fafc;
  padding: 0 4px;
  font-size: 0.7rem;
  font-weight: 700;
  color: #6366f1;
  text-transform: uppercase;
}

/* Toggle Switch */
.checkbox-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 22px;
}

.toggle-switch input { opacity: 0; width: 0; height: 0; }

.slider {
  position: absolute;
  cursor: pointer;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: #cbd5e1;
  transition: .4s;
  border-radius: 34px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px; width: 16px;
  left: 3px; bottom: 3px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider { background-color: #6366f1; }
input:checked + .slider:before { transform: translateX(18px); }

.toggle-label { font-size: 0.85rem; font-weight: 600; color: #475569; }

.btn-primary {
  padding: 0.75rem 1.5rem;
  background: #0f172a;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover:not(:disabled) { background: #1e293b; transform: translateY(-1px); }

.error-alert {
  margin: 1rem;
  padding: 0.75rem 1rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
  border-radius: 8px;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Animaciones */
.scale-enter-active, .scale-leave-active { transition: all 0.2s ease; }
.scale-enter-from, .scale-leave-to { transform: scale(0.5); opacity: 0; }

@media (max-width: 768px) {
  .modern-inline-form { flex-direction: column; align-items: stretch; }
  .btn-icon-text { width: 100%; justify-content: center; }
  .actions-group { flex-direction: column; }
}
</style>