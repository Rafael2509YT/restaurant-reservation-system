<template>
  <div class="availability-checker">
    <h2>Verificar Disponibilidad</h2>
    <form @submit.prevent="checkAvailability" class="checker-form">
      <div class="form-group">
        <label for="date">Fecha:</label>
        <input type="date" id="date" v-model="date" required :min="today" />
      </div>
      <div class="form-group">
        <label for="partySize">Party Size (optional):</label>
        <input type="number" id="partySize" v-model="partySize" min="1" max="20" />
      </div>
      <button type="submit" :disabled="loading">
        {{ loading ? 'Checking...' : 'Check Availability' }}
      </button>
    </form>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <div v-if="availability && availability.length > 0" class="results">
      <h3>Mesas disponibles para el {{ date }}</h3>
      <div class="tables-grid">
        <div v-for="table in availability" :key="table.table_id" class="table-card">
          <h4>Mesa {{ table.table_number }}</h4>
          <p>Capacidad: {{ table.table_capacity }} personas</p>
          <div v-if="table.available_times?.length > 0" class="reserved-times">
            <p>Horarios disponibles:</p>
            <ul class="times-list">
              <li v-for="(time, index) in table.available_times" :key="index">
                {{ time }}
              </li>
            </ul>
          </div>
          <div v-else class="available-all-day">
            <p>No available times</p>
          </div>
          <button @click="$emit('select-table', table.table_id)" :disabled="!table.available_times?.length">Reservar esta Mesa</button>
        </div>
      </div>
    </div>
    <div v-else-if="hasChecked && !loading">
      <div v-if="noCapacity" class="no-results no-results--capacity">
        <p>⚠️ No hay mesas disponibles para <strong>{{ partySize }} personas</strong> en esa fecha.</p>
        <p><small>Intenta con un grupo más pequeño o elige otra fecha.</small></p>
      </div>
      <div v-else-if="noDate" class="no-results no-results--date">
        <p>📅 No hay disponibilidad para el <strong>{{ date }}</strong>.</p>
        <p><small>Por favor selecciona otra fecha.</small></p>
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

</script>

<style scoped>
.availability-checker {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
.checker-form {
  display: flex;
  gap: 15px;
  align-items: flex-end;
  margin-bottom: 20px;
}
.form-group {
  display: flex;
  flex-direction: column;
}
.table-card {
  border: 1px solid #ccc;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 10px;
}
.tables-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
}
.error-message {
  color: red;
  margin-bottom: 15px;
}
.no-results {
  text-align: center;
  padding: 20px;
  background: #fff3e0;
  border-radius: 8px;
  border-left: 5px solid #ff9800;
  margin-top: 20px;
}
.no-results--capacity, .no-results--date {
    background: #e1f5fe;
    border-left-color: #03a9f4;
}
.times-list {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  list-style: none;
  padding: 0;
}
.times-list li {
  background: #e0f7fa;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9em;
}
</style>
