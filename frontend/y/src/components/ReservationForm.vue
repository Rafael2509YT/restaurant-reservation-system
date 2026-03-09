
/*este es el formulario de reservacion */
<template>
  <div class="reservation-form">
    <h2>Realiza una reservación</h2>
    <div v-if="success" class="success-message">
        <p>¡Reservación exitosa! Esperamos verte pronto.</p>
        <div v-if="assignedTable" class="assignment-info">
            <p><strong>Mesa Asignada:</strong> {{ assignedTable.number }} (Capacidad: {{ assignedTable.capacity }})</p>
            <p v-if="assignedTable.id !== tableId" class="reassignment-note">
                💡 Hemos seleccionado esta mesa automáticamente para asegurar la disponibilidad de tu reservación y acomodar a tus invitados.
            </p>
        </div>
        <div v-if="uniqueCode" class="cancellation-info">
            <p>Su numero de reservacion es: {{ reservation_id }}</p>
            <strong>Tu código de cancelación:</strong> <span>{{ uniqueCode }}</span>
            <br/><small>por favor guarda esta información si necesitas cancelar tu reservación más tarde.</small>
        </div>
        <button @click="$emit('reset')">Realiza otra reservación</button>
    </div>
    <form v-else @submit.prevent="submitReservation">
      <div class="form-group">
        <label>Selected Table ID:</label>
        <input type="text" :value="tableId" disabled />
      </div>
      
      <div class="form-group">
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="form.customer_name" required />
      </div>

      <div class="form-group">
        <label for="email">Email (optional):</label>
        <input type="email" id="email" v-model="form.customer_email" />
      </div>

      <div class="form-group">
        <label for="phone">Phone (optional):</label>
        <input type="tel" id="phone" v-model="form.customer_phone" />
      </div>

      <div class="form-group">
        <label for="date">Date:</label>
        <input type="date" id="date" v-model="selectedDate" required :min="today" />
      </div>

      <div class="form-group time-duration-group">
        <div>
            <label for="time">Start Time:</label>
            <input type="time" id="time" v-model="selectedTime" required step="1800" />
            <small>Must be within operating hours.</small>
        </div>
        <div>
            <label for="guests">Number of Guests:</label>
            <input type="number" id="guests" v-model="form.guests" required min="1" max="20" />
        </div>
      </div>

      <button type="submit" :disabled="store.loading">
        {{ store.loading ? 'Submitting...' : 'Confirm Reservation' }}
      </button>

      <div v-if="store.error" class="error-message">
        {{ store.error }}
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useReservationStore } from '../stores/reservationStore';

const props = defineProps({
  tableId: {
    type: Number,
    required: true
  }
});

const emit = defineEmits(['reset', 'success']);
const store = useReservationStore();

const today = computed(() => {
  const d = new Date();
  return d.toISOString().split('T')[0];
});

const success = ref(false);
const selectedDate = ref('');
const selectedTime = ref('');
const uniqueCode = ref('');
const reservation_id = ref('');
const assignedTable = ref(null);

const form = ref({
  customer_name: '',
  customer_email: '',
  customer_phone: '',
  guests: 2
});

const submitReservation = async () => {
    const payload = {
        table_id: props.tableId,
        name: form.value.customer_name,
        email: form.value.customer_email || 'noemail@example.com',
        phone: form.value.customer_phone || 'N/A',
        date: selectedDate.value,
        time: selectedTime.value,
        guests: form.value.guests
    };

    try {
        const response = await store.createReservation(payload);
        uniqueCode.value = response.unique_code;
        reservation_id.value = response.id;
        assignedTable.value = response.table_details;
        success.value = true;
        emit('success');
    } catch (e) {
        // error is handled in store and displayed in template
        console.error("Reservation failed:", store.error);
    }
};
</script>

<style scoped>
.reservation-form {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}
.form-group {
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
}
.form-group label {
  margin-bottom: 5px;
  font-weight: bold;
}
.form-group input, .form-group select {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.time-duration-group {
    flex-direction: row;
    gap: 15px;
}
.time-duration-group > div {
    flex: 1;
    display: flex;
    flex-direction: column;
}
button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 100%;
  font-size: 16px;
}
button:hover {
  background-color: #45a049;
}
button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
.error-message {
  color: red;
  margin-bottom: 15px;
  padding: 10px;
  background-color: #ffebee;
  border-radius: 4px;
}
.cancellation-info {
    margin: 15px 0;
    padding: 10px;
    background-color: #e3f2fd;
    border: 1px solid #bbdefb;
    border-radius: 4px;
    color: #0d47a1;
}
.cancellation-info span {
    font-family: monospace;
    font-size: 1.1em;
    font-weight: bold;
    display: inline-block;
    margin-left: 5px;
}
.success-message {
    text-align: center;
    color: green;
}
.assignment-info {
    margin: 15px 0;
    padding: 10px;
    background-color: #f1f8e9;
    border: 1px solid #c8e6c9;
    border-radius: 4px;
    color: #2e7d32;
}
.reassignment-note {
    font-size: 0.9em;
    font-style: italic;
    color: #ef6c00;
}
small {
    color: #666;
    margin-top: 4px;
}
</style>
