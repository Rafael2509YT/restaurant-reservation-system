<template>
  <div class="reservation-card">
    <header class="card-header">
      <h2 class="title">Realiza una reservación</h2>
      <div v-if="!success" class="table-badge">
        <span class="label">Mesa Seleccionada:</span>
        <span class="value">#{{ tableId }}</span>
      </div>
    </header>

    <!-- ESTADO DE ÉXITO -->
    <div v-if="success" class="success-container animate-fade-in">
      <div class="success-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
      </div>
      
      <h3 class="success-title">¡Reservación Confirmada!</h3>
      <p class="success-subtitle">Esperamos verte pronto en nuestro restaurante.</p>

      <div v-if="assignedTable" class="info-box assignment">
        <div class="info-content">
          <p class="info-label">Mesa Asignada</p>
          <p class="info-main">{{ assignedTable.number }} <span class="cap">(Capacidad: {{ assignedTable.capacity }})</span></p>
          <p v-if="assignedTable.id !== tableId" class="reassignment-alert">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
            Optimización automática para tu grupo.
          </p>
        </div>
      </div>

      <div v-if="uniqueCode" class="info-box cancellation">
        <p class="reservation-id">Reserva: <strong>#{{ reservation_id }}</strong></p>
        <div class="code-wrapper">
          <span class="code-label">Código de cancelación:</span>
          <code class="code-value">{{ uniqueCode }}</code>
        </div>
        <small class="code-note">Guarda este código por si necesitas realizar cambios.</small>
      </div>

      <button @click="$emit('reset')" class="btn-secondary">
        Realizar otra reservación
      </button>
    </div>

    <!-- FORMULARIO -->
    <form v-else @submit.prevent="submitReservation" class="form-body">
      
      <div class="form-section">
        <label class="section-title">Información del Cliente</label>
        <div class="form-group">
          <label for="name">Nombre completo</label>
          <div class="input-wrapper">
            <input type="text" id="name" v-model="form.customer_name" placeholder="Ej. Juan Pérez" required />
          </div>
        </div>

        <div class="grid-2">
          <div class="form-group">
            <label for="email">Email <span class="optional">(opcional)</span></label>
            <input type="email" id="email" v-model="form.customer_email" placeholder="juan@ejemplo.com" />
          </div>
          <div class="form-group">
            <label for="phone">Teléfono <span class="optional">(opcional)</span></label>
            <input type="tel" id="phone" v-model="form.customer_phone" placeholder="+00 000 000" />
          </div>
        </div>
      </div>

      <div class="form-section">
        <label class="section-title">Detalles de la Reserva</label>
        <div class="grid-2">
          <div class="form-group">
            <label for="date">Fecha</label>
            <input type="date" id="date" v-model="selectedDate" :min="today" required />
          </div>

          <div class="form-group">
            <label for="guests">Invitados</label>
            <input type="number" id="guests" v-model="form.guests" required min="1" max="20" />
          </div>
        </div>

        <div class="form-group">
          <label>Hora de inicio</label>
          <div class="custom-time-picker">
            <!-- Selector de Hora -->
            <div class="stepper">
              <button type="button" @click="adjustTime('h', -1)" class="step-btn">−</button>
              <input type="text" v-model="displayHours" @change="validateManualTime" class="time-input" maxlength="2" />
              <button type="button" @click="adjustTime('h', 1)" class="step-btn">+</button>
            </div>
            <span class="time-separator">:</span>
            <!-- Selector de Minutos -->
            <div class="stepper">
              <button type="button" @click="adjustTime('m', -30)" class="step-btn">−</button>
              <input type="text" v-model="displayMinutes" @change="validateManualTime" class="time-input" maxlength="2" />
              <button type="button" @click="adjustTime('m', 30)" class="step-btn">+</button>
            </div>
          </div>
          <small class="help-text">Incrementos de 30 minutos dentro del horario comercial.</small>
        </div>
      </div>

      <div v-if="store.error" class="error-banner">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
        {{ store.error }}
      </div>

      <button type="submit" class="btn-primary" :disabled="store.loading">
        <span v-if="!store.loading">Confirmar Reservación</span>
        <span v-else class="loader"></span>
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useReservationStore } from '../stores/reservationStore';

const props = defineProps({
  tableId: {
    type: Number,
    required: true
  }
});

const emit = defineEmits(['reset', 'success']);
const store = useReservationStore();

// Variables de estado (Mantenidas)
const success = ref(false);
const selectedDate = ref('');
const selectedTime = ref('12:00'); // Valor por defecto
const uniqueCode = ref('');
const reservation_id = ref('');
const assignedTable = ref(null);

const form = ref({
  customer_name: '',
  customer_email: '',
  customer_phone: '',
  guests: 2
});

// Lógica de Picker Progresivo
const displayHours = ref('12');
const displayMinutes = ref('00');

// Sincronizar selectTime con los campos visuales
watch([displayHours, displayMinutes], () => {
  selectedTime.value = `${displayHours.value.padStart(2, '0')}:${displayMinutes.value.padStart(2, '0')}`;
});

