<script setup>
import { ref } from 'vue';
import AvailabilityChecker from '../components/AvailabilityChecker.vue';
import ReservationForm from '../components/ReservationForm.vue';
import ClientCancellation from '../components/ClientCancellation.vue';

const selectedTableId = ref(null);
const showCancellation = ref(false);

const handleTableSelected = (tableId) => {
  selectedTableId.value = tableId;
  showCancellation.value = false;
};

const handleReset = () => {
    selectedTableId.value = null;
};
</script>

<template>
  <main>
    <div class="header">
        <h1>Bienvenido a Nuestro Restaurante</h1>
        <p>¡Reserva tu mesa en línea hoy!</p>
    </div>

    <div v-if="!selectedTableId && !showCancellation">
        <AvailabilityChecker @select-table="handleTableSelected" />
        
        <div class="cancellation-toggle">
            <p>¿Ya tienes una reservación?</p>
            <button @click="showCancellation = true" class="text-btn">Cancelar una Reservación</button>
        </div>
    </div>
    
    <div v-else-if="showCancellation" class="reservation-section">
        <button @click="showCancellation = false" class="back-btn">&larr; Volver a la disponibilidad</button>
        <ClientCancellation />
    </div>

    <div v-else class="reservation-section">
        <button @click="handleReset" class="back-btn">&larr; Volver a la disponibilidad</button>
        <ReservationForm :tableId="selectedTableId" @reset="handleReset" />
    </div>

  </main>
</template>

<style scoped>
main {
    padding: 20px;
}
.header {
    text-align: center;
    margin-bottom: 30px;
}
.back-btn {
    background: none;
    border: none;
    color: #2196F3;
    cursor: pointer;
    font-size: 16px;
    margin-bottom: 20px;
    padding: 0;
}
.back-btn:hover {
    text-decoration: underline;
}
.reservation-section {
    max-width: 600px;
    margin: 0 auto;
}
.cancellation-toggle {
    text-align: center;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #ddd;
}
.text-btn {
    background: none;
    border: none;
    color: #f44336;
    text-decoration: underline;
    cursor: pointer;
    font-size: 16px;
}
</style>
