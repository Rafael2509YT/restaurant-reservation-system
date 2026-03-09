<template>
  <div class="admin-tables">
    <h2>Gestion de Mesas</h2>
    
    <div v-if="error" class="error-message">{{ error }}</div>
    
    <div class="tables-list">
      <table>
        <thead>
          <tr>
            <th>Número</th>
            <th>Capacidad</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="table in tables" :key="table.id">
            <td>{{ table.number }}</td>
            <td>
              <div class="capacity-edit">
                <select 
                  v-model="pendingCapacities[table.id]" 
                  class="capacity-select">
                  <option v-for="opt in capacityOptions" :key="opt" :value="opt">{{ opt }}</option>
                </select>
                <button 
                  v-if="pendingCapacities[table.id] !== table.capacity"
                  @click="commitCapacity(table)" 
                  class="mini-success-btn">
                  Actualizar
                </button>
              </div>
            </td>
            <td>{{ table.is_active ? 'Activa' : 'Desactivada' }}</td>
            <td class="table-actions">
              <button 
                @click="store.toggleTableStatus(table)" 
                :class="table.is_active ? 'warning-btn' : 'success-btn'">
                {{ table.is_active ? 'Desactivar' : 'Activar' }}
              </button>
              <button @click="deleteTable(table.id)" class="danger-btn"> Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="add-table">
      <h3>Agregar Nueva Mesa</h3>
      <form @submit.prevent="createTable" class="table-form">
        <input type="text" v-model="form.number" placeholder="Número de Mesa" required />
        <select v-model="form.capacity" required class="form-select">
          <option value="" disabled>Capacidad</option>
          <option v-for="opt in capacityOptions" :key="opt" :value="opt">{{ opt }} personas</option>
        </select>
        <label>
          <input type="checkbox" v-model="form.is_active" /> Activa
        </label>
        <button type="submit" :disabled="loading">Agregar Mesa</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useReservationStore } from '../stores/reservationStore';
import { storeToRefs } from 'pinia';

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
    // Initialize pending capacities
    tables.value.forEach(t => {
        pendingCapacities.value[t.id] = t.capacity;
    });
});

// Watch tables to react to external changes or initial load
import { watch } from 'vue';
watch(tables, (newTables) => {
    newTables.forEach(t => {
        if (!(t.id in pendingCapacities.value)) {
            pendingCapacities.value[t.id] = t.capacity;
        }
    });
}, { deep: true });

const commitCapacity = async (table) => {
    const newCapacity = pendingCapacities.value[table.id];
    try {
        await store.updateTable(table.id, { capacity: newCapacity });
    } catch(e) {
        // Error is shown in alert for explicit feedback
        alert(store.error);
        // Reset to original value on failure
        pendingCapacities.value[table.id] = table.capacity;
    }
};

const createTable = async () => {
    try {
        await store.createTable(form.value);
        form.value.number = '';
        form.value.capacity = 2;
        form.value.is_active = true;
    } catch(e) { /* Error handled in store */ }
};

const deleteTable = async (id) => {
    if(confirm("¿Estás seguro de que quieres eliminar esta mesa?")) {
        try {
            await store.deleteTable(id);
        } catch(e) {
            alert(store.error);
        }
    }
};
</script>

<style scoped>
.admin-tables {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 30px;
}
.tables-list table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}
.tables-list th, .tables-list td {
  border: 1px solid #eee;
  padding: 10px;
  text-align: left;
}
.tables-list th {
  background: #f9f9f9;
}
.danger-btn {
  background-color: #f44336;
  color: white;
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  width: 100px;
  cursor: pointer;
}
.warning-btn {
  background-color: #ff9800;
  color: white;
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  width: 100px;
  cursor: pointer;
}
.success-btn {
  background-color: #4caf50;
  color: white;
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  width: 100px;
  cursor: pointer;
}
.table-actions {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  min-width: 210px;
}
.add-table {
  border-top: 1px solid #eee;
  padding-top: 20px;
}
.table-form {
  display: flex;
  gap: 10px;
  align-items: center;
}
.table-form input[type="text"], .table-form input[type="number"], .table-form select {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.capacity-select {
    padding: 2px 5px;
    border-radius: 4px;
    border: 1px solid #ddd;
    background: #fdfdfd;
}
.capacity-edit {
    display: flex;
    align-items: center;
    gap: 5px;
}
.mini-success-btn {
    background-color: #4caf50;
    color: white;
    padding: 2px 5px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.8em;
}
.error-message {
  color: red;
  margin-bottom: 15px;
  background: #ffebee;
  padding: 10px;
  border-radius: 4px;
}
</style>
