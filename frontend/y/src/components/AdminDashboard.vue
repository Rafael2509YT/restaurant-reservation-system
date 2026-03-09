<template>
  <div class="admin-dashboard">
    <h1>Admin Dashboard</h1>
    
    <div class="admin-sections">
      <AdminConfig />
      <AdminTables />
    </div>

    <div class="reservations-section">
      <h2>Reservations Calendar</h2>
      
      <div class="filters">
        <label>
          Date:
          <input type="date" v-model="filters.date" @change="fetchData" />
        </label>
        <label>
          Status:
          <select v-model="filters.status" @change="fetchData">
            <option value="">All</option>
            <option value="confirmed">Confirmed</option>
            <option value="pending">Pending</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </label>
        <button @click="resetFilters">Reset</button>
      </div>

      <div v-if="metrics" class="metrics">
        <h3>Ocupación {{ metrics.date }}</h3>
        <p>Capacidad Total: {{ metrics.total_capacity }}</p>
        <p>Invitados: {{ metrics.reserved_guests }}</p>
        <div class="progress-bar">
          <div class="progress" :style="{ width: `${metrics.occupancy_percentage}%` }">
            {{ metrics.occupancy_percentage }}%
          </div>
        </div>
      </div>

      <div v-if="loading" class="loading">Loading data...</div>
      <div v-else-if="error" class="error-message">{{ error }}</div>
      
      <table v-else-if="adminReservations.length > 0" class="res-table">
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Hora</th>
            <th>Nombre</th>
            <th>Invitados</th>
            <th>Mesa</th>
            <th>Estado</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="res in adminReservations" :key="res.id" :class="res.status">
            <td>{{ res.date }}</td>
            <td>{{ formatTime(res.time) }}</td>
            <td>{{ res.name }}<br><small>{{ res.phone }}</small></td>
            <td>{{ res.guests }}</td>
            <td>{{ res.table_details?.number || '?' }}</td>
            <td class="status-cell">{{ res.status }}</td>
            <td>
              <button 
                v-if="res.status !== 'cancelled'" 
                @click="cancelReservation(res.id)" 
                class="danger-btn">
                Cancel
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No reservations found.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useReservationStore } from '../stores/reservationStore';
import { storeToRefs } from 'pinia';
import AdminConfig from './AdminConfig.vue';
import AdminTables from './AdminTables.vue';

const store = useReservationStore();
const { adminReservations, loading, error } = storeToRefs(store);

const filters = ref({
    date: '',
    status: ''
});

const metrics = ref(null);

const fetchData = async () => {
    await store.fetchAdminReservations(filters.value.date, filters.value.status);
    if (filters.value.date) {
        metrics.value = await store.fetchMetrics(filters.value.date);
    } else {
        metrics.value = await store.fetchMetrics(); // Gets today by default
    }
};

onMounted(() => {
    fetchData();
});

const resetFilters = () => {
    filters.value.date = '';
    filters.value.status = '';
    fetchData();
};

const cancelReservation = async (id) => {
    if(confirm("Are you sure you want to cancel this reservation?")) {
        try {
            await store.adminCancelReservation(id);
            await fetchData();
        } catch(e) {
            alert("Could not cancel reservation.");
        }
    }
};

const formatTime = (timeStr) => {
    if (!timeStr) return '';
    return timeStr.substring(0, 5); // display HH:MM
};
</script>

<style scoped>
.admin-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
.filters {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  align-items: center;
  background: #f5f5f5;
  padding: 15px;
  border-radius: 8px;
}
.metrics {
  background: #e3f2fd;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}
.progress-bar {
  background: #ccc;
  border-radius: 10px;
  height: 20px;
  overflow: hidden;
  margin-top: 10px;
}
.progress {
  background: #4caf50;
  height: 100%;
  color: white;
  text-align: center;
  font-size: 12px;
  line-height: 20px;
  transition: width 0.3s;
}
.res-table {
  width: 100%;
  border-collapse: collapse;
}
.res-table th, .res-table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
}
.res-table th {
  background-color: #f5f5f5;
}
.status-cell {
  text-transform: capitalize;
  font-weight: bold;
}
tr.cancelled .status-cell { color: #f44336; }
tr.confirmed .status-cell { color: #4caf50; }
tr.pending .status-cell { color: #ff9800; }

.danger-btn {
  background-color: #f44336;
  color: white;
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
}
</style>
