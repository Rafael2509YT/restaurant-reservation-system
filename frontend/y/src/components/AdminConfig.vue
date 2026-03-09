<template>
  <div class="admin-config">
    <h2>Horario del Restaurante y ajustes de reservaciones</h2>
    
    <div v-if="error" class="error-message">
        {{ error }}
    </div>
    <div v-if="successMsg" class="success-message">
        {{ successMsg }}
    </div>

    <form @submit.prevent="saveConfig" v-if="form" class="config-form">
      <div class="form-group">
        <label>Apertura</label>
        <input type="time" v-model="form.opening_time" required />
      </div>
      <div class="form-group">
        <label>Cierre</label>
        <input type="time" v-model="form.closing_time" required />
      </div>
      <div class="form-group">
        <label>Reservation Interval (minutes):</label>
        <input type="number" v-model="form.reservation_interval_minutes" required min="15" step="15" />
        <small>E.g., 30 means times available at :00 and :30.</small>
      </div>
      <div class="form-group">x
        <label>Reservation Duration (minutes):</label>
        <input type="number" v-model="form.reservation_duration_minutes" required min="30" step="15" />
        <small>How long each party can stay.</small>
      </div>
      
      <button type="submit" :disabled="loading">
        {{ loading ? 'Guardando...' : 'Guardar Configuración' }}
      </button>
    </form>
    <p v-else>Cargando configuración...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useReservationStore } from '../stores/reservationStore';
import { storeToRefs } from 'pinia';

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
        successMsg.value = "Configuration updated successfully.";
    } catch (e) {
        console.error("Config save error");
    }
};
</script>

<style scoped>
.admin-config {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 30px;
}
.config-form {
  display: flex;
  flex-direction: column;
  max-width: 400px;
}
.form-group {
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
}
.form-group input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.form-group small {
  color: #666;
  margin-top: 4px;
}
.error-message {
  color: red;
  margin-bottom: 15px;
}
.success-message {
  color: #2e7d32;
  margin-bottom: 15px;
  background: #e8f5e9;
  padding: 10px;
  border-radius: 4px;
}
button {
  width: auto;
  align-self: flex-start;
  padding: 10px 20px;
}
</style>