const adjustTime = (type, delta) => {
  if (type === 'h') {
    let h = parseInt(displayHours.value) + delta;
    if (h > 23) h = 0;
    if (h < 0) h = 23;
    displayHours.value = h.toString().padStart(2, '0');
  } else {
    let m = parseInt(displayMinutes.value) + delta;
    if (m >= 60) {
      m = 0;
      adjustTime('h', 1);
    } else if (m < 0) {
      m = 30;
      adjustTime('h', -1);
    }
    displayMinutes.value = m.toString().padStart(2, '0');
  }
};

const validateManualTime = () => {
  let h = parseInt(displayHours.value) || 0;
  let m = parseInt(displayMinutes.value) || 0;
  
  if (h > 23) h = 23;
  if (m > 59) m = 30;
  
  displayHours.value = h.toString().padStart(2, '0');
  displayMinutes.value = (m < 30 ? 0 : 30).toString().padStart(2, '0');
};

const today = computed(() => {
  const d = new Date();
  return d.toISOString().split('T')[0];
});

// Lógica de Envío (Mantenida intacta)
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
        console.error("Reservation failed:", store.error);
    }
};

onMounted(() => {
    selectedDate.value = today.value;
});
</script>

<style scoped>
/* Contenedor Principal Estilo SaaS */
.reservation-card {
  max-width: 550px;
  margin: 2rem auto;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  border: 1px solid #e2e8f0;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

.card-header {
  padding: 1.5rem 2rem;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
}

.table-badge {
  background: #eef2ff;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  border: 1px solid #c7d2fe;
  display: flex;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.table-badge .label { color: #4338ca; }
.table-badge .value { font-weight: 700; color: #312e81; }

.form-body {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.section-title {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #64748b;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

/* Grilla para inputs */
.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #334155;
}

.optional {
  font-weight: 400;
  color: #94a3b8;
  font-size: 0.8rem;
}

input {
  padding: 0.625rem 0.875rem;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.2s;
  color: #1e293b;
}

input:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

/* Custom Time Picker */
.custom-time-picker {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #f1f5f9;
  padding: 0.5rem;
  border-radius: 10px;
  width: fit-content;
}

.stepper {
  display: flex;
  align-items: center;
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  overflow: hidden;
}

.step-btn {
  border: none;
  background: #f8fafc;
  color: #475569;
  width: 32px;
  height: 38px;
  cursor: pointer;
  font-size: 1.2rem;
  transition: background 0.2s;
}

.step-btn:hover { background: #e2e8f0; }

.time-input {
  width: 40px;
  border: none !important;
  text-align: center;
  padding: 0;
  font-weight: 700;
  box-shadow: none !important;
}

.time-separator {
  font-weight: 700;
  color: #64748b;
  font-size: 1.2rem;
}

/* Botones */
.btn-primary {
  background: #4f46e5;
  color: white;
  padding: 0.875rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 1rem;
}

.btn-primary:hover { background: #4338ca; transform: translateY(-1px); }
.btn-primary:disabled { background: #94a3b8; cursor: not-allowed; transform: none; }

.btn-secondary {
  background: white;
  color: #475569;
  border: 1px solid #cbd5e1;
  padding: 0.75rem;
  border-radius: 8px;
  width: 100%;
  font-weight: 600;
  cursor: pointer;
}

.btn-secondary:hover { background: #f8fafc; }

/* Estados de Éxito mejorados */
.success-container {
  padding: 3rem 2rem;
  text-align: center;
}

.success-icon {
  color: #10b981;
  margin-bottom: 1rem;
}

.success-title { font-size: 1.5rem; color: #1e293b; margin-bottom: 0.5rem; }
.success-subtitle { color: #64748b; margin-bottom: 2rem; }

.info-box {
  border-radius: 12px;
  padding: 1.25rem;
  margin-bottom: 1.5rem;
  text-align: left;
}

.info-box.assignment { background: #f0fdf4; border: 1px solid #bbf7d0; }
.info-box.cancellation { background: #f8fafc; border: 1px solid #e2e8f0; }

.info-label { font-size: 0.75rem; color: #166534; font-weight: 700; text-transform: uppercase; }
.info-main { font-size: 1.1rem; color: #14532d; font-weight: 700; margin: 0.25rem 0; }
.reassignment-alert { 
  display: flex; 
  align-items: center; 
  gap: 0.4rem; 
  font-size: 0.85rem; 
  color: #b45309; 
  margin-top: 0.5rem;
}

.code-value {
  display: block;
  background: #1e293b;
  color: #f8fafc;
  padding: 0.75rem;
  border-radius: 6px;
  font-family: monospace;
  font-size: 1.2rem;
  letter-spacing: 2px;
  margin: 0.5rem 0;
}

.error-banner {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #b91c1c;
  padding: 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

/* Loader */
.loader {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255,255,255,0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.animate-fade-in { animation: fadeIn 0.4s ease-out forwards; }

@media (max-width: 480px) {
  .grid-2 { grid-template-columns: 1fr; }
  .reservation-card { margin: 1rem; }
}
</style>