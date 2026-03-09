<template>
  <div class="client-cancellation">
    <h2>Cancelar una Reservación</h2>
    
    <div v-if="success" class="success-message">
        <p>Tu reservación ha sido cancelada exitosamente. La mesa ahora está disponible para otros.</p>
        <button @click="resetForm">Ok</button>
    </div>
    
    <form v-else @submit.prevent="submitCancel">
      <div class="form-group">
        <label for="resId">ID de la Reservación:</label>
        <input type="number" id="resId" v-model="form.id" required placeholder="Encontrado en tu confirmación" />
      </div>
      
      <div class="form-group">
        <label for="code">Código de Cancelación:</label>
        <input type="text" id="code" v-model="form.code" required placeholder="Ingresa el código único de 36 caracteres" />
      </div>
      
      <button type="submit" :disabled="loading" class="danger-btn">
        {{ loading ? 'Cancelando...' : 'Cancelar Reservación' }}
      </button>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useReservationStore } from '../stores/reservationStore';

const store = useReservationStore();
const success = ref(false);
const loading = ref(false);
const error = ref(null);

const form = ref({
  id: '',
  code: ''
});

const submitCancel = async () => {
    loading.value = true;
    error.value = null;
    try {
        await store.cancelReservation(form.value.id, form.value.code);
        success.value = true;
    } catch (e) {
        error.value = e.response?.data?.error || e.message;
    } finally {
        loading.value = false;
    }
};

const resetForm = () => {
    success.value = false;
    form.value.id = '';
    form.value.code = '';
};
</script>

<style scoped>
.client-cancellation {
  max-width: 500px;
  margin: 30px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fff;
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
.danger-btn {
  background-color: #f44336;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 100%;
}
.danger-btn:hover {
  background-color: #d32f2f;
}
.error-message {
  color: red;
  margin-top: 15px;
  padding: 10px;
  background-color: #ffebee;
  border-radius: 4px;
}
.success-message {
    color: #2e7d32;
    text-align: center;
}
</style>
